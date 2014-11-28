import sys, os

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.utils.intervalTree import IntervalTree, Interval

## Klasa dziedziczaca po IntervalTree
class ScaffoldIntervalTree(IntervalTree):
    pass

## Klasa dziedziczaca po Interval
class ScaffoldInterval(Interval):
    def __init__(self, scaffold_id, chromosome_id, assemb_type, start, stop, order):
        Interval.__init__(self, start, stop)
        self.scaffold_id = scaffold_id
        self.chromosome_id = chromosome_id
        self.assemb_type = assemb_type
        self.order = order

    def __unicode__(self):
        return str(self.scaffold_id) + "; " + str(self.chromosome_id) + "; " + str(self.assemb_type) + "; " + str(self.start) + "; " + str(self.stop) + " --> " + str(self.order)

    def __str__(self):
        return str(self.scaffold_id) + "; " + str(self.chromosome_id) + "; " + str(self.assemb_type) + "; " + str(self.start) + "; " + str(self.stop) + " --> " + str(self.order)
