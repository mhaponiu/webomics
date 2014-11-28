import sys
import os

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
fasta_path = os.path.join(this_module_path, "fasta", "scaffolds.fasta")

contigs_path = os.path.join(this_module_path, "output", "contigs.fasta")

def getScaffolds(fasta_lines):
    scaffolds = {}
    
    scaff_id = ""
    
    print "Odczytuje scaffoldy z pliku fasta!"
    
    lines_count = len(fasta_lines)
    
    for i, fasta_line in enumerate(fasta_lines):
        print "\rLinia:", i, "/", lines_count,
        
        if '>' in fasta_line:   # nowy scaffold sie rozpoczyna
            # Odczytujemy jego ID i zapamietujemy
            scaff_id = fasta_line.replace(">scf", "").strip()
            if not scaffolds.has_key(scaff_id):
                scaffolds[scaff_id] = ""
            else:
                print "Scaffold", scaff_id, "jest juz dodany!"
        else:
            # Odczytujemy sekwencje i dodajemy ja do ostatniego scaffoldu
            if not scaffolds.has_key(scaff_id):
                print "Nie istnieje scaffold", scaff_id, "!"
                continue
            scaffolds[scaff_id] += fasta_line.strip()

    print "\tODCZYTANO", len(scaffolds), "SCAFFOLDOW!"
    
    return scaffolds

def getContigs(sequence):
    return [cont for cont in sequence.split('N') if len(cont) > 0]

def createContigs(src_path):
    fasta_lines = open(src_path, "r").readlines()
    
    scaffolds = getScaffolds(fasta_lines)
    
    cont_id = 0
    
    contigs_file = open(contigs_path, "w")
    
    for scaff_id, scaff_seq in scaffolds.iteritems():
        contigs = getContigs(scaff_seq)
        for contig_seq in contigs:
            contigs_file.write(">" + str(cont_id) + " SID:" + str(scaff_id) + "\n")
            contigs_file.write(str(contig_seq) + "\n")
            cont_id += 1
    
    contigs_file.close()

if __name__ == '__main__':
    createContigs(fasta_path)
    
    '''sequence = "AAANNNANAANNNANAA"
    contigs = getContigs(sequence)
    for contig in contigs:
        print contig'''