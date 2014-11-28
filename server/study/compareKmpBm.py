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

from server.scaffold.models import Scaffold as ScaffoldDB
from server.contig.models import Contig as ContigDB

NUCLEOTIDES = "ACGT"

def generateSequence(nucleotides_count):
    return (random.choice(NUCLEOTIDES)) * nucleotides_count

def kmp(pattern, sequence, output_file):
    kmp = calc.KMP()
    
    tstart = time.time()
    table_status = kmp.calculateTable(pattern)
    tend = time.time()
    positions = kmp.compute(sequence)
    
    #print "\tKMP:", len(positions)
    
    return (tend - tstart)
    
def bm(pattern, sequence, output_file):
    bm = calc.BM()

    tstart = time.time()
    bm.prepare(pattern)
    tend = time.time()
    positions = bm.compute(sequence)
    
    #print "\tBM:", len(positions)
    
    return (tend - tstart)

def compareTest():
    PATTERN_LENS = range(10000, 100000, 10000) # od 10 000 do 100 000 co 10 000
    SEQ_LENS = range(50000, 1000000, 50000) # od 50 000 do 1 000 000 co 50 000
    
    # Sekwencje domyslne
    default_pattern = generateSequence(10000)   # 10 000
    default_seq = generateSequence(10000000)  # 10 000 000

    # TYLKO CZAS SZUKANIA
    print "Porownanie algorytmow KMP oraz BM w zaleznosci od dlugosci sekwencji przeszukiwanej (tylko czas wyszukiwania)..."
    
    output_file = open(os.path.join(output_path, "compare_kmp_bm_only_search_time.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,KMP_TIME,BM_TIME\n')
    
    bm_algo = calc.BM()
    kmp_algo = calc.KMP()
    
    print "Przygotowywanie algorytmu BM..."
    tstart = time.time()
    bm_algo.prepare(default_pattern)
    tend = time.time()
    bm_prep_time = tend - tstart
    print "Przygotowywanie algorytmu KMP..."
    tstart = time.time()
    kmp_algo.calculateTable(default_pattern)
    tend = time.time()
    kmp_prep_time = tend - tstart
    
    print "KMP prep:", kmp_prep_time
    print "BM prep:", bm_prep_time
    
    for seq_len in SEQ_LENS:
        print "\tDlugosc sekwencji:", seq_len
        seq = generateSequence(seq_len)
        
        output_seq = open(os.path.join(output_path, "KMP_BM_SEQUENCES", str(seq_len) + ".txt"), "w")
        output_seq.write("%s\n" % seq)
        output_seq.close()
        
        print "\t\tKMP:\t",
        ts_kmp = time.time()
        kmp_algo.compute(seq)
        te_kmp = time.time()
        print (te_kmp - ts_kmp)
        
        print "\t\tBM:\t",
        ts_bm = time.time()
        bm_algo.compute(seq)
        te_bm = time.time()
        print (te_bm - ts_bm)
        
        output_file.write('%r,%r,%f,%f\n' % (len(default_pattern), len(seq), (te_kmp - ts_kmp), (te_bm - ts_bm)))

    output_file.close()
    
    # W ZALEZNOSCI OD SEKWENCJI WZORCOWEJ
    print "Porownanie algorytmow KMP oraz BM w zaleznosci od dlugosci sekwencji wzorcowej..."
    
    output_file = open(os.path.join(output_path, "compare_kmp_bm_pat_len.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,KMP_TIME,KMP_PREP_TIME,BM_TIME,BM_PREP_TIME\n')
    
    for pat_len in PATTERN_LENS:
        print "\tDlugosc wzorca:", pat_len
        pattern = generateSequence(pat_len)
        
        print "\t\t\tKMP..."
        ts_kmp = time.time()
        kmp_prep_time = kmp(pattern, default_seq, output_file)
        te_kmp = time.time()
        
        print "\t\t\tBM..."
        ts_bm = time.time()
        bm_prep_time = bm(pattern, default_seq, output_file)
        te_bm = time.time()
        
        print "\t\tKMP:", (te_kmp - ts_kmp), "(", kmp_prep_time, ");\t\tBM:", (te_bm - ts_bm), "(", bm_prep_time, ")"
        
        output_file.write('%r,%r,%f,%f,%f,%f\n' % (len(pattern), len(default_seq), (te_kmp - ts_kmp), kmp_prep_time, (te_bm - ts_bm), bm_prep_time))
        
    output_file.close()
    
    # W ZALEZNOSCI OD SEKWENCJI
    print "Porownanie algorytmow KMP oraz BM w zaleznosci od dlugosci sekwencji przeszukiwanej..."
    
    output_file = open(os.path.join(output_path, "compare_kmp_bm_seq_len.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,KMP_TIME,BM_TIME\n')
    
    for seq_len in SEQ_LENS:
        print "\tDlugosc sekwencji:", seq_len
        seq = generateSequence(seq_len)
        
        ts_kmp = time.time()
        kmp(default_pattern, seq, output_file)
        te_kmp = time.time()
        
        ts_bm = time.time()
        bm(default_pattern, seq, output_file)
        te_bm = time.time()
        
        output_file.write('%r,%r,%f,%f\n' % (len(default_pattern), len(seq), (te_kmp - ts_kmp), (te_bm - ts_bm)))

if __name__ == '__main__':
    compareTest()