import sys, os

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.utils.intervalTree import IntervalTree, Interval

## Klasa dziedziczaca po IntervalTree
class MarkerIntervalTree(IntervalTree):
    pass

## Klasa dziedziczaca po Interval
class MarkerInterval(Interval):
    def __init__(self, marker_name, start, stop, order):
        Interval.__init__(self, start, stop)
        self.marker_name = marker_name
        self.order = order

    def __unicode__(self):
        return str(self.marker_name) + "; " + str(self.start) + "; " + str(self.stop) + " --> " + str(self.order)

    def __str__(self):
        return str(self.marker_name) + "; " + str(self.start) + "; " + str(self.stop) + " --> " + str(self.order)
