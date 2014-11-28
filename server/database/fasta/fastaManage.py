import os
import sys

import pickle

from openpyxl.reader.excel import load_workbook

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
fasta_src_path = os.path.join(this_module_path, "src")

ARACHNE = 0
CELERA = 1

SCAFFOLD = 0
CONTIG = 1

## !! Do sprawdzenia jeszcze z plikami fasta dokladnie, czy zgadzaja sie te wartosci po '>'
def getSequences(fasta_path, struct, assem):
    if not os.path.exists(fasta_path):
        print "[F] Niepoprawna sciezka do pliku fasta", fasta_path, "!"
        sys.exit(1)
    # Otworzenie pliku z sekwencjami
    fasta_file = open(fasta_path, "r")
    structures = {}
    lines = fasta_file.readlines()
    structure_name = ""

    # --------------------------------- CELERA ----------------------------------
    if assem == CELERA:
        if struct == SCAFFOLD:
            type_str = "scf"
        elif struct == CONTIG:
            type_str = "ctg"
        else:
            print "[F] Niepoprawny typ struktury!"

        for line in lines:
            if ">" in line:
                line = line[line.find(type_str) + len(type_str):].strip("\n")
                structure_name = line
                structures[int(structure_name)] = ""
            else:
                structures[int(structure_name)] += line.strip("\n")
    # --------------------------------- ARACHNE ----------------------------------
    elif assem == ARACHNE:
        for line in lines:
            try:
                if ">" in line:
                    if struct == SCAFFOLD:
                        if "Scaffold" in line:
                            type_str = "Scaffold"
                        #elif "repeat" in line:
                        #    type_str = "repeat"
                        else:
                            print "Niepoprawna struktura po znaku >!"
                            break
                    elif struct == CONTIG:
                        type_str = "CSB10A_v1_contig_"
                    else:
                        print "[F] Niepoprawny typ struktury!"
                        break
                    line = line[line.find(type_str) + len(type_str):].strip("\n")
                    structure_name = line
                    print structure_name
                    structures[int(structure_name)] = ""
                else:
                    structures[int(structure_name)] += line.strip("\n")
            except ValueError:
                print "Niepoprawne ID:", structure_name, "! Nie dodaje."
                continue
    # ------------------------------- NIEPOPRAWNY ----------------------------------
    else:
        print "[F] Niepoprawny typ asemblacji!"
        sys.exit(2)
            
    return structures

def loadScaffolds(assem):
    if assem == CELERA:
        pickle_file = "scaff_celera.pickle"
        fasta_file = "scaff_celera.fasta"
        assem_str = "Celera"
    elif assem == ARACHNE:
        pickle_file = "scaff_arachne.pickle"
        fasta_file = "scaff_arachne.fasta"
        assem_str = "Arachne"
    print "[F] Odczytuje scaffoldy " + assem_str + "..."
    if not os.path.exists(os.path.join(fasta_src_path, pickle_file)):
        fasta_path = os.path.join(fasta_src_path, fasta_file)
        print "[F] Pobieram scaffoldy z pliku..."
        scaffolds = getSequences(fasta_path, SCAFFOLD, assem)
        print "[F] Zrzucam obiekt (scaffold) do pliku..."
        pickle.dump(scaffolds, open(os.path.join(fasta_src_path, pickle_file), "wb"))
        print "[F] Zakonczylem zrzucanie obiektu (scaffold) do pliku."
    else:
        print "[F] Pobieram scaffoldy z pickla..."
        scaffolds = pickle.load(open(os.path.join(fasta_src_path, pickle_file), "rb"))
    print "[F] Liczba odczytanych scaffoldow:", len(scaffolds)
    return scaffolds

def loadContigs(assem):
    if assem == CELERA:
        pickle_file = "cont_celera.pickle"
        fasta_file = "cont_celera.fasta"
        assem_str = "Celera"
    elif assem == ARACHNE:
        pickle_file = "cont_arachne.pickle"
        fasta_file = "cont_arachne.fasta"
        assem_str = "Arachne"
    print "\n[F] Odczytuje contigi " + assem_str + "..."
    if not os.path.exists(os.path.join(fasta_src_path, pickle_file)):
        fasta_path = os.path.join(fasta_src_path, fasta_file)
        print "[F] Pobieram contigi z pliku..."
        contigs = getSequences(fasta_path, CONTIG, assem)
        print "[F] Zrzucam obiekt (contig) do pliku..."
        pickle.dump(contigs, open(os.path.join(fasta_src_path, pickle_file), "wb"))
        print "[F] Zakonczylem zrzucanie obiektu (contig) do pliku."
    else:
        print "[F] Pobieram contigi z pickla..."
        contigs = pickle.load(open(os.path.join(fasta_src_path, pickle_file), "rb"))
    print "[F] Liczba odczytanych contigow:", len(contigs)
    return contigs

def getCoverage(scaffolds, contigs, assem):
    if assem == CELERA:
        pickle_file = "cont_coverage_celera.pickle"
        assem_str = "Celera"
    elif assem == ARACHNE:
        pickle_file = "cont_coverage_arachne.pickle"
        assem_str = "Arachne"
    print "\n[F] Sprawdzam, czy kazdy contig umieszczony jest na scaffoldzie..."
    if not os.path.exists(os.path.join(fasta_src_path, pickle_file)):
        print "[F] Badam contigi..."
        contigs_coverage = {}
        i = 0
        contgis_len = len(contigs)
        for contig_id, contig_seq in contigs.iteritems():
            i += 1
            print "\r" + str(i) + "/" + str(contgis_len),
            contigs_coverage[int(contig_id)] = -1
            for scaffold_id, scaffold_seq in scaffolds.iteritems():
                if contig_seq in scaffold_seq:
                    contigs_coverage[int(contig_id)] = int(scaffold_id)
                    break
        print "\n[F] Zrzucam obiekt (contig coverage celera) do pliku..."
        pickle.dump(contigs_coverage, open(os.path.join(fasta_src_path, pickle_file), "wb"))
        print "[F] Zakonczylem zrzucanie obiektu (contig coverage celera) do pliku."
    else:
        print "[F] Pobieram pokrycie contigow z pickla..."
        contigs_coverage = pickle.load(open(os.path.join(fasta_src_path, pickle_file), "rb"))
    print "[F] Contigow przy badaniu pokrycia:", len(contigs_coverage)
    return contigs_coverage

def getScaffoldsLength(scaffolds, without_gap = False):
    scaffolds_len = {}
    for scaff_id, seq in scaffolds.iteritems():
        seq = seq.replace(" ", "").replace("\n", "")
        if without_gap:
            seq = seq.replace("N", "")
        scaffolds_len[scaff_id] = len(seq)
    return scaffolds_len

def getArachneMarkers():
    pickle_file = "markers.pickle"
    fasta_file = "markers.fasta"
    ssr_file = "ssr_seqs.xlsx"
    if not os.path.exists(os.path.join(fasta_src_path, pickle_file)):
        fasta_path = os.path.join(fasta_src_path, fasta_file)
        print "[F] Pobieram markery z pliku fasta..."
        markers = getMarkersSequences(fasta_path)
        print "[F] Markerow z pliku fasta:", len(markers)
        ssr_path = os.path.join(fasta_src_path, ssr_file)
        print "[F] Pobieram markery SSR z pliku xlsx..."
        markers = getSSRSequences(markers, ssr_path)
        print "[F] Zrzucam obiekt (markers) do pliku..."
        #pickle.dump(markers, open(os.path.join(fasta_src_path, pickle_file), "wb"))
        print "[F] Zakonczylem zrzucanie obiektu (markers) do pliku."
    else:
        print "[F] Pobieram markery z pickla..."
        markers = pickle.load(open(os.path.join(fasta_src_path, pickle_file), "rb"))
    print "[F] Liczba wszystkich odczytanych markerow:", len(markers)
    return markers

def getMarkersSequences(fasta_path):
    if not os.path.exists(fasta_path):
        print "[F] Niepoprawna sciezka do pliku fasta", fasta_path, "!"
        sys.exit(1)
    # Otworzenie pliku z sekwencjami
    fasta_file = open(fasta_path, "r")
    markers = {}
    lines = fasta_file.readlines()
    marker_name = ""
    
    for line in lines:
        if ">" in line:
            line = line[1:].strip("\n")
            marker_name = line
            markers[str(marker_name)] = ""
        else:
            markers[str(marker_name)] += line.strip("\n").upper()
            
    return markers

def getSSRSequences(markers, ssr_path):
    if not os.path.exists(ssr_path):
        print "[F] Niepoprawna sciezka do pliku z sekwencjami markerow SSR", ssr_path, "!"
        sys.exit(1)
    # Otworzenie pliku z sekwencjami
    xls_file = load_workbook(ssr_path)
    for sheet in xls_file.worksheets:
        if sheet.title in ['995_primer']:
            # Odczytanie pozycji kolumn
            first_row = sheet.rows[0]
            name_col = -1
            motif_col = -1
            forward_col = -1
            reverse_col= -1
            
            for i, cell in enumerate(first_row):
                # Odczytanie nazwy markera
                if "loci" == cell.value:
                    name_col = i
                    continue
                # Odczytanie motywu markera
                if "motif" == cell.value:
                    motif_col = i
                    continue
                # Odczytanie poczatku markera
                if "forward_primer" == cell.value:
                    forward_col = i
                    continue
                # Odczytanie konca markera
                if "reverse_primer" == cell.value:
                    reverse_col = i
                    continue

            if name_col == -1:
                raise "[X] Nie znaleziono kolumny 'loci'!"
                sys.exit(1)
            if motif_col == -1:
                raise "[X] Nie znaleziono kolumny 'motif'!"
                sys.exit(1)
            if forward_col == -1:
                raise "[X] Nie znaleziono kolumny 'forward_primer'!"
                sys.exit(1)
            if reverse_col == -1:
                raise "[X] Nie znaleziono kolumny 'reverse_primer'!"
                sys.exit(1)

            # Kolejne markery
            for i, row in enumerate(sheet.rows[1:]):
                # MARKER NAME
                marker_name = str(row[name_col].value)
                # MARKER MOTIF
                motif = str(row[motif_col].value)
                # MARKER FORWARD
                forward = str(row[forward_col].value)
                # MARKER REVERSE
                reverse = str(row[reverse_col].value)
                
                if marker_name == "None" or forward == "None" or reverse == "None":
                    print "Pusta linia (", i, ")!"
                    continue
                
                # Zbudowanie sekwencji
                marker_seq = ""
                motifs = getMotifs(motif)
                if motifs == None:  # Nie chcemy takiego markera
                    continue
                marker_seq += forward
                for (motif_seq, motif_count) in motifs:
                    marker_seq += motif_seq * motif_count
                marker_seq += reverse
 
                if not markers.has_key(marker_name):     # Nie mamy jeszcze tego markera
                    markers[str(marker_name)] = str(marker_seq).upper()
                else:
                    print "Marker", marker_name, "juz istnieje!"
                    print "Forward:", forward
                    print "Reverse:", reverse
                    print "Linia:", i
                    continue
    return markers

def getMotifs(motif):
    motifs = []

    if motif == "NA":
        return None

    try:
        left_bracket = motif.find("(")
        
        if left_bracket == -1:  # cos takiego: "TC"
            motifs.append((motif, 1))
            return motifs
        
        # Mamy co najmniej jeden motyw, np. "(TTTAAT)5(A)31"
        while left_bracket != -1:
            right_bracket = motif.find(")", left_bracket)
            motif_seq = motif[left_bracket + 1 : right_bracket]
            left_bracket = motif.find("(", right_bracket)
            if left_bracket == -1:
                motif_count = int(motif[right_bracket + 1 : ])
            else:
                motif_count = int(motif[right_bracket + 1 : left_bracket])
            
            motifs.append((motif_seq, motif_count))
    except ValueError:
        print "Blad w kolumnie z motywem! -->", motif
        sys.exit(1)

    return motifs

def main():
    print "[F] Rozpoczynam badania...\n"
    print "-------------------------------- CELERA ------------------------------------"
    # Pobranie scaffoldow
    scaffolds_celera = loadScaffolds(CELERA)
    # Pobranie contigow
    contigs_celera = loadContigs(CELERA)
    # Sprawdzanie pokrycia
    contigs_coverage = getCoverage(scaffolds_celera, contigs_celera, CELERA)

    print "\n[F] Sprawdzam stopien pokrycia..."
    bad = 0
    bad_list = []
    i = 0
    contigs_coverage_len = len(contigs_coverage)
    for contig_id, scaffold_id in contigs_coverage.iteritems():
        i += 1
        print "\r" + str(i) + "/" + str(contigs_coverage_len),

        if scaffold_id == -1:
            bad += 1
            bad_list.append(int(contig_id))

    print "\n[F] Contigi nie zawierajace sie w zadnym scaffoldzie:"
    print str(bad) + "/" + str(len(contigs_coverage))
    bad_list_file = open(os.path.join(fasta_src_path, "bad_list.txt"), "w")
    try:
        for bad_elem in bad_list:
            #print bad_elem,
            bad_list_file.write(str(bad_elem) + "\n")
            #print bad_elem
            bad_list_file.write(contigs_celera[int(bad_elem)] + "\n")
    except KeyError:
        print "[F] Nieprawidlowa wartosc klucza. Brak zadanego contiga!"
        sys.exit(1)

    bad_list_file.close()
    print "\n\n[F] Zakonczylem badania."

def mainLen():
    scaff = loadScaffolds(CELERA)
    print "[F] Obliczam dlugosci sekwencji scaffoldow celera z dziurami..."
    scaffolds_len = getScaffoldsLength(scaff)
    len_file_name = "study\\celera_scaffolds_len.csv"
    print "[F] Zapisuje do pliku:", len_file_name
    length_file = open(len_file_name, "w")
    for sid, slen in scaffolds_len.iteritems():
        length_file.write(str(sid) + ";" + str(slen) + "\n")
    length_file.close()

    print "[F] Obliczam dlugosci sekwencji scaffoldow celera bez dziur..."
    scaffolds_len = getScaffoldsLength(scaff, True)
    len_file_name = "study\\celera_scaffolds_len_without_gap.csv"
    print "[F] Zapisuje do pliku:", len_file_name
    length_file = open(len_file_name, "w")
    for sid, slen in scaffolds_len.iteritems():
        length_file.write(str(sid) + ";" + str(slen) + "\n")
    length_file.close()

if __name__ == "__main__":
    #main()
    #mainLen()
    
    markers = getArachneMarkers()
    
    print markers["SSR17062"]
