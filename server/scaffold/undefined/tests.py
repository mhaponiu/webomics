import os, sys

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

'''from interf import buildScaffoldTree, getScaffoldsFromTree

buildScaffoldTree(1)
from_ = 0.0
to_ = 22.0
scaffs = getScaffoldsFromTree(1, from_, to_)
print "Przedzial: (", from_, ", ", to_, ")"
for scaff in scaffs:
    print scaff
'''

'''from server.scaffold.models import Scaffold, ScaffoldPosition

scaffs = Scaffold.objects.filter(chromosome_id = 1, assemb_type = 1)
scaffolds = []
for scaff in scaffs:
    poss = ScaffoldPosition.objects.filter(scaff_id = scaff.id)
    for pos in poss:
        scaffolds.append(pos)
scaffolds.sort(key = lambda x: x.order, reverse = False)
print scaffolds'''

from server.scaffold.models import UndefinedScaffold
from server.scaffold.undefined.interf import getScaffolds, getMaxID, getMinID
from server.config import static

max_id = getMaxID(static.CELERA)
print "MAX:", max_id
min_id = getMinID(static.CELERA)
print "MIN:", min_id
scaffs = getScaffolds(static.CELERA, 356596, 356600)
print "\n\n"

for scaff in scaffs:
    print "\t", scaff
