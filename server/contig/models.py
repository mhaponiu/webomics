from django.db import models

class Contig(models.Model):
    id = models.IntegerField(primary_key = True)
    scaff_id = models.TextField()
    order = models.IntegerField()
    start = models.IntegerField()
    end = models.IntegerField()
    sequence = models.TextField()
    length_bp = models.FloatField()
    
#
#    def __init__(self, id_, scaff_id, order, start, end, sequence, length_bp):
#        self.id = id_
#        self.scaff_id = scaff_id
#        self.order = order
#        self.start = start
#        self.end = end
#        self.sequence = sequence
#        self.length_bp = length_bp

    def __unicode__(self):
        return str(self.id) + " --> " + str(self.scaff_id) + "; " + str(self.order) + "; " + str(self.start) + "; " + str(self.end) + "; " + str(self.length_bp)

class ContigWrap(models.Model):
    id = models.IntegerField(primary_key = True)
    scaff_id = models.TextField()
    order = models.IntegerField()
    start = models.IntegerField()
    end = models.IntegerField()
    sequence = models.TextField()
    length_bp = models.FloatField()

    def __init__(self, id_, scaff_id, order, start, end, sequence, length_bp):
        self.id = id_
        self.scaff_id = scaff_id
        self.order = order
        self.start = start
        self.end = end
        self.sequence = sequence
        self.length_bp = length_bp

    def __unicode__(self):
        return str(self.id) + " --> " + str(self.scaff_id) + "; " + str(self.order) + "; " + str(self.start) + "; " + str(self.end) + "; " + str(self.length_bp)

    def __str__(self):
        return str(self.id) + " --> " + str(self.scaff_id) + "; " + str(self.order) + "; " + str(self.start) + "; " + str(self.end) + "; " + str(self.length_bp)
