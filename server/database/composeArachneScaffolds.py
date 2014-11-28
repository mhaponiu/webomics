import sys
import os
import pickle
import time

from openpyxl.reader.excel import load_workbook

from fasta import fastaManage

ASSEMB = fastaManage.ARACHNE

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
xlsx_src_path = os.path.join(this_module_path, "xls", "src")
pickle_path = os.path.join(this_module_path, "pickle")

source_file_path = os.path.join(xlsx_src_path, "Cucumber_scaffold.xlsx")
pickle_file_path = os.path.join(pickle_path, "scaffolds_arachne.pickle")

server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.scaffold.models import Scaffold as ScaffoldDB
from server.scaffold.models import ScaffoldPosition as ScaffoldPositionDB
from server.contig.models import Contig as ContigDB

from server.database.createDatabase import getOrCreateArachneScaffolds

class Scaffold:
    id = -1
    contigs = None
    order = -1
    sequence = ""
    
    def __init__(self, id_, order):
        self.id = id_
        self.order = order
        self.contigs = []
    
    def addContig(self, contig):
        self.contigs.append(contig)
        
    def appendSequence(self, seq_frag):
        self.sequence += seq_frag
    
class Contig:
    id = -1
    order = -1
    length = -1
    gap_after = -1
    start = -1
    stop = -1
    
    sequence = ""
    
    def __init__(self, id_, order, length, gap_after, sequence):
        self.id = id_
        self.order = order
        self.length = length
        self.gap_after = gap_after
        self.sequence = sequence

def readInformations():
    scaffolds = []
    contigs_sequences = fastaManage.loadContigs(fastaManage.ARACHNE)
    
    xls_file = load_workbook(source_file_path)
    
    for sheet in xls_file.worksheets:
        if sheet.title == 'Arkusz1':
            # Odczytanie pozycji kolumn
            first_row = sheet.rows[0]
            scaff_id_col = -1
            cont_id_col = -1
            cont_order_col = -1
            cont_length_col = -1
            cont_gap_after_col = -1
            
            for i, cell in enumerate(first_row):
                if "scf_id" in cell.value:
                    scaff_id_col = i
                    continue
                elif "ctg_id" in cell.value:
                    cont_id_col = i
                    continue
                elif "ordinal_num_of_contig_in_scf" in cell.value:
                    cont_order_col = i
                    continue
                elif "length_of_ctg" in cell.value:
                    cont_length_col = i
                    continue
                elif "estimated_gap_after_contig" in cell.value:
                    cont_gap_after_col = i
                    continue
            if scaff_id_col == -1:
                raise "Nie znaleziono kolumny 'scf_id'!"
                sys.exit(1)
            if cont_id_col == -1:
                raise "Nie znaleziono kolumny 'ctg_id'!"
                sys.exit(1)
            if cont_order_col == -1:
                raise "Nie znaleziono kolumny 'ordinal_num_of_contig_in_scf'!"
                sys.exit(1)
            if cont_length_col == -1:
                raise "Nie znaleziono kolumny 'length_of_ctg'!"
                sys.exit(1)
            if cont_gap_after_col == -1:
                raise "Nie znaleziono kolumny 'estimated_gap_after_contig'!"
                sys.exit(1)
    
            # Mamy pozycje kolumn - czas parsowac kolejne wiersze
            scaff_order = 0
            last_scaff_id = -1
            for row in sheet.rows[1:]:
                try:
                    # Wartosci kolumn
                    scaff_id = int(row[scaff_id_col].value)
                    cont_id = int(row[cont_id_col].value)
                    cont_order = int(row[cont_order_col].value)
                    cont_length = int(row[cont_length_col].value)
                    cont_gap_after = int(row[cont_gap_after_col].value)
                    
                    try:
                        cont_sequence = contigs_sequences[cont_id]
                    except KeyError:
                        print "Brak contiga", cont_id, "w pliku fasta, wstawiam dziure!"
                        cont_sequence = 'N' * cont_length
                    
                    # Dodajemy nowy scaffold
                    if last_scaff_id != scaff_id:
                        print "\tPrzetwarzam SCAFFOLD =", scaff_id
                        scaffolds.append(Scaffold(scaff_id, scaff_order))
                        scaff_order += 1
                        last_scaff_id = scaff_id
                    
                    # Dodajemy contig do ostatniego scaffolda
                    print "\tPrzetwarzam CONTIG =", cont_id
                    current_contig = Contig(cont_id, cont_order, cont_length, cont_gap_after, cont_sequence)
                    scaffolds[-1].addContig(current_contig)
                except ValueError:
                    print "Bledna wartosc w wierszu:", row
                    time.sleep(1)
                    continue
    
    return scaffolds

def createScaffolds():
    print "\n\nOdczytuje informacje o scaffoldach ARACHNE..."
    scaffolds = readInformations()
    
    # Buduje sekwencje scaffoldow arachne
    print "\n\nBuduje sekwencje scaffoldow ARACHNE..."
    
    # Posortowanie scaffoldow po order
    scaffolds = sorted(scaffolds, key = lambda scaffold : scaffold.order)
    
    scaffolds_count = len(scaffolds)
    for i, scaffold in enumerate(scaffolds):
        print "\rScaffold:", i, "/", scaffolds_count,
        
        # Posortowanie contigow po order
        contigs = sorted(scaffold.contigs, key = lambda contig : contig.order)
        for contig in contigs:
            if contig.length != len(contig.sequence):
                print "(CID: ", contig.id, ") --> Dlugosc sekwencji odczytana z XLSX rozni sie od rzeczywistej dlugosci sekwencji z pliku FASTA:", contig.length, "vs", len(contig.sequence)
                #time.sleep(1)
                
            gap = contig.gap_after
            if gap < 0:
                gap = 0
            
            # Pozycja START contiga - dlugosc sekwencji scaffoldu PRZED dodaniem aktualnego contiga
            contig.start = len(scaffold.sequence)
            
            # Dodanie sekwencji contiga
            scaffold.appendSequence(contig.sequence)

            # Pozycja STOP contiga - dlugosc sekwencji scaffoldu PO dodaniu aktualnego contiga
            contig.stop = len(scaffold.sequence)
                
            # Dodanie przerwy
            scaffold.appendSequence('N' * gap)
    
    return scaffolds

def getScaffolds():
    scaffolds = []
    
    if not os.path.exists(pickle_file_path):
        print "\n\nBuduje scaffoldy ARACHNE..."
        scaffolds = createScaffolds()
        print "\n[X] Zapisuje znalezione scaffoldy w pliku pickle\\scaffolds_arachne.pickle..."
        pickle.dump(scaffolds, open(pickle_file_path, "wb"))
    else:
        print "\n[X] Odczytuje scaffoldy ARACHNE z pliku pickle..."
        scaffolds = pickle.load(open(pickle_file_path, "rb"))
    
    return scaffolds

def saveArachneDataToDB():
    scaffolds = getScaffolds()
    scaffolds_ids = []
    new_scaffolds_dict = {}
    for scaffold in scaffolds:
        new_scaffolds_dict[scaffold.id] = scaffold
        scaffolds_ids.append(scaffold.id)
        
    sum = 0
        
    chromosomes = getOrCreateArachneScaffolds("pickle\\scaffolds_arachne_old.pickle", False)
    
    #for chr_id, scaffolds_dict in chromosomes.iteritems():
    #    sum += len(scaffolds_dict)
    #    print "\n>> Odczytuje chromosom", chr_id, ". Scaffoldow:", len(scaffolds_dict)
    #    for scaff_id_old, scaff_poss_frag_old in scaffolds_dict.iteritems():
    #        try:
    #            if(int(scaff_id_old) not in scaffolds_ids):
    #                print "Scaffold:", scaff_id_old, "nie znajduje sie w NOWEJ tablicy!"
    #        except ValueError:
    #            print "ID:", scaff_id_old, "nie jest typu INT."
    #
    #print "\n\nSUMA STARYCH:\t", sum
    #print "SUMA NOWYCH:\t", len(scaffolds_ids)
    
    for chr_id, old_scaffolds_dict in chromosomes.iteritems():
        for old_scaff_id, old_scaff_poss_frag in old_scaffolds_dict.iteritems():
            if(int(old_scaff_id) in scaffolds_ids): # Dodajemy tylko wtedy :)
                
                # Dodajemy scaffold
                new_scaffold = new_scaffolds_dict[old_scaff_id]
                scaff_sequence = new_scaffold.sequence
                scaff_to_save = ScaffoldDB(id = old_scaff_id, chromosome_id = chr_id, sequence = scaff_sequence, assemb_type = 0, length_bp = len(scaff_sequence))
                scaff_to_save.save()
                for scaff_poss in old_scaff_poss_frag:
                    scaff_pos_obj = ScaffoldPositionDB(scaff_id = scaff_to_save.id, start = scaff_poss[1][0], end = scaff_poss[1][-1], order = scaff_poss[0])
                    scaff_pos_obj.save()
                    
                # Dodajemy contigi
                for cont in new_scaffold.contigs:
                    try:
                        contig_to_save = ContigDB(id = cont.id, 
                             scaff_id = new_scaffold.id,
                             order = cont.order,
                             start = cont.start,
                             end = cont.stop,
                             sequence = cont.sequence,
                             length_bp = cont.length)
                        contig_to_save.save()
                    except ValueError:
                        print "Sekwencja contiga", cont.id, "nie znajduje sie na scaffoldzie", new_scaffold.id
    

if __name__ == '__main__':
    #scaffolds = getScaffolds()
    #print "Ilosc odczytanych scaffoldow:", len(scaffolds)
    saveArachneDataToDB()