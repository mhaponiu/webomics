# Biblioteka obliczeniowa
import calc

# Dostep do bazy danych
from server.scaffold.models import Scaffold
from server.scaffold.models import UndefinedScaffold

from server.contig.models import Contig

from server.config import static

from server.utils.remoteAccess import RemoteManager

import time

from server.utils import log as LOG

def debug(progress, text, arg = None):
    print str(progress), "-->", text

# =================================================================================================
# ======================================= SW ======================================================
# =================================================================================================

def searchProgressSW(pattern, match = 2, mismatch = -1, gap_open = -1, gap_extend = -1, structs = "A"):
    LOG.INFO("Rozpoczynam poszukiwanie podobnej sekwencji algorytmem SW.\nMATCH: " + str(match) + "\nMISMATCH: " + str(mismatch) + "\nGAP OPEN: " + str(gap_open) + "\nGAP EXTEND: " + str(gap_extend) + "\nWzorzec: " + str(pattern) + "\nPoszukuje: " + str(structs))
    rm = RemoteManager()
    params = {"pattern" : pattern, "structs" : structs, "match" : match, "mismatch" : mismatch, "gap_open" : gap_open, "gap_extend" : gap_extend}
    tid = rm.run(searchSW, params)
    LOG.DEBUG("Poszukiwanie podobnej sekwencji algorytmem SW. Numer watku: " + str(tid))
    
    return tid

## Funkcja przeszukuje baze danych w poszukiwaniu najbardziej podobnej sekwencji nukleotydow wykorzystujac algorytm Smidtha-Watermana
#  @param pattern: 
#  @param match: 
#  @param mismatch: 
#  @param gap_open:
#  @param gap_extend:  
#  @param structs:
#  @return: 
def searchSW(callback, pattern, structs, match = 2, mismatch = -1, gap_open = -3, gap_extend = -1):
    return (True, _searchSW(pattern, match, mismatch, gap_open, gap_extend, structs, callback))

def _searchSW(pattern, structs, match = 2, mismatch = -1, gap_open = -3, gap_extend = -1, callback = None):
    # Sprawdzamy czy na pewno mamy do czynienia z lancuchem znakow
    if not isinstance(pattern, basestring):
        LOG.WARN("Wzorzec nie jest dozwolona sekwencja znakow!")
        return None
    pattern = str(pattern)
    
    if callback == None:
        callback = debug
    
    # Wynik
    results = []
    
    # Tworzymy obiekt algorytmu
    LOG.INFO("Utworzenie obiektu algorytmu SW.")
    sw = calc.SW()

    if "S" in structs or "A" in structs:        
        # 5 % 
        callback(5, "Retrieving the scaffolds database...")
        LOG.INFO("Pobranie sekwencji scaffoldow z bazy danych.")
        
        # Scaffolds
        scaffs = Scaffold.objects.values('id', 'sequence')
        
        # 20 % 
        callback(20, "Searching in scaffolds...")
        LOG.INFO("Uruchomienie algorytmu dla sekwencji scaffoldow.")
        
        scaffs_results = _searchMaxSW(callback, pattern, scaffs, sw, match, mismatch, gap_open, gap_extend, "Scaffold")
        results.extend(scaffs_results)
        LOG.DEBUG("Ilosc znalezionych scaffoldow: " + str(len(scaffs_results)))
    
    if "U" in structs or "A" in structs:
        # 40 % 
        callback(40, "Retrieving the undefined scaffolds database...")
        LOG.INFO("Pobranie sekwencji niezdefiniowanych scaffoldow.")
        
        # Undefined Scaffolds
        udef_scaffs = UndefinedScaffold.objects.values('id', 'sequence')
        
        # 55 % 
        callback(55, "Searching in undefined scaffolds...")
        LOG.INFO("Uruchomienie algorytmu dla sekwencji niezdefiniowanych scaffoldow.")
        
        udef_scaffs_results = _searchMaxSW(callback, pattern, udef_scaffs, sw, match, mismatch, gap_open, gap_extend, "Undefined scaffold")
        results.extend(udef_scaffs_results)
        LOG.DEBUG("Ilosc znalezionych niezdefiniowanych scaffoldow: " + str(len(udef_scaffs_results)))
    
    if "C" in structs or "A" in structs:
        # 75 % 
        callback(75, "Retrieving the contigs database...")
        LOG.INFO("Pobranie sekwencji contigow.")
        
        # Contigs
        conts = Contig.objects.values('id', 'sequence')
        
        # 90 % 
        callback(90, "Searching in contigs...")
        LOG.INFO("Uruchomienie algorytmu dla sekwencji contigow.")
        
        conts_results = _searchMaxSW(callback, pattern, conts, sw, match, mismatch, gap_open, gap_extend, "Contig")
        results.extend(conts_results)
        LOG.DEBUG("Ilosc znalezionych contigow: " + str(len(conts_results)))
    
    # 95 % 
    callback(95, "Saving results...")
    
    return results
    
def _searchMaxSW(callback, pattern, objects, sw, match, mismatch, gap_open, gap_extend, struct_name):
    results = []
    
    ### !!!!!!!!!!!!!!!!!!!!!!!!
    #objects = objects[6:7]
    ### !!!!!!!!!!!!!!!!!!!!!!!!
    
    for i, obj in enumerate(objects):
        # Uruchomienie algorytmu
        LOG.INFO("Uruchomienie algorytmu w wersji fastComputeWithStringsResult")
        similarity = sw.fastComputeWithStringsResult(match, mismatch, gap_open, gap_extend, str(obj['sequence']), pattern)

        result = {}
        result['TYPE'] = str(struct_name)
        result['ID'] = str(obj['id'])
        result['SCORE'] = str(similarity.getValue())
        seq_after = similarity.getText()
        pat_after = similarity.getPattern()
        align_len = len(seq_after)
        gaps = 0
        same = 0
        for i, l in enumerate(seq_after):
            if l == '-':    # dziurka
                gaps += 1
            elif l == pat_after[i]: # takie same
                same += 1
        result['GAPS'] = str(gaps)
        result['IDENTITY'] = str(float(same) / float(align_len))
        result['LENGTH'] = align_len
        seq_end_index = similarity.getPositionJ()
        seq_start_index = seq_end_index - len(str(seq_after).replace("-", ""))
        result['SEQ_START_INDEX'] = seq_start_index
        result['SEQ_END_INDEX'] = seq_end_index
        results.append(result)
    
    LOG.INFO("Posortowanie wynikow.")
    results = sorted(results, key=lambda res: res['IDENTITY'], reverse=True)
    
    return results

## 
#  @param pattern: 
#  @param obj_id: 
#  @param type_: 
#  @param match: 
#  @param mismatch: 
#  @param gap: 
#  @return: 
def getTextsResultSW(pattern, obj_id, type_, match = 2, mismatch = -1, gap_open = -3, gap_extend = -1):
    obj = None
    try:
        if type_ == static.SCAFFOLDS:
            obj = Scaffold.objects.get(id = str(obj_id))
        elif type_ == static.UDEF_SCAFFOLDS:
            obj = UndefinedScaffold.objects.get(id = int(obj_id))
        elif type_ == static.CONTIGS:
            obj = Contig.objects.get(id = int(obj_id))
        else:
            return None
    except Scaffold.DoesNotExist or UndefinedScaffold.DoesNotExist or Contig.DoesNotExist:
        return None

    # Tworzymy obiekt algorytmu
    sw = calc.SW()

    # Uruchamiamy algorytm, ktory automatycznie zwraca max wartosc oraz przetworzone sekwencje
    similarity_obj = sw.fastComputeWithStringsResult(match, mismatch, gap_open, gap_extend, str(obj.sequence), str(pattern))
    
    return [similarity_obj.getValue(), similarity_obj.getPattern(), similarity_obj.getText()]
