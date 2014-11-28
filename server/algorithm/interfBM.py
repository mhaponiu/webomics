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
# ======================================= BM ======================================================
# =================================================================================================

def findProgressBM(pattern, structs = "A"):
    LOG.INFO("Rozpoczynam poszukiwanie podobnej sekwencji algorytmem BM.\nWzorzec: " + str(pattern) + ". Poszukuje: " + str(structs))
    rm = RemoteManager()
    params = {"pattern" : pattern, "structs" : structs}
    tid = rm.run(findBM, params)
    LOG.DEBUG("Poszukiwanie podobnej sekwencji algorytmem BM. Numer watku: " + str(tid))
    
    return tid

## Funkcja przeszukuje baze danych w poszukiwaniu sekwencji pattern wykorzystujac algorytm Boyera-Moorea
#  @param pattern: 
#  @return: 
def findBM(callback, pattern, structs):
    # Sprawdzamy czy na pewno mamy do czynienia z lancuchem znakow
    if not isinstance(pattern, basestring):
        LOG.WARN("Wzorzec nie jest dozwolona sekwencja znakow!")
        return None
    pattern = str(pattern)
    
    # Wynik
    results = []

    # Tworzymy obiekt algorytmu
    LOG.INFO("Utworzenie obiektu algorytmu BM.")
    bm = calc.BM()
    
    # Obliczenie tablicy pomocniczej
    LOG.INFO("Obliczenie tablicy pomocniczej.")
    bm.prepare(pattern)
    
    if "S" in structs or "A" in structs:
        # 5 % 
        callback(5, "Retrieving the scaffolds database...")
        LOG.INFO("Pobranie sekwencji scaffoldow.")
        
        # Scaffolds
        scaffs = Scaffold.objects.values('id', 'sequence')
        
        # 20 % 
        callback(20, "Searching in scaffolds...")
        LOG.INFO("Uruchomienie algorytmu dla sekwencji scaffoldow.")
        
        scaffs_results = _findBM(callback, pattern, scaffs, bm, "Scaffold")
        results.extend(scaffs_results)
        LOG.DEBUG("Ilosc znalezionych scaffoldow: " + str(len(scaffs_results)))
    
    if "U" in structs or "A" in structs:
        # 40 % 
        callback(40, "Retrieving the undefined scaffolds database...")
        LOG.INFO("Pobranie sekwencji niezdefiniowanych scaffolodow.")
        
        # Undefined Scaffolds
        udef_scaffs = UndefinedScaffold.objects.values('id', 'sequence')
        
        # 55 % 
        callback(55, "Searching in undefined scaffolds...")
        LOG.INFO("Uruchomienie algorytmu dla sekwencji niezdefiniowanych scaffoldow.")
        
        udef_scaffs_results = _findBM(callback, pattern, udef_scaffs, bm, "Undefined scaffold")
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
        
        conts_results = _findBM(callback, pattern, conts, bm, "Contig")
        results.extend(conts_results)
        LOG.DEBUG("Ilosc znalezionych contigow: " + str(len(conts_results)))
    
    # 95 % 
    callback(95, "Saving results...")
    
    return (True, results)
            
## Slownik: klucz - ID struktury; wartosc - tupla z sekwencja jako pierwszym elementem oraz tablica indeksow jako drugim elementem
#  Python: { ID : (seq, [i1, i2, i3...]) }
#  Flex: [ ID, [seq, [i1, i2, i3...]] ] ?
def _findBM(callback, pattern, objects, bm, struct_name):
    text = ""
    results = []
    
    # !!!!!!!!!!!!!!!!!!
    #objects = objects[:10]
    # !!!!!!!!!!!!!!!!!!
    
    for obj in objects:
        text = str(obj['sequence'])
        if not isinstance(text, unicode):
            text = unicode(text)
        text = text.encode('utf8')

        # Uruchomienie algorytmu
        positions = bm.compute(text)
    
        # Pozycje na ktorych rozpoczyna sie wzorzec w danym tekscie
        for pos in positions:
            result = {}
            result['TYPE'] = struct_name
            result['ID'] = str(obj['id'])
            result['START_INDEX'] = str(pos - 1)
            result['END_INDEX'] = str(pos - 1 + len(pattern))
            results.append(result)

    return results
            
##
#  @param scaff: str(scaff_id : start_index)
#  @param pattern: Poszukiwany wzorzec
def getTextResultBM(scaff, pattern):
    scaff_id, start_index = str(scaff).split(";")
    try:
        scaff = Scaffold.objects.get(id = scaff_id)
    except Scaffold.DoesNotExist:
        LOG.WARN("Scaffold o ID: " + str(scaff_id) + " nie istnieje!")
        return None
    start_index = int(start_index)
    scaff_seq = scaff.sequence

    start = '<b><font color="blue">'
    
    if start_index < 10:
        prefix = scaff_seq[:start_index]
    else:
        prefix = scaff_seq[start_index - 10 : start_index]
    
    content = scaff_seq[start_index : start_index + len(pattern)]
    
    end = '</font></b>'
    
    if start_index + len(pattern) + 10 > len(scaff_seq):
        sufix = scaff_seq[start_index + len(pattern):]
    else:
        sufix = scaff_seq[start_index + len(pattern) : start_index + len(pattern) + 10]

    return (prefix + start + content + end + sufix)