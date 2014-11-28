from server.organism.models import Organism
from server.chromosome.models import Chromosome, Assemb
from server.chromosome.interf import deleteChromosome

from server.utils import log as LOG
from config.settings import DEBUG

def getOrganisms():
    LOG.INFO("Rozpoczynam pobieranie wszystkich organizmow.")
    organisms = Organism.objects.all().values()
    LOG.INFO("Zakonczylem pobieranie wszystkich organizmow.")
    return organisms

def getOrganismsByID(organism_id):
    LOG.INFO("Rozpoczynam pobieranie obiektu organizmu o ID: " + str(organism_id))
    organism = Organism.objects.filter(id = organism_id).values()
    try:
        organism_ret = organism[0]
    except IndexError:
        LOG.WARN("Nie istnieje organizm o ID: " + str(organism_id))
        return None
    LOG.INFO("Zakonczylem pobieranie obiektu organizmu o ID: " + str(organism_id))
    return organism_ret

def addOrganism(org_name, org_desc, chrs_count):
    LOG.INFO("Rozpoczynam dodawanie organizmu: " + str(org_name) + ". Ilosc chromosomow: " + str(chrs_count) + ". Opis: " + str(org_desc))
    organism = None
    try:
        organism = Organism(name=str(org_name), description=str(org_desc))
        organism.save()
        LOG.DEBUG("Dodano organizm: " + str(organism.id))
    except Exception:
        LOG.WARN("Blad podczas dodawania nowego organizmu: " + str(org_name))
        return None
    
    try:
        # Dodanie wszystkich chromosomow
        for i in range(chrs_count):
            chr = Chromosome(name=("Chromosome " + str(i+1)), organism_id=int(organism.id))
            chr.save()
            LOG.DEBUG("Dodano chromosom: " + str(chr.name) + " (" + str(chr.id) + ")" + " do organizmu: " + str(chr.organism_id))
    except Exception:
        LOG.WARN("Blad podczas dodawania nowego chromosomu do organizmu: " + str(org_name))
        return None
    
    LOG.INFO("Zakonczylem dodawanie organizmu: " + str(org_name))
    return organism.id

def deleteOrganism(org_id):
    LOG.INFO("Rozpoczynam usuwanie organizmu o ID: " + str(org_id))
    try:
        o = Organism.objects.get(id = int(org_id))
    except Organism.DoesNotExist:
        LOG.WARN("Brak organizmu o ID: " + str(org_id))
        return None
    o.delete()
    
    LOG.DEBUG("Usuwam wszystkie chromosomy organizmu: " + str(org_id) + " wraz z podleglymi strukturami")
    # Usuniecie wszystkich chromosomow ze wszystkimi strukturami
    chrs = Chromosome.objects.filter(organism_id = int(org_id))
    for chromosome in chrs:
        LOG.DEBUG("Usuwam chromosome: " + str(chromosome.id) + " z organizmu: " + str(org_id))
        deleteChromosome(chromosome.id)
        
    LOG.DEBUG("Usuwam wszystkie typy asemblacji z organizmu: " + str(org_id))
    # Usuniecie wszystkich typow asemblacji
    Assemb.objects.filter(organism_id = int(org_id)).delete()
    
    LOG.INFO("Zakonczylem usuwanie organizmu o ID: " + str(org_id))
    return True