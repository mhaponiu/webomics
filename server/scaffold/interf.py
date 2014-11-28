from server.scaffold.models import Scaffold, ScaffoldPosition, ScaffoldWrap
from server.contig.models import Contig
from server.config import static
import random

from server.scaffold.scaffoldIntervals import ScaffoldInterval, ScaffoldIntervalTree
from server.database.colors import COLORS

from server.utils import log as LOG

colors = {}

class TreeObject:
    interval_tree = None

    def getInstance(self):
        return self.interval_tree

def buildScaffoldTree(chr_id):
    LOG.INFO("[C" + str(chr_id) + "] Rozpoczynam budowe drzewa przedzialowego...")
    scaffolds = Scaffold.objects.all().filter(chromosome_id = int(chr_id))
    LOG.DEBUG("[C" + str(chr_id) + "] Scaffoldow na Chromosomie " + str(chr_id) + ": " + str(len(scaffolds)))
    scaffolds_to_tree = []
    for scaffold in scaffolds:
        scaffolds_positions = ScaffoldPosition.objects.all().filter(scaff_id = scaffold.id)
        for scaffolds_position in scaffolds_positions:
            scaffold_interval = ScaffoldInterval(scaffold.id, scaffold.chromosome_id, scaffold.assemb_type, scaffolds_position.start, scaffolds_position.end, scaffolds_position.order)
            scaffolds_to_tree.append(scaffold_interval)
    print "Scaffs:", len(scaffolds_to_tree)
    if len(scaffolds_to_tree) != 0:
        # Zapamietanie obiektu drzewa przedzialowego
        TreeObject.interval_tree = ScaffoldIntervalTree(scaffolds_to_tree)
        LOG.INFO("[C" + str(chr_id) + "] Zakonczylam budowe drzewa przedzialowego...")
        return 1
    else:
        LOG.INFO("Nie znaleziono scaffoldow dla chromosomu o ID:" + str(chr_id))
        return 0

def getScaffoldsFromTree(shown_types, start, stop):
    global colors
    scaffolds_return = []
    if TreeObject.interval_tree == None:
        LOG.WARN("Blad drzewa przedzialowego. Nie istnieje!")
        return scaffolds_return
    LOG.INFO("Rozpoczynam poszukiwanie scaffoldow w drzewie. Typy: " + str(shown_types) + ". Od " + str(start) + " do " + str(stop))
    scaffolds_result = TreeObject.interval_tree.find(start, stop)
    i = 0
    for scaffold in scaffolds_result:
        try:
            # Obiekt scaffoldu
            scaff = Scaffold.objects.all().get(id = scaffold.scaffold_id)
        except Scaffold.DoesNotExist:
            LOG.WARN("Brak scaffoldu o ID: " + str(scaffold.scaffold_id))
            continue
        # Filtrujemy po typie asemblacji
        if scaff.assemb_type in shown_types:
            # Wylosowany kolor
            if colors.has_key(scaffold.scaffold_id):
                color = colors[scaffold.scaffold_id]
            else:
                #color = random.choice(COLORS)
                x = random.randint(0, 16777215)
                color = hex(x).replace("0x", "#")
                colors[scaffold.scaffold_id] = color
            # Dla kazdej pozycji tworzymy obiekt wrappera scaffoldu - wyswietlanego elementu
            scaffold_wrap = ScaffoldWrap(i,
                                         scaffold.scaffold_id,
                                         scaff.chromosome_id,
                                         scaff.sequence,
                                         scaff.assemb_type,
                                         scaffold.start,
                                         scaffold.stop,
                                         color,
                                         scaffold.order,
                                         scaff.length_bp)
            scaffolds_return.append(scaffold_wrap)
            i += 1
    scaffolds_return.sort(key = lambda x: x.length_bp, reverse = False)
    scaffolds_return.sort(key = lambda x: x.start, reverse = False)
    LOG.DEBUG("Wynik poszukiwan (T:" + str(shown_types) + " - " + str(start) + " - " + str(stop) + "):\n" + str(scaffolds_return))
    LOG.INFO("Zakonczylem przeszukiwanie scaffoldow w drzewie.")
    return scaffolds_return

def getScaffoldsCount(chr_id):
    return Scaffold.objects.filter(chromosome_id=int(chr_id)).count()

## Funkcja zwraca ID chromosomu, na ktorym lezy dany scaffold
#  @param scaff_id: ID scaffoldu, dla ktorego ID chromosomu poszukujemy
#  @return: ID chhromosomu, na ktorym lezy szukany scaffold
def getChromosomeID(scaff_id):
    LOG.INFO("Rozpoczynam pobieranie ID chromosomu, na ktorym znajduje sie scaffold o ID: " + str(scaff_id))
    try:
        scaffold = Scaffold.objects.get(id = str(scaff_id))
    except Scaffold.DoesNotExist:
        LOG.WARN("Brak scaffoldu o ID: " + str(scaffold.scaffold_id))
        return None
    LOG.INFO("Zakonczylem pobieranie ID chromosomu.")
    return scaffold.chromosome_id

##
#TODO: Funkcja powinna zwracac wszystkie pozycje, a nie tylko jedna...
def getScaffoldPosition(scaff_id):
    LOG.INFO("Rozpoczynam poszukiwanie pozycji start dla scaffoldu: " + str(scaff_id))
    scaffold = ScaffoldPosition.objects.filter(scaff_id = str(scaff_id))
    try:
        pos_start = scaffold[0].start
    except IndexError:
        LOG.WARN("Scaffold o ID: " + str(scaff_id) + " nie ma pozycji start.")
        return None
    LOG.DEBUG("Pozycja start dla scaffoldu: " + str(scaff_id) + " to: " + str(pos_start))
    LOG.INFO("Zakonczylem poszukiwanie pozycji start dla scaffoldu:" + str(scaff_id))
    return pos_start

##
def getScaffold(scaff_id):
    LOG.INFO("Rozpoczynam pobieranie scaffoldu o ID: " + str(scaff_id))
    try:
        scaff = Scaffold.objects.get(id = str(scaff_id))
    except Scaffold.DoesNotExist:
        LOG.WARN("Brak scaffoldu o ID: " + str(scaff_id))
        return None
    #TODO: Istnieje przeciez kilka pozycji danego scaffoldu! Bez sensu jest zwracac tylko jedna
    try:
        scaff_pos = ScaffoldPosition.objects.filter(scaff_id = str(scaff_id))[0] 
    except IndexError:
        LOG.WARN("Scaffold o ID: " + str(scaff_id) + " nie posiada zadnych pozycji.")
        return None
    scaffold_wrap = ScaffoldWrap(scaff.id,
                             scaff.id,
                             scaff.chromosome_id,
                             scaff.sequence,
                             scaff.assemb_type,
                             scaff_pos.start,
                             scaff_pos.end,
                             None,
                             scaff_pos.order,
                             scaff.length_bp)
    LOG.INFO("Zakonczylem pobieranie scaffoldu o ID: " + str(scaff_id))
    return scaffold_wrap

def deleteScaffold(scaff_id, with_contigs=False):
    LOG.INFO("Rozpoczynam usuwanie scaffoldu o ID: " + str(scaff_id))
    try:
        s = Scaffold.objects.get(id = str(scaff_id))
    except Scaffold.DoesNotExist:
        LOG.WARN("Brak scaffoldu o ID: " + str(scaff_id))
        return None
    s.delete()
    
    LOG.DEBUG("Usuwam wszystkie pozycje scaffoldu ze scaffoldu: " + str(scaff_id))
    # Usuniecie scaffold positions
    try:
        Scaffold.objects.filter(scaff_id = str(scaff_id)).delete()
    except Exception:
        LOG.DEBUG("Brak pozycji scaffoldu: " + str(scaff_id))
    
    if with_contigs == True:
        LOG.DEBUG("Usuwam wszystkie contigi nalezace do scaffoldu: " + str(scaff_id))
        # Usuniecie contigow
        try:
            Contig.objects.filter(scaff_id = str(scaff_id)).delete()
        except Exception:
            LOG.DEBUG("Brak contigow na scaffoldzie: " + str(scaff_id))
    
    #TODO: Sprawdzenie czy przez to nie zmniejszyla sie laczna dlugosc chromosomu
    
    LOG.INFO("Zakonczylem usuwanie scaffoldu o ID: " + str(scaff_id))
    return True