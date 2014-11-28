from django.db import models

class Marker(models.Model):
    name = models.TextField()
    chr_id = models.IntegerField()
    pos_cm = models.FloatField()
    cont_id = models.IntegerField()
    contig_start = models.FloatField()
    contig_end = models.FloatField()
    scaff_id = models.TextField()
    scaffold_start = models.FloatField()
    scaffold_end = models.FloatField()
    sequence = models.TextField()

    def __unicode__(self):
        return self.name + "; " + str(self.chr_id) + "; " + str(self.contig_start) + "; " + str(self.contig_end)

class MarkerWrap(models.Model):
    name = models.TextField()
    chr_id = models.IntegerField()
    pos_cm = models.FloatField()
    cont_id = models.IntegerField()
    contig_start = models.FloatField()
    contig_end = models.FloatField()
    scaff_id = models.TextField()
    scaffold_start = models.FloatField()
    scaffold_end = models.FloatField()
    sequence = models.TextField()

    def __init__(self, name, chr_id, pos_cm, cont_id, contig_start, contig_end, scaff_id, scaffold_start, scaffold_end, sequence):
        self.name = name
        self.chr_id = chr_id
        self.pos_cm = pos_cm
        self.cont_id = cont_id
        self.contig_start = contig_start
        self.contig_end = contig_end
        self.scaff_id = scaff_id
        self.scaffold_start = scaffold_start
        self.scaffold_end = scaffold_end
        self.sequence = sequence

    def __unicode__(self):
        return self.name + "; " + str(self.chr_id) + "; " + str(self.contig_start) + "; " + str(self.contig_end)

    def __str__(self):
        return self.name + "; " + str(self.chr_id) + "; " + str(self.contig_start) + "; " + str(self.contig_end)
