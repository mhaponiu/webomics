import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

from pyamf.remoting.client import RemotingService
import os, sys

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.config import static

url = 'http://127.0.0.1:8000/gateway/'
gw = RemotingService(url, logger = logging)

pattern = "GCAAACCGGUUUGGCCAAGGCAAC"

#service = gw.getService('main.echo')
#print service()

#service = gw.getService('algorithm._runBLAST')
#res = service(pattern, 11, 0.5, 5, 5, "A")

#print res

service = gw.getService('algorithm._runBLAST_SW')
res = service(pattern, 11, 0.5, 5, 5, "C")

print res

#service = gw.getService('algorithm._searchSW')
#res = service(pattern)
#
#scaffs = res[0]
#max_scaff = scaffs[0] #(max_value, max_id)
#
#print "Max wartosc dla scaffoldu o ID:", max_scaff[1], "wynosi:", max_scaff[0]
#
#service = gw.getService('algorithm.getTextsResultSW')
#res = service(pattern, max_scaff[1], static.SCAFFOLDS)
#
#print "Zas getTextsResultSW() mowi ze wynosi ona:", res


#service = gw.getService('algorithm.getTextsResultSW')
#res = service(pattern, "360259", static.SCAFFOLDS)
#
#print "Zas getTextsResultSW() mowi ze wynosi ona:", res




#service = gw.getService('algorithm.findKMP')
#service("ACAATGAGTTGGTCAGA")
#
#service = gw.getService('algorithm.getTextResultKMP')
#service("10785;42", "ACAATGAGTTGGTCAGA")

