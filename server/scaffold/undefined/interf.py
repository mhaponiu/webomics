from django.db.models import Q
from django.db.models import Max, Min
from server.scaffold.models import UndefinedScaffold, UndefinedScaffoldWrap
from server.config import static

import logging
logger = logging.getLogger('cgb')  # logger z settings.py

def getMaxLength(shown_types, start, end):
    print "Sprawdzam max dlugosc niezdefiniowanych scaffoldow (", shown_types, ") od", start, "do", end
    max_len = 0.0

    for ass_type in shown_types:
        curr_max = UndefinedScaffold.objects.all().filter(assemb_type = ass_type).filter(scaff_id__range = (start, end)).aggregate(Max('length'))
        if curr_max['length__max'] > max_len and curr_max['length__max'] != None:
            max_len = curr_max['length__max']

    print "\tMax dlugosc niezdefiniowanych scaffoldow wynosi:" , max_len
    return max_len

def getMaxID(shown_types):
    print "Sprawdzam max ID niezdefiniowanych scaffoldow (", shown_types, ")"
    max_id = 0.0
    
    for ass_type in shown_types:
        curr_max_id = UndefinedScaffold.objects.all().filter(assemb_type = ass_type).aggregate(Max('scaff_id'))
        if curr_max_id['scaff_id__max'] > max_id and curr_max_id['scaff_id__max'] != None:
            max_id = curr_max_id['scaff_id__max']
    
    print "\tMax ID niezdefiniowanych scaffoldow wynosi:" , max_id
    return max_id

def getMinID(shown_types):
    print "Sprawdzam min ID niezdefiniowanych scaffoldow (", shown_types, ")"
    import sys
    min_id = sys.float_info.max

    for ass_type in shown_types:
        curr_min_id = UndefinedScaffold.objects.all().filter(assemb_type = ass_type).aggregate(Min('scaff_id'))
        if curr_min_id['scaff_id__min'] < min_id and curr_min_id['scaff_id__min'] != None:
            min_id = curr_min_id['scaff_id__min']
    
    if min_id == float("inf"):
        min_id = 0.0

    print "\tMin ID niezdefiniowanych scaffoldow wynosi:" , min_id
    return min_id

def getScaffolds(shown_types, start, end):
    print "Pobieram niezdefiniowane scaffoldy (", shown_types, ") od", start, "do", end
    scaffolds_return = []
    # Wszystkie niezdefiniowane scaffoldy
    scaffolds = UndefinedScaffold.objects.all().filter(scaff_id__range = (start, end))

    i = 0
    for scaff in scaffolds:
        if scaff.assemb_type in shown_types:
            # Podzielic dany scaffold na UndeffinedScaffoldWrap, wzgledem dziur NNNNN
            new_seq = scaff.sequence + "N"
            last_gap_pos = -1
            found = new_seq.find("N")
    
            while found != -1:
                # N z przodu (jedna lub kilka) lub dowolna grupa N
                if last_gap_pos + 1 != found:
                    # Kawalek scaffolda
                    found_scaff_seq = new_seq[last_gap_pos + 1:found - 1]
                    scaffold_wrap = UndefinedScaffoldWrap(i, scaff.scaff_id, scaff.sequence, last_gap_pos + 1, found - 1, scaff.length, scaff.id, scaff.assemb_type)
                    scaffolds_return.append(scaffold_wrap)
    
                    print "\t\tFRAG ", scaff.id, " (", scaff.scaff_id, ") od", last_gap_pos + 1, "do", found - 1
    
                last_gap_pos = found
                found = new_seq.find("N", found + 1)
    
                # Lecimy na kolejny scaffold
                i += 1

    #print "\nIlosc zwracanych scaffoldow: ", len(scaffolds_return)
    #for scaff_ret in scaffolds_return:
    #    print "\t\t", scaff_ret

    return scaffolds_return
