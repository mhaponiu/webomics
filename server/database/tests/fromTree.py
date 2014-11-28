import os, sys
import time
import datetime
import logging
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

from pyamf.remoting.client import RemotingService

url = 'http://127.0.0.1:8000/gateway/'
gw = RemotingService(url, logger = logging)

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.config import static

# Testowanie czasu wyszukiwania i pobierania danych z drzewa przedzialow
service = gw.getService('scaffold.buildTree')
service(3)

intervals_file = open("../utils/example_intervals_chr_3.csv", "r")
intervals_lines = intervals_file.readlines()
intervals = []
for inter in intervals_lines:
    start, stop = inter.strip("\n").split("\t")
    intervals.append((start, stop))
intervals_file.close()

# Wszystkie dane testowe odczytane
service = gw.getService('scaffold.getFromTree')
#print service(3, static.ALL_ASSEM, 0, 100000)
time_start = time.time()
for frame in intervals:
    service(3, static.ALL_ASSEM, int(frame[0]), int(frame[1]))
time_stop = time.time()

directly_result = open("tree_results.txt", "a")
directly_result.write(str(datetime.datetime.now()) + "\t\t" + str(time_stop - time_start) + "\t\t" + str(len(intervals_lines)) + "\n")
directly_result.close()
