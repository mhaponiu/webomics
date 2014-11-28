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

DEF_PATTERN_LEN = 20
DEF_SEQ_LEN     = 5000

DEF_W           = 11
DEF_T           = 0.001
DEF_C           = 5
DEF_CUT_OFF     = 10

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

def blastStart(pattern, seqs, w, t, c, cut_off):
    blast = calc.Blast(w, t, c)
    
    res = blast.prepare(str(pattern))
    if res == 0:
        print "Parametr W (= " + str(w) + ") powinien byc nie wiekszy od dlugosci zadanej sekwencji (= " + str(len(pattern)) + ")."
        return -1
        
    for seq in seqs:
        blast.addSequence("-1", seq)
        
    res = blast.search()
    if res == 0:
        print "Zbyt wysoka wartosc parametru W (= " + str(w) + "). Nie mozna odnalezc zadnego fragmentu poszukiwanej sekwecji."
        return -2
    
    res = blast.estimate()
    if res == 0:
        print "Zbyt wysoka wartosc parametru T (= " + str(t) + "). Powinien zawierac sie w zakresie od " + str(blast.getMinRate()) + " do " + str(blast.getMaxRate()) + ", srednia wartosc rate wynosi " + str(blast.getAvgRate())
        return -3
    
    res = blast.extend()
    
    aligns = blast.getAligns(cut_off)
    
    return aligns

def blastPatternLen():
    
    print "Badania algorytmu BLAST w zaleznosci od dlugosci sekwencji wzorcowej..."
    
    output_file = open(os.path.join(output_path, "blast_pattern_len.csv"), "w")
    output_file.write('PATTERN_LEN,AVG_SEQS_LEN,W,T,C,SCORE,SAME,GAPS,ALIGN_LEN,TIME\n')
    
    
    output_file.close()

def blastSeqsLen():
    
    print "Badania algorytmu BLAST w zaleznosci od sredniej dlugosci sekwencji..."
    
    output_file = open(os.path.join(output_path, "blast_seqs_len.csv"), "w")
    output_file.write('PATTERN_LEN,AVG_SEQS_LEN,W,T,C,SCORE,SAME,GAPS,ALIGN_LEN,TIME\n')
    
    
    output_file.close()

def blastParams():
    error_rets = [-1, -2, -3]
    
    PATTERN = generateSequence(DEF_PATTERN_LEN)
    DATABASE = generateDatabase(PATTERN, DEF_SEQ_LEN, 1000, 0.05)
    
    w_range = range(5, 25, 1)
    t_range = [i / 1000.0 for i in range(1, 50, 1)]
    c_range = range(2, 20, 1)
    
    output_file = open(os.path.join(output_path, "blast_params.csv"), "w")
    output_file.write('W,T,C,SCORE,SAME,GAPS,ALIGN_LEN,TIME\n')
    
    print "Badania algorytmu BLAST w zaleznosci od parametru W..."
    output_file.write('PARAMETR,W,,,,,,\n')
    for W in w_range:
        ts = time.time()
        blast_ret = blastStart(PATTERN, DATABASE, W, DEF_T, DEF_C, DEF_CUT_OFF)
        te = time.time()
        if blast_ret not in error_rets:
            if len(blast_ret) > 0:
                blast_ret = blast_ret[0]
                output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (W, DEF_T, DEF_C, 
                                                           blast_ret.getScore(),
                                                           blast_ret.getSame(),
                                                           blast_ret.getGaps(),
                                                           blast_ret.getAlignLength(),
                                                           te - ts))
            else:
                output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (W, DEF_T, DEF_C, 
                                                           -4,
                                                           -4,
                                                           -4,
                                                           -4,
                                                           te - ts))
        else:
            output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (W, DEF_T, DEF_C, 
                                                           blast_ret,
                                                           blast_ret,
                                                           blast_ret,
                                                           blast_ret,
                                                           te - ts))
    
    print "Badania algorytmu BLAST w zaleznosci od parametru T..."
    output_file.write('PARAMETR,T,,,,,,\n')
    for T in t_range:
        ts = time.time()
        blast_ret = blastStart(PATTERN, DATABASE, DEF_W, T, DEF_C, DEF_CUT_OFF)
        te = time.time()
        if blast_ret not in error_rets:
            if len(blast_ret) > 0:
                blast_ret = blast_ret[0]
                output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (DEF_W, T, DEF_C, 
                                                           blast_ret.getScore(),
                                                           blast_ret.getSame(),
                                                           blast_ret.getGaps(),
                                                           blast_ret.getAlignLength(),
                                                           te - ts))
            else:
                output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (DEF_W, T, DEF_C, 
                                                           -4,
                                                           -4,
                                                           -4,
                                                           -4,
                                                           te - ts))
        else:
            output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (DEF_W, T, DEF_C, 
                                                           blast_ret,
                                                           blast_ret,
                                                           blast_ret,
                                                           blast_ret,
                                                           te - ts))
    
    print "Badania algorytmu BLAST w zaleznosci od parametru C..."
    output_file.write('PARAMETR,C,,,,,,\n')
    for C in c_range:
        ts = time.time()
        blast_ret = blastStart(PATTERN, DATABASE, DEF_W, DEF_T, C, DEF_CUT_OFF)
        te = time.time()
        if blast_ret not in error_rets:
            if len(blast_ret) > 0:
                blast_ret = blast_ret[0]
                output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (DEF_W, DEF_T, C, 
                                                           blast_ret.getScore(),
                                                           blast_ret.getSame(),
                                                           blast_ret.getGaps(),
                                                           blast_ret.getAlignLength(),
                                                           te - ts))
            else:
                output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (DEF_W, DEF_T, C, 
                                                           -4,
                                                           -4,
                                                           -4,
                                                           -4,
                                                           te - ts))
        else:
            output_file.write("%d,%f,%d,%d,%d,%d,%d,%f\n" % (DEF_W, DEF_T, C, 
                                                           blast_ret,
                                                           blast_ret,
                                                           blast_ret,
                                                           blast_ret,
                                                           te - ts))

    output_file.close()
    

if __name__ == '__main__':
    blastParams()
    #blastPatternLen()
    #blastSeqsLen()