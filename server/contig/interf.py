from server.contig.models import Contig, ContigWrap
from server.contig.contigIntervals import ContigInterval, ContigIntervalTree

from server.utils import log as LOG

class ContigsTreeObject:
    interval_tree = None
    
    def getInstance(self):
        return self.interval_tree

def buildContigTree(scaff_id):
    LOG.INFO("Rozpoczynam budowanie drzewa przedzialowego contigow dla scaffoldu o ID:" + str(scaff_id))
    contigs = Contig.objects.all().filter(scaff_id = str(scaff_id))
    LOG.DEBUG("Ilosc contigow na scaffoldzie o ID: " + str(scaff_id) + " wynosi: " + str(len(contigs)))
    contigs_to_tree = []
    for contig in contigs:
        contig_interval = ContigInterval(contig.id, contig.start, contig.end, -1)
        contigs_to_tree.append(contig_interval)

    if len(contigs) != 0:
        # Zapamietanie obiektu drzewa przedzialowego
        ContigsTreeObject.interval_tree = ContigIntervalTree(contigs_to_tree)
        LOG.INFO("Zakonczylem budowanie drzewa przedzialowego contigow dla scaffoldu o ID:" + str(scaff_id))
        return 1
    else:
        LOG.INFO("Nie znaleziono contigow dla scaffoldu o ID: " + str(scaff_id))
        return 0

def getContigFromTree(start, stop):
    contigs_return = []
    if ContigsTreeObject.interval_tree == None:
        return contigs_return
    LOG.INFO("Rozpoczynam poszukiwanie contigow w drzewie. Od " + str(start) + " do " + str(stop))
    contigs_result = ContigsTreeObject.interval_tree.find(start, stop)
    i = 0
    for contig in contigs_result:
        # Obiekt contigu
        try:
            cont = Contig.objects.all().get(id = contig.contig_id)
        except Contig.DoesNotExist:
            LOG.WARN("Brak contigu o ID: " + str(contig.contig_id))
            return None
        #cont_wrap = ContigWrap(cont.id, cont.scaff_id, cont.order, cont.start, cont.end, cont.sequence, cont.length_bp)
        contigs_return.append(cont)
        i += 1
        
    contigs_return.sort(key = lambda x: x.scaff_id, reverse = False)
    contigs_return.sort(key = lambda x: x.start, reverse = False)

    LOG.DEBUG("Wynik poszukiwan (" + str(start) + " - " + str(stop) + "):\n" + str(contigs_return))
    LOG.INFO("Zakonczylem przeszukiwanie contigow w drzewie.")
    
    return contigs_return

def getContig(cont_id):
    LOG.INFO("Rozpoczynam pobieranie contigu o ID: " + str(cont_id))
    try:
        c = Contig.objects.all().get(id = int(cont_id))
    except Contig.DoesNotExist:
        LOG.WARN("Brak contigu o ID: " + str(cont_id))
        return None
    #cont_wrap = ContigWrap(c.id, c.scaff_id, c.order, c.start, c.end, c.sequence, c.length_bp)
    LOG.INFO("Zakonczylem pobieranie contigu o ID: " + str(cont_id))
    return c

def getScaffByContID(cont_id):
    LOG.INFO("Rozpoczynam pobieranie scaffoldu, na ktorym jest contig o ID: " + str(cont_id))
    try:
        c = Contig.objects.get(id = int(cont_id))
    except Contig.DoesNotExist:
        LOG.WARN("Brak contigu o ID: " + str(cont_id))
        return None
    scaff_id = c.scaff_id
    #TODO: Funkcja musisz zwracac scaffold, do ktorego nalezy dany contig. Problem? Do ktorej ScaffoldPosition nalezy ten contig?
    LOG.DEBUG("Contig o ID: " + str(cont_id) + " znajduje sie na scaffoldzie o ID: " + str(scaff_id))
    LOG.INFO("Zakonczylem pobieranie scaffoldu na ktorym jest contig o ID: " + str(cont_id))
    return c.scaff_id

def getContigs(scaff_id):
    LOG.INFO("Rozpoczynam pobieranie contigow ze scaffoldu o ID: " + str(scaff_id))
    contigs = Contig.objects.all().filter(scaff_id = str(scaff_id))
    LOG.DEBUG("Ilosc contigow na scaffoldzie o ID: " + str(scaff_id) + " wynosi " + str(len(contigs)))
    
    conts_return = []
    
    for cont in contigs:
        try:
            c = Contig.objects.all().get(id = cont.id)
        except Contig.DoesNotExist:
            LOG.WARN("Brak contigu o ID: " + str(cont.id))
            return None
        cont_wrap = ContigWrap(c.id, c.scaff_id, c.order, c.start, c.end, c.sequence, c.length_bp)
        conts_return.append(cont_wrap)
    
    LOG.INFO("Zakonczylem pobieranie contigow ze scaffoldu o ID: " + str(scaff_id))
    return conts_return

def getContigsDict(scaff_id):
    LOG.INFO("Rozpoczynam pobieranie contigow ze scaffoldu o ID: " + str(scaff_id))
    contigs = Contig.objects.all().filter(scaff_id = str(scaff_id))
    LOG.DEBUG("Ilosc contigow na scaffoldzie o ID: " + str(scaff_id) + " wynosi " + str(len(contigs)))
    
    conts_return = []
    
    for i, cont in enumerate(contigs):
        cont_dict = {}
        cont_dict['LP'] = i + 1
        cont_dict['ID'] = cont.id
        cont_dict['SCAFF_ID'] = cont.scaff_id
        cont_dict['START_INDEX'] = cont.start
        cont_dict['END_INDEX'] = cont.end
        cont_dict['LENGTH'] = cont.length_bp
        conts_return.append(cont_dict)
    
    LOG.INFO("Zakonczylem pobieranie contigow ze scaffoldu o ID: " + str(scaff_id))
    return conts_return

def deleteCongit(cont_id):
    LOG.INFO("Rozpoczynam usuwanie contigu o ID: " + str(cont_id))
    try:
        c = Contig.objects.get(id = int(cont_id))
    except Contig.DoesNotExist:
        LOG.WARN("Brak contigu o ID: " + str(cont_id))
        return None
    c.delete()
    return True
