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

DEF_MATCH       = 2
DEF_MISMATCH    = -1 
DEF_GAP_OPEN    = -3
DEF_GAP_EXTEND  = -1

def generateSequence(nucleotides_count):
    return (random.choice(NUCLEOTIDES)) * nucleotides_count

def swStart(output_file, pattern, seq, match, mismatch, gap_open, gap_extend):
    ts = time.time()
    sw = calc.SW()
    
    max_value = sw.fastInitAndCompute(match, mismatch, gap_open, gap_extend, seq, pattern)
    print "\t\tMAX_VALUE =", max_value
    
    te = time.time()
    
    output_file.write('%r,%r,%r,%r,%r,%r,%r,%f\n' % (len(pattern), len(seq), match, mismatch, gap_open, gap_extend, max_value, te - ts))
    
    
def swPatternLen():
    SEQ     = generateSequence(100000)  # 100 000   nukleotydow
    PATTERNS = []
    pattern_len_range = range(100, 1000, 100)
    for len_cut in pattern_len_range:
        pattern = SEQ[50000:(50000 + len_cut)]
        # Zmiana 10 losowych nukleotydow z sekwencji wzorcowej
        for _ in range(10):
            pos = random.randint(0, len(pattern) - 1)
            pattern = pattern[:pos] + random.choice(NUCLEOTIDES.replace(pattern[pos], "")) + pattern[pos + 1 :]
    
        PATTERNS.append(pattern)

    print "Badania algorytmu SW w zaleznosci od dlugosci sekwencji wzorcowej..."

    output_file = open(os.path.join(output_path, "sw_pattern_len.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,MATCH,MISMATCH,GAP_OPEN,GAP_EXTEND,MAX_VALUE,TIME\n')
    
    for PATTERN in PATTERNS:
        print "\tPATTERN_LEN =", len(PATTERN)
        swStart(output_file, PATTERN, SEQ, DEF_MATCH, DEF_MISMATCH, DEF_GAP_OPEN, DEF_GAP_EXTEND)
    
    output_file.close()

def swSeqLen():
    output_file = open(os.path.join(output_path, "sw_seq_len.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,MATCH,MISMATCH,GAP_OPEN,GAP_EXTEND,MAX_VALUE,TIME\n')
    
    print "Badania algorytmu SW w zaleznosci od dlugosci sekwencji..."
    
    PATTERN = generateSequence(100)
    seqs_range = range(100000, 1000000, 100000)

    for seq_len in seqs_range:
        print "\tSEQ_LEN =", seq_len
        SEQ = generateSequence(seq_len)
        swStart(output_file, PATTERN, SEQ, DEF_MATCH, DEF_MISMATCH, DEF_GAP_OPEN, DEF_GAP_EXTEND)
    
    output_file.close()

# Parametry do zbadania:
# - match
# - mismatch
# - gap_open
# - gap_extend
def swParams():
    SEQ     = generateSequence(1000000)  # 1 000 000   nukleotydow
    PATTERN = SEQ[50000:50100]
    # Zmiana 10 losowych nukleotydow z sekwencji wzorcowej
    for _ in range(10):
        pos = random.randint(0, len(PATTERN) - 1)
        PATTERN = PATTERN[:pos] + random.choice(NUCLEOTIDES.replace(PATTERN[pos], "")) + PATTERN[pos + 1 :]
    
    output_file = open(os.path.join(output_path, "sw_params.csv"), "w")
    output_file.write('PATTERN_LEN,SEQ_LEN,MATCH,MISMATCH,GAP_OPEN,GAP_EXTEND,MAX_VALUE,TIME\n')
    
    print "Badania algorytmu SW w zaleznosci od parametru MATCH..."
    output_file.write('PARAMETR,MATCH,,,,,,\n')
    # - match
    match_range = range(1, 11)
    for m in match_range:
        print "\tMATCH =", m
        swStart(output_file, PATTERN, SEQ, m, DEF_MISMATCH, DEF_GAP_OPEN, DEF_GAP_EXTEND)
    
    print "Badania algorytmu SW w zaleznosci od parametru MISMATCH..."
    output_file.write(',\n')
    output_file.write('PARAMETR,MISMATCH,,,,,,\n')
    # - mismatch
    mis_match_range = range(1, 11)
    for mm in mis_match_range:
        print "\tMISMATCH =", -mm
        swStart(output_file, PATTERN, SEQ, DEF_MATCH, -mm, DEF_GAP_OPEN, DEF_GAP_EXTEND)
    
    print "Badania algorytmu SW w zaleznosci od parametru GAP OPEN..."
    output_file.write(',\n')
    output_file.write('PARAMETR,GAP_OPEN,,,,,,\n')
    # - gap_open
    gap_open_range = range(1, 11)
    for go in gap_open_range:
        print "\tGAP_OPEN =", -go
        swStart(output_file, PATTERN, SEQ, DEF_MATCH, DEF_MISMATCH, -go, DEF_GAP_EXTEND)
    
    print "Badania algorytmu SW w zaleznosci od parametru GAP EXTEND..."
    output_file.write(',\n')
    output_file.write('PARAMETR,GAP_EXTEND,,,,,,\n')
    # - gap_extend
    gap_extend_range = range(0, 11)
    for ge in gap_extend_range:
        print "\tGAP_EXTEND =", -ge
        swStart(output_file, PATTERN, SEQ, DEF_MATCH, DEF_MISMATCH, DEF_GAP_OPEN, -ge)

    output_file.close()

if __name__ == '__main__':
    #swParams()
    #swPatternLen()
    swSeqLen()