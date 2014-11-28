import sys
import os

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.scaffold.models import Scaffold
from server.scaffold.models import UndefinedScaffold
from server.contig.models import Contig


#scaffs = Scaffold.objects.all()
#print "Ilosc scaffoldow:", len(scaffs)
#
#max_seq_len = 0
#
#for scaff in scaffs:
#    if scaff.length_bp > max_seq_len:
#        max_seq_len = scaff.length_bp
#
#print "Max dlugosc:", max_seq_len

#udef_scaffs = UndefinedScaffold.objects.all()
#print "Ilosc niezdef. scaffoldow:", len(udef_scaffs)

import pickle

scaffolds = Scaffold.objects.all()
contigs = Contig.objects.all()

scaffs = {}
conts = {}

print "Scaffolds..."

for s in scaffolds:
    try:
        scaffs[int(s.id)] = str(s.sequence)
    except ValueError:
        print "Bledne ID scaffolda!"
        continue
    
print "Contigs..."
    
for c in contigs:
    try:
        conts[int(c.id)] = (int(c.scaff_id), str(c.sequence))
    except ValueError:
        print "Bledne ID contiga!"
        continue

pickle.dump(scaffs, open("mbi_scaffs.pickle", "wb"))
pickle.dump(conts, open("mbi_conts.pickle", "wb"))