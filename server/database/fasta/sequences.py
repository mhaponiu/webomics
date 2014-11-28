import re

def getSequences(file_path):
    # Otworzenie pliku z sekwencjami
    fasta_file = open(file_path, "r")
    scaffolds = {}
    lines = fasta_file.readlines()
    scaffold_name = ""
    for line in lines:
        if ">" in line:
            line = line[line.find("scf") + 3:].strip("\n")
            scaffold_name = line
            scaffolds[int(scaffold_name)] = ""
        else:
            scaffolds[int(scaffold_name)] += line.strip("\n")
    return scaffolds

def getSequencesCountArachne():
    # Otworzenie pliku z sekwencjami
    fasta_file = open("src\\scaff_arachne.fasta", "r").read()
    regex = re.compile('>repeat(.*?)\n')
    count = regex.findall(fasta_file)
    #print count[-1]
    return len(count)

def getSequencesCountCelera():
    # Otworzenie pliku z sekwencjami
    fasta_file = open("src\\scaff_celera.fasta", "r").read()
    regex = re.compile('>scf(.*?)\n')
    count = regex.findall(fasta_file)
    #print count[:1000]
    return len(count)


#print "Arachne:", getSequencesCountArachne()
print "Celera:", getSequencesCountCelera()
#print getSequences("src\\test.fasta")

