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
# ====================================== BLAST ====================================================
# =================================================================================================

def findProgressBLAST(pattern, w, t, c, cut_off, structs = "A"):
    LOG.INFO("Rozpoczynam poszukiwanie podobnej sekwencji algorytmem BLAST.\nW: " + str(w) + "\nT: " + str(t) + "\nC: " + str(c) + "\nCUT OFF: " + str(cut_off) + "\nWzorzec: " + str(pattern) + "\nPoszukuje: " + str(structs))
    rm = RemoteManager()
    params = {"pattern" : pattern, "w" : w, "t" : t, "c" : c, "cut_off" : cut_off, "structs" : structs}
    tid = rm.run(runBLAST, params)
    LOG.DEBUG("Poszukiwanie podobnej sekwencji algorytmem BLAST. Numer watku: " + str(tid))
    
    return tid

## Funkcja przeszukuje baze danych w poszukiwaniu sekwencji pattern wykorzystujac algorytm BLAST
#  @param pattern:
#  @param w:
#  @param t:
#  @param c:
#  @param cut_off:
#  @return: 
def runBLAST(callback, pattern, w, t, c, cut_off, structs):
    return _runBLAST(pattern, w, t, c, cut_off, structs, callback)

## Funkcja przeszukuje baze danych w poszukiwaniu sekwencji pattern wykorzystujac algorytm BLAST - bez progresu
#  @param pattern:
#  @param w:
#  @param t:
#  @param c:
#  @param cut_off:
#  @return: 
def _runBLAST(pattern, w, t, c, cut_off, structs = "A", callback = None):
    # Sprawdzamy czy na pewno mamy do czynienia z lancuchem znakow
    if not isinstance(pattern, basestring):
        LOG.WARN("Wzorzec nie jest dozwolona sekwencja znakow!")
        return None
    pattern = str(pattern)
    
    if callback == None:
        callback = debug

    # Wynik
    results = []

    start = time.time()

    # Tworzymy obiekt algorytmu
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

    callback(50, "Searching in database...")
    LOG.INFO("Przeszukanie sekwencji.")
    
    res = blast.search()
    
    if res == 0:
        LOG.WARN("Zbyt wysoka wartosc parametru W (= " + str(w) + "). Nie mozna odnalezc zadnego fragmentu poszukiwanej sekwecji.")
        return (False, "Zbyt wysoka wartosc parametru W (= " + str(w) + "). Nie mozna odnalezc zadnego fragmentu poszukiwanego sekwecji.")

    callback(70, "Limiting the set of sequences...")
    LOG.INFO("Zmniejszenie liczby elementow najistotniejszych.")
    
    res = blast.estimate()
    
    if res == 0:
        LOG.WARN("Zbyt wysoka wartosc parametru T (= " + str(t) + "). Powinien zawierac sie w zakresie od " + str(blast.getMinRate()) + " do " + str(blast.getMaxRate()) + ", srednia wartosc rate wynosi " + str(blast.getAvgRate()))
        return (False, "Zbyt wysoka wartosc parametru T (= " + str(t) + "). Powinien zawierac sie w zakresie od " + str(blast.getMinRate()) + " do " + str(blast.getMaxRate()) + ", srednia wartosc rate wynosi " + str(blast.getAvgRate()))
    
    callback(90, "Extending keywords...")
    LOG.INFO("Rozszerzenie slow kluczowych.")
    
    res = blast.extend()
    
    callback(95, "Calculating additional parameters...")
    LOG.INFO("Obliczenie dodatkowych parametrow.")
    
    res = blast.evaluate()

    callback(99, "Retreving results...")
    LOG.INFO("Pobranie " + str(cut_off) + " najlepszych sekwencji.")

    aligns = blast.getAligns(cut_off)
    
    LOG.INFO("Pogrupowanie wynikow. Pobranych rezultatow: " + str(len(aligns)))
    aligns_len = len(aligns)
    # Zebranie wynikow
    for i, align in enumerate(aligns):
        same = align.getSame()
        align_len = align.getAlignLength()
        seq_id = align.getSequenceId()
        result = {}
        try:
            result['TYPE'] = id_type[str(seq_id)]
        except KeyError:
            result['TYPE'] = "Unknown"
        result['ID'] = str(seq_id)
        result['SCORE'] = str(align.getScore())
        result['IDENTITY'] = str((float(same) / float(align_len) * 100.00))
        result['GAPS'] = str(align.getGaps())
        result['LENGTH'] = str(align_len)
        result['SEQ_START_INDEX'] = str(align.getSeqStart())
        result['SEQ_END_INDEX'] = str(align.getSeqEnd())
        results.append(result)
        LOG.DEBUG("Zapisalem wynik " + str(i+1) + "/" + str(aligns_len) + ":\n" + str(result))
    LOG.INFO("Zakonczylem grupowanie wynikow. Rezultatow: " + str(len(results)))
    
    end = time.time()
    LOG.DEBUG("Czas dzialania algorytmu BLAST dla sekwencji o dlugosci " + str(len(str(pattern))) + ": " + str(end - start) + "s.")
    
    return (True, results)