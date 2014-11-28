from server.chromosome.models import Chromosome, ChromosomeLength, Assemb
from server.scaffold.models import Scaffold
from server.scaffold.interf import deleteScaffold

from server.utils import log as LOG

def getChromosomes(organism_id):
    LOG.INFO("Rozpoczynam pobieranie wszystkich chromosomow z organizmu: " + str(organism_id))
    chromosomes = Chromosome.objects.filter(organism_id=int(organism_id)).values()
    LOG.DEBUG("Chromosomy organizmu: " + str(organism_id) + ": " + str(chromosomes))
    # Pobranie pierwszego typu asemblacji danego organizmu
    org_assembs = Assemb.objects.filter(organism_id = int(organism_id))
    if len(org_assembs) == 0:
        LOG.DEBUG("Brak typow asemblacji organizmu: " + str(organism_id))
        return None
    
    LOG.DEBUG("Typy asemblacji organizmu: " + str(organism_id) + ": " + str(org_assembs))
    
    # Wybieramy tego, ktory jest najdluzszy sumarycznie
    ass_lenghts = {}
    for ass in org_assembs:
        chr_len_objs = ChromosomeLength.objects.filter(assemb_id = ass.id)
        total_len = 0.0
        for chr_len_obj in chr_len_objs:
            total_len += chr_len_obj.length
        LOG.DEBUG("Typ asemblacji: " + str(ass) + ". Sumaryczna dlugosc: " + str(total_len))
        ass_lenghts[ass.id] = total_len
        
    max_assemb = max(ass_lenghts, key=ass_lenghts.get)
    LOG.DEBUG("Typ asemblacji o najwiekszej sumie dlugosci chromosomow: " + str(max_assemb))
    
    if max_assemb == 0.0:
        LOG.DEBUG("Najdluzszy chromosom ma 0 dlugosc.")
        return None
    
    for chromosome in chromosomes:
        try:
            chr_len = ChromosomeLength.objects.get(chr_id = chromosome['id'], assemb_id = max_assemb)
            chromosome['length'] = chr_len.length
        except ChromosomeLength.DoesNotExist:
            LOG.WARN("Chromosome o ID: " + str(chromosome['id']) + " nie ma zadnej dlugosci.")
            return None
    
    LOG.INFO("Zakonczylem pobieranie wszystkich chromosomow z organizmu: " + str(organism_id))
    return chromosomes

def getChromosomeByID(chr_id):
    LOG.INFO("Rozpoczynam pobieranie obiektu chromosomu o ID: " + str(chr_id))
    chromosome = Chromosome.objects.filter(id = int(chr_id)).values()
    try:
        chromosome_ret = chromosome[0]
    except IndexError:
        LOG.WARN("Nie istnieje chromosom o ID: " + str(chr_id))
        return None
    
    LOG.DEBUG("Pobieram typy asemblacji organizmu: " + str(chromosome_ret['organism_id']))
    
    # Pobranie pierwszego typu asemblacji danego organizmu
    org_assembs = Assemb.objects.filter(organism_id = int(chromosome_ret['organism_id']))
    if len(org_assembs) == 0:
        return None
    
    LOG.DEBUG("Typy asemblacji organizmu: " + str(chromosome_ret['organism_id']) + ": " + str(org_assembs))
    
    # Wybieramy tego, ktory jest najdluzszy sumarycznie
    ass_lenghts = {}
    for ass in org_assembs:
        chr_len_objs = ChromosomeLength.objects.filter(assemb_id = ass.id)
        total_len = 0.0
        for chr_len_obj in chr_len_objs:
            total_len += chr_len_obj.length
        LOG.DEBUG("Typ asemblacji: " + str(ass) + ". Sumaryczna dlugosc: " + str(total_len))
        ass_lenghts[ass.id] = total_len
        
    max_assemb = max(ass_lenghts, key=ass_lenghts.get)
    LOG.DEBUG("Typ asemblacji o najwiekszej sumie dlugosci chromosomow: " + str(max_assemb))
    
    if max_assemb == 0.0:
        LOG.DEBUG("Najdluzszy chromosom ma 0 dlugosc.")
        return None
    
    try:
        chr_len = ChromosomeLength.objects.get(chr_id = chromosome_ret['id'], assemb_id = max_assemb)
    except ChromosomeLength.DoesNotExist:
        LOG.WARN("Chromosome o ID: " + str(chr_id) + " nie ma zadnej dlugosci.")
        return None
    print "Dlugosc:", chr_len
    chromosome_ret['length'] = chr_len.length
    LOG.INFO("Zakonczylem pobieranie obiektu chromosomu o ID: " + str(chr_id))
    return chromosome_ret

def getAssembByID(assemb_id):
    LOG.INFO("Rozpoczynam pobieranie obiektu typu asemblacji o ID: " + str(assemb_id))
    assemb = Assemb.objects.filter(id = assemb_id).values()
    try:
        assemb_ret = assemb[0]
    except IndexError:
        LOG.WARN("Nie istnieje typ asemblacji o ID: " + str(assemb_id))
        return None
    LOG.INFO("Zakonzylem pobieranie obiektu typu asemblacji o ID: " + str(assemb_id))
    return assemb_ret

def getAssembName(assemb_id):
    LOG.INFO("Rozpoczynam pobieranie nazwy typu asemblacji o ID: " + str(assemb_id))
    try:
        assemb = Assemb.objects.get(id = int(assemb_id))
    except Assemb.DoesNotExist:
        LOG.WARN("Nie istnieje typ asemblacji o ID: " + str(assemb_id))
        return None
    LOG.INFO("Zakonczylem pobieranie nazwy typu asemblacji o ID: " + str(assemb_id))
    return assemb.name

def getAssembs():
    LOG.INFO("Rozpoczynam pobieranie wszystkich typow asemblacji.")
    assembs = Assemb.objects.all().values()
    LOG.INFO("Zakonczylem pobieranie wszystkich typow asemblacji: " + str(assembs))
    return assembs

def getAssembsFromOrganism(organism_id):
    LOG.INFO("Rozpoczynam pobieranie wszystkich typow asemblacji z organizmu: " + str(organism_id))
    assembs = Assemb.objects.filter(organism_id=int(organism_id)).values()
    LOG.INFO("Zakonczylem pobieranie wszystkich typow asemblacji z organizmu: " + str(organism_id) + ": " + str(assembs))
    return assembs

def getAssembsFromOrganismOld(organism_id):
    LOG.INFO("Rozpoczynam pobieranie wszystkich typow asemblacji z organizmu: " + str(organism_id))
    assembs = []

    query = '''
        SELECT DISTINCT
          chromosome_assemb.id, 
          chromosome_assemb.name
        FROM 
          public.chromosome_assemb
        INNER JOIN public.chromosome_chromosomelength
        ON chromosome_assemb.id = chromosome_chromosomelength.assemb_id
        INNER JOIN public.chromosome_chromosome
        ON chromosome_chromosomelength.chr_id = chromosome_chromosome.id
        INNER JOIN public.organism_organism
        ON chromosome_chromosome.organism_id = %s;
        ''' % (organism_id)
    
    assembs_raws = Assemb.objects.raw(query)
    
    for ass in assembs_raws:
        ass_dict = {}
        ass_dict['id'] = str(ass.id)
        ass_dict['name'] = ass.name
        ass_dict['description'] = ass.description
        assembs.append(ass_dict)

    LOG.INFO("Zakonczylem pobieranie wszystkich typow asemblacji z organizmu: " + str(organism_id))
    return assembs

def getAssembsDict():
    LOG.INFO("Rozpoczynam pobieranie wszystkich typow asemblacji - wersja dict.")
    assembs = []
    assembs_db = Assemb.objects.all();
    for ass in assembs_db:
        assemb = {}
        assemb['ID'] = ass.id;
        assemb['NAME'] = ass.name;
        assemb['DESC'] = ass.description;
        scaff_count = Scaffold.objects.filter(assemb_type=ass.id).count()
        assemb['SCAFF_COUNT'] = scaff_count;
        assembs.append(assemb)
    LOG.INFO("Zakonczylem pobieranie wszystkich typow asemblacji - wersja dict.")
    return assembs

def getAssembsDictFromOrganism(organism_id):
    LOG.INFO("Rozpoczynam pobieranie wszystkich typow asemblacji - wersja dict z organizmu: " + str(organism_id))
    assembs = []
    assembs_db = getAssembsFromOrganism(organism_id)
    for ass in assembs_db:
        assemb = {}
        assemb['ID'] = ass['id'];
        assemb['NAME'] = ass['name'];
        assemb['DESC'] = ass['description'];
        scaff_count = Scaffold.objects.filter(assemb_type=ass['id']).count()
        assemb['SCAFF_COUNT'] = scaff_count;
        assembs.append(assemb)
    LOG.INFO("Zakonczylem pobieranie wszystkich typow asemblacji - wersja dict z organizmu: " + str(organism_id))
    return assembs

def updateAssembs(new_assembs, org_id):
    LOG.INFO("Rozpoczynam uaktualnianie wszystkich typow asemblacji dla organizmu: " + str(org_id))
    LOG.DEBUG("Nowe typy asemblacji: " + str(new_assembs))

    new_assembs_tmp_dict = {}
    added_assembs = []
    # DODANIE
    for new_ass in new_assembs:
        try:
            # Jezeli ID = -1 -> dodajemy
            if int(new_ass['ID']) == -1:
                LOG.DEBUG("Dodaje nowy typ asemblacji: " + str(new_ass['NAME']))
                a = Assemb(name = new_ass['NAME'], description = new_ass['DESC'], organism_id = int(org_id))
                a.save()
                new_ass['ID'] = str(a.id)
                added_assembs.append(new_ass['ID'])
                
                # Dodanie odpowiednich ChromosomeLength
                LOG.DEBUG("Dodaje odpowiednie wpisy w ChromosomeLength.")
                chromosomes = Chromosome.objects.all().filter(organism_id = int(org_id))
                LOG.DEBUG("Wszystkie chromosomy organizmu: " + str(org_id) + ": " + str(chromosomes))
                for chromosome_obj in chromosomes:
                    LOG.DEBUG("Dodaje nowa dlugosc chromosomu " + str(chromosome_obj.id) + " dla typu asemblacji: " + str(new_ass['NAME']))
                    chr_len_new = ChromosomeLength(chr_id=chromosome_obj.id, assemb_id=a.id, length=0.0)
                    chr_len_new.save()
                    LOG.DEBUG("Dodalem nowa dlugosc chromosomu dla typu asemblacji: " + str(new_ass['NAME']) + " --> " + str(chr_len_new.id))
                
            # Jezeli nie -> dodajemy do new_assembs_tmp_dict, zeby ponizszy for byl wydajniejszy
            else:
                new_assembs_tmp_dict[int(new_ass['ID'])] = {'NAME' : new_ass['NAME'], 'DESC' : new_ass['DESC']}
        except Exception:
            LOG.WARN("Blad podczas dodawania nowych typow asemblacji.")
            return None
            
    # UAKTUALNIENIE / USUNIECIE
    assembs_db = Assemb.objects.filter(organism_id = int(org_id));
    LOG.DEBUG("Typy asemblacji w bazie przed modyfikacja oraz usuwaniem: " + str(assembs_db))
    try:
        for ass in assembs_db:
            # Jezeli istnieje w slowniku -> uaktualniamy name i desc
            if new_assembs_tmp_dict.has_key(int(ass.id)):
                LOG.DEBUG("Uaktualniam typ asemblacji: " + str(ass))
                ass.name = new_assembs_tmp_dict[int(ass.id)]['NAME']
                ass.description = new_assembs_tmp_dict[int(ass.id)]['DESC']
                ass.save()
            # Jezeli nie ma w slowniku i w nowo dodanych -> usuwamy
            else:
                LOG.DEBUG("Probuje usunac typ asemblacji: " + str(ass))
                if str(ass.id) not in added_assembs:
                    LOG.DEBUG("Usuwam typ asemblacji: " + str(ass))
                    ass.delete()
    except ValueError:
        LOG.WARN("Blad podczas dodawania nowych typow asemblacji (ValueError).")
        return None

    LOG.INFO("Zakonczylem uaktualnianie wszystkich typow asemblacji.")
    return new_assembs

def deleteChromosome(chr_id):
    LOG.INFO("Rozpoczynam usuwanie chromosomu o ID: " + str(chr_id))
    try:
        chr = Chromosome.objects.get(id = int(chr_id))
    except Chromosome.DoesNotExist:
        LOG.WARN("Brak chromosomu o ID: " + str(chr_id))
        return None
    chr.delete()
    
    LOG.DEBUG("Usuwam wszystkie dlugosci chromosomow z chromosomu: " + str(chr_id))
    # Usuniecie wszystkich ChromosomeLength
    try:
        ChromosomeLength.objects.filter(chr_id = int(chr_id)).delete()
    except Exception:
        LOG.DEBUG("Brak dlugosci chromosomu: " + str(chr_id))
    
    LOG.DEBUG("Usuwam wszystkie scaffoldy wraz z contigami z chromosomu: " + str(chr_id))
    # Usuniecie wszystkich Scaffoldow, ScaffoldPositions oraz Contigs
    scaffs = Scaffold.objects.filter(chromosome_id = int(chr_id))
    for scaff in scaffs:
        deleteScaffold(scaff.id, True)
    
    LOG.INFO("Zakonczylem usuwanie chromosomu o ID: " + str(chr_id))