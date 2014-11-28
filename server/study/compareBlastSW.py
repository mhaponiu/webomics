import sys
import os
import time
import random

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

calc_path = os.path.join( this_module_path, '..', '..', 'calculation', 'build')
sys.path.append(calc_path)

output_path = os.path.join(this_module_path, 'output')

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

# Biblioteka obliczeniowa
import calc

NUCLEOTIDES = "ACGT"

DEF_MATCH       = 2
DEF_MISMATCH    = -1 
DEF_GAP_OPEN    = -3
DEF_GAP_EXTEND  = -1

DEF_W           = 11
DEF_T           = 0.001
DEF_C           = 5
DEF_CUT_OFF     = 10

DEF_PATTERN_LEN = 500
DEF_SEQ_LEN     = 5000

def generateSequence(nucleotides_count):
    return (random.choice(NUCLEOTIDES)) * nucleotides_count

def generateDatabase(pattern, length, count, percent_changed):
    sequences = []
    
    pattern_len = len(pattern)
    nucls_changed = int(pattern_len * percent_changed)
    
    for _ in range(count):
        left_right = (length - pattern_len) / 2
        prefix = generateSequence(left_right)
        sufix = generateSequence(left_right)
        stem = pattern
        
        # Losowa modyfikacja trzonu zgodnie z zadanym procentem
        for _ in range(nucls_changed):
            pos = random.randint(0, len(stem) - 1)
            stem = stem[:pos] + random.choice(NUCLEOTIDES.replace(stem[pos], "")) + stem[pos + 1 :]
            
        sequences.append(prefix + stem + sufix)
        #print "!!! LeftRight:", left_right
        #print "!!! Prefix:", len(prefix)
        #print "!!! Sufix:", len(sufix)
        #print "!!! Stem:", len(stem)
        #print "!!! Dlugosc wygenerowanej sekwencji:", len(sequences[-1])
            
    return sequences

def runBlast(pattern, database, w, t, c, cut_off):
    blast = calc.Blast(w, t, c)
    
    res = blast.prepare(str(pattern))
    if res == 0:
        print "Parametr W (= " + str(w) + ") powinien byc nie wiekszy od dlugosci zadanej sekwencji (= " + str(len(pattern)) + ")."
        return None
        
    for seq in database:
        blast.addSequence("-1", seq)
        
    res = blast.search()
    if res == 0:
        print "Zbyt wysoka wartosc parametru W (= " + str(w) + "). Nie mozna odnalezc zadnego fragmentu poszukiwanej sekwecji."
        return None
    
    res = blast.estimate()
    if res == 0:
        print "Zbyt wysoka wartosc parametru T (= " + str(t) + "). Powinien zawierac sie w zakresie od " + str(blast.getMinRate()) + " do " + str(blast.getMaxRate()) + ", srednia wartosc rate wynosi " + str(blast.getAvgRate())
        print "Uruchomienie algorytmu BLAST z nowa wartoscia parametru T =", str(blast.getAvgRate())
        return runBlast(pattern, database, w, blast.getAvgRate(), c, cut_off)
    
    res = blast.extend()
    
    aligns = blast.getAligns(cut_off)
    
    return aligns

def runSW(pattern, database, match, mismatch, gap_open, gap_extend):
    results = []
    for seq in database:
        sw = calc.SW()
        max_value = sw.fastInitAndCompute(match, mismatch, gap_open, gap_extend, seq, pattern)
        results.append(max_value)
        
    return results

def timePatternCompare():
    pattern_range = range(50, 500, 50)
    
    print "Badania porownawcze algorytmow BLAST oraz SW w zaleznosci od dlugosci sekwencji wzorcowej..."

    output_file = open(os.path.join(output_path, "compare_time_pattern_blast_sw.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,BLAST_TIME,SW_TIME\n')

    for pattern_len in pattern_range:
        print "\tDlugosc wzorca:", pattern_len
        
        # Wygenerowanie wzorca
        print "\t\tGenerowanie sekwencji..."
        PATTERN = generateSequence(pattern_len)
        # Wygenerowanie sekwencji przeszukiwanych
        DATABASE = generateDatabase(PATTERN, DEF_SEQ_LEN, 100, 0.25)
        
        # Uruchomienie algorytmu BLAST
        print "\t\tUruchomienie algorytmu BLAST..."
        ts_blast = time.time()
        aligns = runBlast(PATTERN, DATABASE, DEF_W, DEF_T, DEF_C, DEF_CUT_OFF)
        te_blast = time.time()
        
        # Uruchomienie algorytmu SW
        print "\t\tUruchomienie algorytmu SW..."
        ts_sw = time.time()
        sw_results = runSW(PATTERN, DATABASE, DEF_MATCH, DEF_MISMATCH, DEF_GAP_OPEN, DEF_GAP_EXTEND)
        te_sw = time.time()
        
        output_file.write('%r,%r,%f,%f\n' % (len(PATTERN), DEF_SEQ_LEN, (te_blast - ts_blast), (te_sw - ts_sw)))
    
    output_file.close()
    

def timeSeqCompare():
    seq_range = range(1000, 10000, 1000)
    
    # Wygenerowanie wzorca
    print "\t\tGenerowanie sekwencji..."
    PATTERN = generateSequence(DEF_PATTERN_LEN)
    
    print "Badania porownawcze algorytmow BLAST oraz SW w zaleznosci od dlugosci sekwencji przeszukiwanych..."

    output_file = open(os.path.join(output_path, "compare_time_seq_blast_sw.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,BLAST_TIME,SW_TIME\n')

    for seq_len in seq_range:
        print "\tDlugosc sekwencji:", seq_len
        
        # Wygenerowanie sekwencji przeszukiwanych
        DATABASE = generateDatabase(PATTERN, seq_len, 100, 0.25)
        
        # Uruchomienie algorytmu BLAST
        print "\t\tUruchomienie algorytmu BLAST..."
        ts_blast = time.time()
        aligns = runBlast(PATTERN, DATABASE, DEF_W, DEF_T, DEF_C, DEF_CUT_OFF)
        te_blast = time.time()
        
        # Uruchomienie algorytmu SW
        print "\t\tUruchomienie algorytmu SW..."
        ts_sw = time.time()
        sw_results = runSW(PATTERN, DATABASE, DEF_MATCH, DEF_MISMATCH, DEF_GAP_OPEN, DEF_GAP_EXTEND)
        te_sw = time.time()
        
        output_file.write('%r,%r,%f,%f\n' % (len(PATTERN), seq_len, (te_blast - ts_blast), (te_sw - ts_sw)))
    
    output_file.close()

def accuracyCompare():
    pass


if __name__ == '__main__':
    #timePatternCompare()
    timeSeqCompare()
    accuracyCompare()
    