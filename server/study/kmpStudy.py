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
    ts = time.time()
    
    kmp = calc.KMP()
    
    ts_tab = time.time()
    table_status = kmp.calculateTable(pattern)
    te_tab = time.time()
    
    positions = kmp.compute(sequence)
    
    te = time.time()

    output_file.write('%r,%r,%f,%f\n' % (len(pattern), len(sequence), te - ts, te_tab - ts_tab))


def kmpTest():
    PATTERN_LENS = range(500000, 100000000, 500000) # od 500 000 do 100 000 000 co 500 000
    SEQ_LENS = range(500000, 1000000000, 500000) # od 500 000 do 1 000 000 000 co 500 000
    
    # Sekwencje domyslne
    default_pattern = generateSequence(10000)   # 10 000
    default_seq = generateSequence(100000000)  # 100 000 000
    
    # W ZALEZNOSCI OD SEKWENCJI WZORCOWEJ
    print "Badania algorytmu KMP w zaleznosci od dlugosci sekwencji wzorcowej..."
    
    output_file = open(os.path.join(output_path, "kmp_pat_len.csv"), "w")
    
    for pat_len in PATTERN_LENS:
        print "\tDlugosc wzorca:", pat_len
        pattern = generateSequence(pat_len)
        kmp(pattern, default_seq, output_file)
        
    output_file.close()
    
    # W ZALEZNOSCI OD SEKWENCJI
    print "Badania algorytmu KMP w zaleznosci od dlugosci sekwencji przeszukiwanej..."
    
    output_file = open(os.path.join(output_path, "kmp_seq_len.csv"), "w")
    
    for seq_len in SEQ_LENS:
        print "\tDlugosc sekwencji:", seq_len
        seq = generateSequence(seq_len)
        kmp(default_pattern, seq, output_file)

    output_file.close()

if __name__ == '__main__':
    kmpTest()