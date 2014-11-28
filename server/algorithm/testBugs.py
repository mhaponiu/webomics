import os, sys

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

from server.config import static

pattern = "GCAAACCGGUUUGGCCAAGGCAACA"   # 25 znakow

scaff = Scaffold.objects.get(id = "360274") # 1 192 788 znakow

sw = calc.SW()

#   100 000
k = 100000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   200 000
k = 200000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   300 000
k = 300000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   400 000
k = 400000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   500 000
k = 500000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   600 000
k = 600000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   700 000
k = 700000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   800 000
k = 800000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
#   900 000
k = 900000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)
# 1 000 000
k = 1000000
print k
sw.fastComputeWithStringsResult(2, -1, -3, -1, str(scaff.sequence)[:k], pattern)