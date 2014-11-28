import random
import sys, os

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..', '..')
sys.path.append(server_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

from server.scaffold.models import Scaffold, ScaffoldPosition

SCAFFOLDS_COUNT = 5
RATE = 2

s_id = 0

chromosomes = [450000, 340000, 600000, 340000, 450000, 470000, 310000]

for i, chr_len in enumerate(chromosomes):
    scaffold_area_len = chr_len / (SCAFFOLDS_COUNT * RATE)
    print "Area LEN: ", scaffold_area_len
    k = 0
    while k < SCAFFOLDS_COUNT * RATE:
        sequence = "GGUUUTTCCCCUUTCCCGGGG"
        assemb = random.randint(0, 1)
        print "k = ", k
        print "Area: ", k * scaffold_area_len, " - ", (k + RATE) * scaffold_area_len
        start_pos = random.randint(k * scaffold_area_len, (k + 1) * scaffold_area_len) # losujemy z pierwszej polowki przedzialu
        end_pos = random.randint((k + RATE - 2) * scaffold_area_len, (k + RATE - 1) * scaffold_area_len) # losujemy z drugiej polowki przedzialu
        print "Start: ", start_pos
        print "Stop: ", end_pos
        print assemb

        # Utworzenie obiektu Scaffold
        scaffold = Scaffold(id = s_id, chromosome_id = i + 1, sequence = sequence, assemb_type = assemb)
        scaffold.save()
        scaffold_pos = ScaffoldPosition(scaff_id = s_id, start = start_pos, end = end_pos)
        scaffold_pos.save()
        s_id += 1

        start = random.randint((k + 1) * scaffold_area_len, (k + 2) * scaffold_area_len) # losujemy z pierwszej polowki przedzialu
        end = random.randint((k + RATE - 1) * scaffold_area_len, (k + RATE) * scaffold_area_len) # losujemy z drugiej polowki przedzialu
        print "Start: ", start_pos
        print "Stop: ", end_pos
        if assemb == 1:
            assemb = 0
        else:
            assemb = 1
        print assemb

        # Utworzenie obiektu Scaffold
        scaffold = Scaffold(id = s_id, chromosome_id = i + 1, sequence = sequence, assemb_type = assemb)
        scaffold.save()
        scaffold_pos = ScaffoldPosition(scaff_id = s_id, start = start_pos, end = end_pos)
        scaffold_pos.save()
        s_id += 1

        k += 4
