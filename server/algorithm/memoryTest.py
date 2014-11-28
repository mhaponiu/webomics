import sys, os

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

calc_path = os.path.join( this_module_path, '..', '..', 'calculation', 'build')
sys.path.append(calc_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

# Biblioteka obliczeniowa
import calc

# Dostep do bazy danych
from server.scaffold.models import Scaffold
from server.scaffold.models import UndefinedScaffold

from server.contig.models import Contig

@profile
def search(text):
    pattern = str(text)
    
    print "Pobieram dane z bazdy danych..."
    
    objects = []
    
    # ----------------- SCAFFOLDY ------------------
    scaffs = Scaffold.objects.all()
    # --------- NIEZIDENTYFIKOWANE SCAFFOLDY -------
    udef_scaffs = UndefinedScaffold.objects.all()
    
    # ------------------ CONTIGI -------------------
    conts = Contig.objects.all()
    
    objects.extend(scaffs)
    objects.extend(udef_scaffs)
    objects.extend(conts)
    
    print "Rozpoczynam przeszukiwanie sekwencji..."
    
    text = ""
    
    #for obj in objects[:10]:
    text = str(objects[0].sequence)
    
    print "LEN:", len(text)
    
    # Tworzymy obiekt algorytmu
    sw = calc.SW(2, -1, -1, -1)
     
    # Uruchomienie algorytmu
    max_value = sw.compute(text, pattern)
    
    print "MAX:", max_value
    
if __name__ == '__main__':
    search("GCAAACCGGUUUGGCCAAGGCAAC")