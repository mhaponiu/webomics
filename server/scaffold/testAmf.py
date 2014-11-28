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

#service = gw.getService('scaffold.buildTree')
#service(2)

#service = gw.getService('scaffold.getFromTree')
#service()

#service = gw.getService('scaffold.getScaffoldPosition')
#service("10785")

service = gw.getService('scaffold.getScaffold')
service("10785")