import sys
import os
import pickle

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
xlsx_src_path = os.path.join(this_module_path, "xls", "src")
fasta_src_path = os.path.join(this_module_path, "fasta", "src")
pickle_path = os.path.join(this_module_path, "pickle")
log_path = os.path.join(this_module_path, "log")

markers_fasta_path = os.path.join(fasta_src_path, "markers.fasta")
markers_pickle_path = os.path.join(pickle_path, "markers.pickle")

server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.scaffold.models import Scaffold

def parseFastaFile():
    # Otworzenie pliku z sekwencjami
    fasta_file = open(markers_fasta_path, "r")
    markers = {}
    lines = fasta_file.readlines()
    marker_name = ""
    for line in lines:
        if ">" in line:
            marker_name = line[1 :].strip()
            markers[str(marker_name)] = ""
        else:
            markers[str(marker_name)] += line.strip("\n").upper()
    return markers

def readMarkers():
    markers = {}
    
    if not os.path.exists(markers_pickle_path):
        print "\n\nBuduje markery z pliku FASTA..."
        markers = parseFastaFile()
        print "\n[X] Zapisuje znalezione markery w pliku pickle\\markers.pickle..."
        pickle.dump(markers, open(markers_pickle_path, "wb"))
    else:
        print "\n[X] Odczytuje markers z pliku pickle..."
        markers = pickle.load(open(markers_pickle_path, "rb"))
        
    return markers

# ==========================================================================

class Marker:
    name = ""
    count = 0
    
    def __init__(self, name):
        self.name = name
        self.where = []
        
    def incCount(self, where_id):
        self.count += 1
        self.where.append(where_id)

def study():
    markers = readMarkers()
    print "Odczytanych markerow", len(markers)
    
    print "\n"
    
    # Odczytanie wszystkich scaffoldow z bazy danych
    print "Odczytuje scaffoldy z bazy danych..."
    scaffolds = Scaffold.objects.values('id', 'sequence')
    print "Odczytano", len(scaffolds), "scaffoldow."
    
    print "\n"
    
    markers_results = []
    
    i = 1
    all_markers = len(markers)
    for marker_name, marker_seq in markers.iteritems():
        print "\tAnalizuje <", i, "/", all_markers, ">:", marker_name
        i += 1
        
        marker = Marker(marker_name)
        
        # Przeszukanie wszystkich scaffoldow
        for scaffold in scaffolds:
            if marker_seq in scaffold['sequence']:
                marker.incCount(scaffold['id'])
                
        markers_results.append(marker)

    return markers_results
    
    
if __name__ == '__main__':
    markers_results = study()
    
    log_file = open(os.path.join(log_path, "markers.log"), "w")
    
    for marker in markers_results:
        if marker.count == 0:
            print "= 0 :", marker.name
            log_file.write("= 0 : " + str(marker.name) + "\n")
        elif marker.count ==1:
            print "\t= 1 :", marker.name
            log_file.write("\t= 1 : " + str(marker.name) + "\n")
        else:
            print "\t\t=", marker.count, ":", marker.name
            log_file.write("\t\t= " + str(marker.count) + " : " + str(marker.name) + "\n")
    
    log_file.close()