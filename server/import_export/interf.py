from server.scaffold.models import Scaffold, ScaffoldPosition
from server.contig.models import Contig
from server.chromosome.models import Chromosome, ChromosomeLength
from server.utils import log as LOG

def importScaffolds(organism_id, assemb_type, csv_array, fasta_array):
    LOG.INFO("Rozpoczynam import danych - scaffoldow...")
    
    LOG.DEBUG("CSV: " + str(csv_array))
    LOG.DEBUG("FASTA: " + str(fasta_array))
    
    if len(csv_array) != len(fasta_array):  # Brak czegos
        return -1
    
    csvs = {}
    fastas = {}
    
    for csv_obj in csv_array:
        if not csvs.has_key(str(csv_obj['id'])):
            csvs[str(csv_obj['id'])] = []
        csvs[str(csv_obj['id'])].append(csv_obj)
        
    for fasta_obj in fasta_array:
        fastas[str(fasta_obj['id'])] = fasta_obj
        
    LOG.DEBUG("CSV 2: " + str(csvs))
    LOG.DEBUG("FASTA 2: " + str(fastas))
        
    if len(csvs) != len(fastas):    # Brak czegos
        return -1
    
    if(csvs.keys() != fastas.keys()):   # Rozne ID
        return -1
    
    chromosomes = Chromosome.objects.all().filter(organism_id=int(organism_id))
    
    LOG.DEBUG("Wszystkie chromosomy organizmu: " + str(organism_id) + ": " + str(chromosomes))
    LOG.DEBUG("Importowane scaffoldy: " + str(csvs))
    
    # Mamy dobre dane - zapisujemy do bazy
    for csv_id, csv_obj_array in csvs.iteritems():
        try:
            # Odczytujemy ze scaffoldPositions od razu
            # Dodajemy dlugosci do ChromosomeLength
            # Czy dany scaffold nie nachodzi na inny scaffold? Jak nachodzi to potem recznie usuwamy.
            
            LOG.DEBUG("Obiekt CSV: " + str(csv_obj_array))
            scaffold_id = str(csv_obj_array[0]['id'])
            chromosome_id = int(csv_obj_array[0]['chr_id'])
            
            chrom = chromosomes[chromosome_id - 1]
            
            scaff_seq = str(fastas[scaffold_id]['seq'])
            
            LOG.DEBUG("Dodaje scaffold: " + str(scaffold_id) + " na chromosom: " + str(chrom.id))
            
            scaff_obj = Scaffold(id=scaffold_id, chromosome_id=chrom.id,
                     sequence=scaff_seq, assemb_type=int(assemb_type),
                     length_bp=len(scaff_seq))
            scaff_obj.save()
            LOG.DEBUG("Dodalem scaffold: " + str(scaff_obj.id))
            
            for i, csv_pos_obj in enumerate(csv_obj_array):
                start_cm = float(csv_pos_obj['start'])
                end_cm = float(csv_pos_obj['end'])
                
                LOG.DEBUG("Dodaje pozycje scaffoldu: " + str(scaffold_id) + ": (" + str(start_cm)  + ", " + str(end_cm) + ")")
               
                # Dodanie nowej pozycji 
                scaff_pos_obj = ScaffoldPosition(scaff_id=scaffold_id, start=start_cm, end=end_cm,
                                                 order=i)
                scaff_pos_obj.save()

            # ChromosomeLength
            chr_len = ChromosomeLength.objects.filter(chr_id=chrom.id, assemb_id=int(assemb_type))[0]

            if end_cm > chr_len.length:
                chr_len.length = end_cm
                chr_len.save()

        except TypeError:
            return -3
        except ValueError:
            return -4
    
    LOG.INFO("Zakonczylem import danych - scaffoldow...")
    
    return 0

def importContigs(csv_array, fasta_array):
    LOG.INFO("Rozpoczynam import danych - contigow...")
    
    LOG.DEBUG("CSV: " + str(csv_array))
    LOG.DEBUG("FASTA: " + str(fasta_array))
    
    if len(csv_array) != len(fasta_array):  # Brak czegos
        return -1
    
    csvs = {}
    fastas = {}
    
    for csv_obj in csv_array:
        csvs[str(csv_obj['id'])] = csv_obj
        
    for fasta_obj in fasta_array:
        fastas[str(fasta_obj['id'])] = fasta_obj
        
    if len(csvs) != len(fastas):    # Brak czegos
        return -1
    
    if(csvs.keys() != fastas.keys()):   # Rozne ID
        return -1
    
    # Mamy dobre dane - zapisujemy do bazy
    for csv_id, csv_obj in csvs.iteritems():
        # Czy dany scaffold istnieje? Jezeli nie to blad.
        # Czy dany contig nie nachodzi na inny contig? Jezeli nachodzi to usuwamy pozniej recznie
    
        scaffold_id = str(csv_obj['scaff_id'])
        LOG.DEBUG("Dodaje contig: " + str(csv_id) + " na scaffold: " + str(scaffold_id) + " --> " + str(csv_obj))
        if Scaffold.objects.filter(id = scaffold_id).count() != 1:
            LOG.DEBUG("Blad podczas importowania contiga: " + str(csv_id) + ". Scaffold: " + str(scaffold_id) + " nie istnieje!")
            return -3

        cont_seq = str(fastas[csv_id]['seq'])
        start_bp = float(csv_obj['start'])
        end_bp = float(csv_obj['end'])
        
        LOG.DEBUG("Dodaje contig: " + str(csv_id) + ". Pozycja: (" + str(start_bp) + " ," + str(end_bp) +  ")")
        
        contig = Contig(id=int(csv_id), scaff_id=scaffold_id, order=int(csv_obj['order']), start=start_bp, end=end_bp,
                        sequence=cont_seq, length_bp=len(cont_seq))
        contig.save()
        LOG.DEBUG("Dodalem contig: " + str(csv_id) + " na scaffold: " + str(scaffold_id))
        
    LOG.INFO("Zakonczylem import danych - contigow...")
    
    return 0