import sys, os
import time

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

calc_path = os.path.join( this_module_path, '..', '..', 'calculation', 'build')
sys.path.append(calc_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

# Biblioteka obliczeniowa
import memo

# Dostep do bazy danych
from server.scaffold.models import Scaffold

@profile
def check():
    print "\n---- ROZPOCZYNAM ----\n"
    # ----------------- SCAFFOLDY ------------------
    scaffs = Scaffold.objects.all()
    
    seq = str(scaffs[0].sequence)
    patt = "G"*500
    
    print "Dlugosc wzorca:\t", len(patt)
    print "Dlugosc sekwencji:\t", len(seq), "\n"
    
    # MATRIX
    start = time.time()
    memo.matrix(seq, patt)
    stop = time.time()
    
    print "Matrix czas:", stop - start, "\n"
    
    # VECTORS
    start = time.time()
    memo.vectors(seq, patt)
    stop = time.time()
    
    print "Vectors czas:", stop - start, "\n"
    
    # MALLOC
    start = time.time()
    memo.heap(seq, patt)
    stop = time.time()
    
    print "Malloc czas:", stop - start, "\n"
    
    print "\n---- ZAKONCZYLEM ----\n"

@profile
def liveMemTest():
    print "\nPobiera dane z bazy danych..."
    scaffs = Scaffold.objects.values('id', 'sequence')
    print "Dane pobrane poprawnie."
    
    pattern = "GCAAACCGGUUUGGCCAAGGCAAC"
    
    for obj in scaffs[:10]:
        print "\t", obj['id'], "\t", len(str(obj['sequence']))
        # Uruchomienie funkcji testujacej
        memo.liveMatrix(str(obj['sequence']), str(pattern))
    
if __name__ == '__main__':
    liveMemTest()