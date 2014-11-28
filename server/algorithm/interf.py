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

class Similarity:
    struct = None
    object_id = ""
    similarity_obj = None
    
    def __init__(self, struct, object_id, similarity_obj):
        self.struct = struct
        self.object_id = object_id
        self.similarity_obj = similarity_obj

def debug(progress, text, arg = None):
    print str(progress), "-->", text

def getAllSequences():
    LOG.INFO("Pobieram wszystkie sekwencje z bazy danych.")
    
    # Wszystkie obiekty, ktore sa przeszukiwane
    objects = []
    
    # ----------------- SCAFFOLDY ------------------
    LOG.INFO("Pobieram scaffoldy.")
    scaffs = Scaffold.objects.all()
    
    # --------- NIEZIDENTYFIKOWANE SCAFFOLDY -------
    LOG.INFO("Pobieram niezdefiniowane scaffoldy.")
    udef_scaffs = UndefinedScaffold.objects.all()
    
    # ------------------ CONTIGI -------------------
    LOG.INFO("Pobieram contigi.")
    conts = Contig.objects.all()
    
    # ---------- NIEZIDENTYFIKOWANE CONTIGI --------
    
    
    # ----------------------------------------------
    
    objects.extend(scaffs)
    objects.extend(udef_scaffs)
    objects.extend(conts)
    
    return objects

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
    objects = objects[6:7]
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
    results = sorted(results, key=lambda res: res[0], reverse=True)
    
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

# =================================================================================================
# ====================================== KMP ======================================================
# =================================================================================================

def findProgressKMP(pattern, structs = "A"):
    LOG.INFO("Rozpoczynam poszukiwanie podobnej sekwencji algorytmem KMP.\nWzorzec: " + str(pattern) + ". Poszukuje: " + str(structs))
    rm = RemoteManager()
    params = {"pattern" : pattern, "structs" : structs}
    tid = rm.run(findKMP, params)
    LOG.DEBUG("Poszukiwanie podobnej sekwencji algorytmem KMP. Numer watku: " + str(tid))
    
    return tid

## Funkcja przeszukuje baze danych w poszukiwaniu sekwencji pattern wykorzystujac algorytm Knutha-Morrisa-Pratha
#  @param pattern: 
#  @return: 
def findKMP(callback, pattern, structs):
    # Sprawdzamy czy na pewno mamy do czynienia z lancuchem znakow
    if not isinstance(pattern, basestring):
        LOG.WARN("Wzorzec nie jest dozwolona sekwencja znakow!")
        return None
    pattern = str(pattern)
    
    # Wynik
    results = []

    # Tworzymy obiekt algorytmu
    LOG.INFO("Utowrzenie obiektu algorytmu KMP.")
    kmp = calc.KMP()
    
    # Obliczenie tablicy pomocniczej
    LOG.INFO("Obliczenie tablicy pomocniczej.")
    status = kmp.calculateTable(pattern)
    
    if "S" in structs or "A" in structs:
        # 5 % 
        callback(5, "Retrieving the scaffolds database...")
        LOG.INFO("Pobranie sekwencji scaffoldow.")
        
        # Scaffolds
        scaffs = Scaffold.objects.values('id', 'sequence')
        
        # 20 % 
        callback(20, "Searching in scaffolds...")
        LOG.INFO("Uruchomienie algorytmu dla sekwencji scaffoldow.")
        
        scaffs_results = _findKMP(callback, pattern, scaffs, kmp, "Scaffold")
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
        
        udef_scaffs_results = _findKMP(callback, pattern, udef_scaffs, kmp, "Undefined scaffold")
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
        
        conts_results = _findKMP(callback, pattern, conts, kmp, "Contig")
        results.extend(conts_results)
        LOG.DEBUG("Ilosc znalezionych contigow: " + str(len(conts_results)))
    
    # 95 % 
    callback(95, "Saving results...")
    
    return (True, results)
            
## Slownik: klucz - ID struktury; wartosc - tupla z sekwencja jako pierwszym elementem oraz tablica indeksow jako drugim elementem
#  Python: { ID : (seq, [i1, i2, i3...]) }
#  Flex: [ ID, [seq, [i1, i2, i3...]] ] ?
def _findKMP(callback, pattern, objects, kmp, struct_name):
    text = ""
    results = []
    
    # !!!!!!!!!!!!!!!!!!
    objects = objects[:10]
    # !!!!!!!!!!!!!!!!!!
    
    for obj in objects:
        text = str(obj['sequence'])
        if not isinstance(text, unicode):
            text = unicode(text)
        text = text.encode('utf8')

        # Uruchomienie algorytmu
        positions = kmp.compute(text)
    
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
def getTextResultKMP(scaff, pattern):
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
        types.append(("Scaffold", scaffs))
    # Undefined Scaffolds
    if "U" in structs or "A" in structs:
        callback(11, "Retrieving the undefined scaffolds database...")
        LOG.INFO("Pobranie sekwencji niezdefiniowanych scaffolodow.")
        uscaffs = UndefinedScaffold.objects.values('id', 'sequence')
        types.append(("Undefined scaffold", uscaffs))
    # Contigs
    if "C" in structs or "A" in structs:
        callback(12, "Retrieving the contigs database...")
        LOG.INFO("Pobranie sekwencji contigow.")
        conts = Contig.objects.values('id', 'sequence')
        types.append(("Contig", conts))
    
    callback(15, "Adding sequences to algorithm...")
    LOG.INFO("Dodanie sekwencji do algorytmu.")
    
    id_type = {}
    #TODO: TESTOWO OGRANICZONE!!!
    for (type_, seqs) in types: 
        for seq in seqs[:10]:
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