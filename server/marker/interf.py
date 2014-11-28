from server.marker.models import Marker, MarkerWrap
from server.marker.markerIntervals import MarkerInterval, MarkerIntervalTree

from server.utils import log as LOG

# 360274 --> 347750

############################## SCAFFOLD ###############################

class MarkersScaffoldTreeObject:
    interval_tree = None
    
    def getInstance(self):
        return self.interval_tree

def buildMarkerScaffoldTree(scaff_id):
    LOG.INFO("Rozpoczynam budowanie drzewa przedzialowego markerow dla scaffoldu o ID:" + str(scaff_id))
    markers = Marker.objects.all().filter(scaff_id = str(scaff_id))
    LOG.DEBUG("Ilosc markerow na scaffoldzie o ID: " + str(scaff_id) + " wynosi: " + str(len(markers)))
    markers_to_tree = []
    for marker in markers:
        marker_interval = MarkerInterval(marker.name, marker.scaffold_start, marker.scaffold_end, -1)
        markers_to_tree.append(marker_interval)

    if len(markers) != 0:
        # Zapamietanie obiektu drzewa przedzialowego
        MarkersScaffoldTreeObject.interval_tree = MarkerIntervalTree(markers_to_tree)
        LOG.INFO("Zakonczylem budowanie drzewa przedzialowego markerow dla scaffoldu o ID:" + str(scaff_id))
        return 1
    else:
        LOG.INFO("Nie znaleziono markerow dla scaffoldu o ID:" + str(scaff_id))
        return 0

def getMarkerFromScaffoldTree(start, stop):
    LOG.INFO("Rozpoczynam poszukiwanie markerow w drzewie (s). Od " + str(start) + " do " + str(stop))
    markers_return = []
    LOG.DEBUG("Drzewo markerow (s): " + str(MarkersScaffoldTreeObject.interval_tree))
    if MarkersScaffoldTreeObject.interval_tree == None:
        LOG.DEBUG("Drzewo markerow nie zostalo zbudowane!")
        return None
    markers_result = MarkersScaffoldTreeObject.interval_tree.find(start, stop)
    i = 0
    for marker in markers_result:
        # Obiekt markera
        try:
            mar = Marker.objects.all().get(name = marker.marker_name)
        except Marker.DoesNotExist:
            LOG.WARN("Brak contigu o ID: " + str(marker.marker_name))
            return None
        markers_return.append(mar)
        i += 1
        
    markers_return.sort(key = lambda x: x.scaff_id, reverse = False)
    markers_return.sort(key = lambda x: x.scaffold_start, reverse = False)

    LOG.DEBUG("Wynik poszukiwan markerow (" + str(start) + " - " + str(stop) + "):\n" + str(markers_return))
    LOG.INFO("Zakonczylem przeszukiwanie markerow w drzewie.")
    
    return markers_return

def getMarkersOnScaffold(scaff_id):
    LOG.INFO("Rozpoczynam pobieranie markerow ze scaffoldu o ID: " + str(scaff_id))
    markers = Marker.objects.all().filter(scaff_id = str(scaff_id))
    LOG.DEBUG("Ilosc markerow na scaffoldzie o ID: " + str(scaff_id) + " wynosi " + str(len(markers)))
    
    marks_return = []
    
    for mark in markers:
        try:
            m = Marker.objects.all().get(name = mark.name)
        except Marker.DoesNotExist:
            LOG.WARN("Brak markera o nazwie: " + str(mark.name))
            return None
        #TODO: Tutaj jezeli nie bedzie dzialalo bedzie trzeba zrobic jakiegos Wrapa
        marks_return.append(m)
    
    LOG.INFO("Zakonczylem pobieranie markerow ze scaffoldu o ID: " + str(scaff_id))
    return marks_return

############################### CONTIG ################################

class MarkersContigTreeObject:
    interval_tree = None

    def getInstance(self):
        return self.interval_tree

def buildMarkerContigTree(cont_id):
    LOG.INFO("Rozpoczynam budowanie drzewa przedzialowego markerow dla contigu o ID:" + str(cont_id))
    markers = Marker.objects.all().filter(cont_id = int(cont_id))
    LOG.DEBUG("Ilosc markerow na contigu o ID: " + str(cont_id) + " wynosi: " + str(len(markers)))
    markers_to_tree = []
    for marker in markers:
        marker_interval = MarkerInterval(marker.name, marker.contig_start, marker.contig_end, -1)
        markers_to_tree.append(marker_interval)

    if len(markers) != 0:
        # Zapamietanie obiektu drzewa przedzialowego
        MarkersContigTreeObject.interval_tree = MarkerIntervalTree(markers_to_tree)
        LOG.INFO("Zakonczylem budowanie drzewa przedzialowego markerow dla contigu o ID:" + str(cont_id))
        return 1
    else:
        LOG.INFO("Nie znaleziono markerow dla contigu o ID:" + str(cont_id))
        return 0

def getMarkerFromContigTree(start, stop):
    LOG.INFO("Rozpoczynam poszukiwanie markerow w drzewie (c). Od " + str(start) + " do " + str(stop))
    markers_return = []
    if MarkersContigTreeObject.interval_tree == None:
        LOG.DEBUG("Drzewo markerow nie zostalo zbudowane!")
        return None
    markers_result = MarkersContigTreeObject.interval_tree.find(start, stop)
    i = 0
    for marker in markers_result:
        # Obiekt markera
        try:
            mar = Marker.objects.all().get(name = marker.marker_name)
        except Marker.DoesNotExist:
            LOG.WARN("Brak contigu o ID: " + str(marker.marker_name))
            return None
        markers_return.append(mar)
        i += 1
        
    markers_return.sort(key = lambda x: x.cont_id, reverse = False)
    markers_return.sort(key = lambda x: x.contig_start, reverse = False)

    LOG.DEBUG("Wynik poszukiwan markerow (" + str(start) + " - " + str(stop) + "):\n" + str(markers_return))
    LOG.INFO("Zakonczylem przeszukiwanie markerow w drzewie.")
    
    return markers_return

def getMarkersOnContig(cont_id):
    LOG.INFO("Rozpoczynam pobieranie markerow z contiga o ID: " + str(cont_id))
    markers = Marker.objects.all().filter(contig_id = int(cont_id))
    LOG.DEBUG("Ilosc markerow na contigu o ID: " + str(cont_id) + " wynosi " + str(len(markers)))
    
    marks_return = []
    
    for mark in markers:
        try:
            m = Marker.objects.all().get(name = mark.name)
        except Marker.DoesNotExist:
            LOG.WARN("Brak markera o nazwie: " + str(mark.name))
            return None
        #TODO: Tutaj jezeli nie bedzie dzialalo bedzie trzeba zrobic jakiegos Wrapa
        marks_return.append(m)
    
    LOG.INFO("Zakonczylem pobieranie markerow z contigu o ID: " + str(cont_id))
    return marks_return

def getMarker(marker_name):
    LOG.INFO("Rozpoczynam pobieranie markera o nazwie: " + str(marker_name))
    try:
        m = Marker.objects.all().get(name = str(marker_name))
    except Marker.DoesNotExist:
        LOG.WARN("Brak markera o nazwie: " + str(marker_name))
        return None
    LOG.INFO("Zakonczylem pobieranie markera o nazwie: " + str(marker_name))
    return m

def getMarkersDictOnScaff(scaff_id):
    LOG.INFO("Rozpoczynam pobieranie markerow ze scaffoldu o ID: " + str(scaff_id))
    markers = Marker.objects.all().filter(scaff_id = str(scaff_id))
    LOG.DEBUG("Ilosc markerow na scaffoldzie o ID: " + str(scaff_id) + " wynosi " + str(len(markers)))
    
    marks_return = []
    
    for i, mark in enumerate(markers):
        mark_dict = {}
        mark_dict['LP'] = i + 1
        mark_dict['NAME'] = mark.name
        mark_dict['CHR_ID'] = mark.chr_id
        mark_dict['POS_CM'] = mark.pos_cm
        mark_dict['SCAFF_ID'] = mark.scaff_id
        mark_dict['START_INDEX'] = mark.scaffold_start
        mark_dict['END_INDEX'] = mark.scaffold_end
        marks_return.append(mark_dict)
    
    LOG.INFO("Zakonczylem pobieranie markerow ze scaffoldu o ID: " + str(scaff_id))
    return marks_return

def getMarkersDictOnCont(cont_id):
    LOG.INFO("Rozpoczynam pobieranie markerow z contiga o ID: " + str(cont_id))
    markers = Marker.objects.all().filter(cont_id = int(cont_id))
    LOG.DEBUG("Ilosc markerow na contigu o ID: " + str(cont_id) + " wynosi " + str(len(markers)))
    
    marks_return = []
    
    for i, mark in enumerate(markers):
        mark_dict = {}
        mark_dict['LP'] = i + 1
        mark_dict['NAME'] = mark.name
        mark_dict['CHR_ID'] = mark.chr_id
        mark_dict['POS_CM'] = mark.pos_cm
        mark_dict['CONT_ID'] = mark.cont_id
        mark_dict['START_INDEX'] = mark.contig_start
        mark_dict['END_INDEX'] = mark.contig_end
        marks_return.append(mark_dict)
    
    LOG.INFO("Zakonczylem pobieranie markerow z contiga o ID: " + str(cont_id))
    return marks_return