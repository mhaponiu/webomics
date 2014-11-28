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
# ====================================== BLAST z SW ===============================================
# =================================================================================================

def findProgressBLAST_SW(pattern, w, t, c, cut_off, structs = "A"):
    LOG.INFO("Rozpoczynam poszukiwanie podobnej sekwencji algorytmem BLAST.\nW: " + str(w) + "\nT: " + str(t) + "\nC: " + str(c) + "\nCUT OFF: " + str(cut_off) + "\nWzorzec: " + str(pattern) + "\nPoszukuje: " + str(structs))
    rm = RemoteManager()
    params = {"pattern" : pattern, "w" : w, "t" : t, "c" : c, "cut_off" : cut_off, "structs" : structs}
    tid = rm.run(runBLAST_SW, params)
    LOG.DEBUG("Poszukiwanie podobnej sekwencji algorytmem BLAST. Numer watku: " + str(tid))
    
    return tid

## Funkcja przeszukuje baze danych w poszukiwaniu sekwencji pattern wykorzystujac algorytm BLAST oraz SW
#  @param pattern:
#  @param w:
#  @param t:
#  @param c:
#  @param cut_off:
#  @return: 
def runBLAST_SW(callback, pattern, w, t, c, cut_off, structs):
    return _runBLAST_SW(pattern, w, t, c, cut_off, structs, callback)

## Funkcja przeszukuje baze danych w poszukiwaniu sekwencji pattern wykorzystujac algorytm BLAST oraz SW - bez progresu
#  @param pattern:
#  @param w:
#  @param t:
#  @param c:
#  @param cut_off:
#  @return: 
def _runBLAST_SW(pattern, w, t, c, cut_off, structs = "A", callback = None):
    # Sprawdzamy czy na pewno mamy do czynienia z lancuchem znakow
    if not isinstance(pattern, basestring):
        LOG.WARN("Wzorzec nie jest dozwolona sekwencja znakow!")
        return None
    pattern = str(pattern)
    
    if callback == None:
        callback = debug

    # Tworzymy obiekt algorytmu BLAST
    LOG.INFO("Utworzenie obiektu algorytmu BLAST.")
    blast = calc.Blast(w, t, c)
    
    callback(5, "Preparing sequence...")
    LOG.INFO("Przygotowanie sekwencji.")
    
    res = blast.prepare(str(pattern))
    if res == 0:
        LOG.WARN("Parametr W (= " + str(w) + ") powinien byc nie wiekszy od dlugosci zadanej sekwencji (= " + str(len(pattern)) + ").")
        return (False, "Parametr W (= " + str(w) + ") powinien byc nie wiekszy od dlugosci zadanej sekwencji (= " + str(len(pattern)) + ").")
    
    types = []
    # Scaffolds
    if "S" in structs or "A" in structs:
        callback(10, "Retrieving the scaffolds database...")
        LOG.INFO("Pobranie sekwencji scaffolodow.")
        scaffs = Scaffold.objects.values('id', 'sequence')
        types.append((static.SEARCH_SCAFFOLDS, scaffs))
    # Undefined Scaffolds
    if "U" in structs or "A" in structs:
        callback(11, "Retrieving the undefined scaffolds database...")
        LOG.INFO("Pobranie sekwencji niezdefiniowanych scaffolodow.")
        uscaffs = UndefinedScaffold.objects.values('id', 'sequence')
        types.append((static.SEARCH_UDEF_SCAFFOLDS, uscaffs))
    # Contigs
    if "C" in structs or "A" in structs:
        callback(12, "Retrieving the contigs database...")
        LOG.INFO("Pobranie sekwencji contigow.")
        conts = Contig.objects.values('id', 'sequence')
        types.append((static.SEARCH_CONTIGS, conts))
    
    callback(15, "Adding sequences to algorithm...")
    LOG.INFO("Dodanie sekwencji do algorytmu.")
    
    id_type = {}
    #TODO: TESTOWO OGRANICZONE!!!
    for (type_, seqs) in types: 
        for seq in seqs:#[:10]:
            blast.addSequence(str(seq['id']), str(seq['sequence']))
            id_type[str(seq['id'])] = str(type_)

    callback(30, "Searching in database...")
    LOG.INFO("Przeszukanie sekwencji.")
    
    res = blast.search()
    
    if res == 0:
        LOG.WARN("Zbyt wysoka wartosc parametru W (= " + str(w) + "). Nie mozna odnalezc zadnego fragmentu poszukiwanej sekwecji.")
        return (False, "Zbyt wysoka wartosc parametru W (= " + str(w) + "). Nie mozna odnalezc zadnego fragmentu poszukiwanego sekwecji.")

    callback(50, "Limiting the set of sequences...")
    LOG.INFO("Zmniejszenie liczby elementow najistotniejszych.")
    
    res = blast.estimate()
    
    if res == 0:
        LOG.WARN("Zbyt wysoka wartosc parametru T (= " + str(t) + "). Powinien zawierac sie w zakresie od " + str(blast.getMinRate()) + " do " + str(blast.getMaxRate()) + ", srednia wartosc rate wynosi " + str(blast.getAvgRate()))
        return (False, "Zbyt wysoka wartosc parametru T (= " + str(t) + "). Powinien zawierac sie w zakresie od " + str(blast.getMinRate()) + " do " + str(blast.getMaxRate()) + ", srednia wartosc rate wynosi " + str(blast.getAvgRate()))
    
    callback(70, "Extending keywords...")
    LOG.INFO("Rozszerzenie slow kluczowych.")
    
    res = blast.extend()
    
    callback(75, "Calculating additional parameters...")
    LOG.INFO("Obliczenie dodatkowych parametrow.")
    
    res = blast.evaluate()

    callback(79, "Retreving results...")
    LOG.INFO("Pobranie " + str(cut_off) + " najlepszych sekwencji.")

    aligns = blast.getAligns(cut_off)
    
    results_sw = []
    
    LOG.INFO("Pogrupowanie wynikow BLAST. Pobranych rezultatow: " + str(len(aligns)))
    
    # Uruchomienie algorytmu SW z domyslnymi wartosciami parametrow
    
    # Tworzymy obiekt algorytmu SW
    LOG.INFO("Utworzenie obiektu algorytmu SW.")
    callback(80, "Starting Smith-Waterman algorithm for top " + str(cut_off) + " sequences...")
    sw = calc.SW()
    
    for i, align in enumerate(aligns):
        seq_id = align.getSequenceId()
        try:
            seq_type = id_type[str(seq_id)]
        except KeyError:
            seq_type = "Unknown"
            
        obj = None
        try:
            if seq_type == static.SEARCH_SCAFFOLDS:
                obj = Scaffold.objects.get(id = str(seq_id))
            elif seq_type == static.SEARCH_UDEF_SCAFFOLDS:
                obj = UndefinedScaffold.objects.get(id = int(seq_id))
            elif seq_type == static.SEARCH_CONTIGS:
                obj = Contig.objects.get(id = int(seq_id))
            else:
                LOG.WARN("Blad wykonania programu! Nie znaleziono typu " + str(seq_type))
                return (False, "Blad wykonania programu!")
        except Scaffold.DoesNotExist or UndefinedScaffold.DoesNotExist or Contig.DoesNotExist:
            LOG.WARN("Blad wykonania programu! Nie znaleziono sekwencji " + str(seq_id) + " w typie " + str(seq_type))
            return (False, "Blad wykonania programu!")
        
        # Uruchomienie algorytmu
        LOG.INFO("Uruchomienie algorytmu w wersji fastComputeWithStringsResult")
        similarity = sw.fastComputeWithStringsResult(2, -1, -3, -1, str(obj.sequence), pattern)
        
        result = {}
        result['TYPE'] = str(seq_type)
        result['ID'] = str(obj.id)
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
        results_sw.append(result)
    
    callback(95, "Sorting results...")
    LOG.INFO("Posortowanie wynikow.")
    results_sw = sorted(results_sw, key=lambda res: res['IDENTITY'], reverse=True)

    return (True, results_sw)