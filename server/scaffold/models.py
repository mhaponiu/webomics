from django.db import models

class Scaffold(models.Model):
    id = models.TextField(primary_key = True)
    chromosome_id = models.IntegerField()
    sequence = models.TextField()
    assemb_type = models.IntegerField() # 0 - Arachne, 1 - Celera
    length_bp = models.FloatField()

    def __unicode__(self):
        return str(self.id) + "; " + str(self.chromosome_id) + "; " + str(self.assemb_type) + "; " + str(self.length_bp)

class ScaffoldPosition(models.Model):
    scaff_id = models.TextField()
    start = models.FloatField()
    end = models.FloatField()
    order = models.IntegerField()

    def __unicode__(self):
        return str(self.scaff_id) + "; " + str(self.start) + "; " + str(self.end) + " --> " + str(self.order)

    def __str__(self):
        return str(self.scaff_id) + "; " + str(self.start) + "; " + str(self.end) + " --> " + str(self.order)


class ScaffoldWrap(models.Model):
    id = models.TextField(primary_key = True)
    scaff_id = models.TextField()
    chromosome_id = models.IntegerField()
    sequence = models.TextField()
    assemb_type = models.IntegerField()
    start = models.FloatField()
    end = models.FloatField()
    color = models.TextField()
    order = models.IntegerField()
    length_bp = models.FloatField()

    def __init__(self, id_, scaff_id, chrom_id, seq, ass_type, start, end, color, order, length_bp):
        self.id = id_
        self.scaff_id = scaff_id
        self.chromosome_id = chrom_id
        self.sequence = seq
        self.assemb_type = ass_type
        self.start = start
        self.end = end
        self.color = color
        self.order = order
        self.length_bp = length_bp

    def __str__(self):
        return str(self.id) + "; " + str(self.scaff_id) + "; " + str(self.chromosome_id) + "; " + str(self.assemb_type) + "; " + str(self.start) + "; " + str(self.end) + "; " + str(self.color) + "; " + str(self.length_bp) + " --> " + str(self.order)

    def __unicode__(self):
        return str(self.id) + "; " + str(self.scaff_id) + "; " + str(self.chromosome_id) + "; " + str(self.assemb_type) + "; " + str(self.start) + "; " + str(self.end) + "; " + str(self.color) + "; " + str(self.length_bp) + " --> " + str(self.order)

class UndefinedScaffold(models.Model):
    id = models.IntegerField(primary_key = True)
    scaff_id = models.IntegerField()
    sequence = models.TextField()
    length = models.FloatField()    # z dziurami
    assemb_type = models.IntegerField() # 0 - Arachne, 1 - Celera

    def __str__(self):
        return str(self.id) + "; " + str(self.sequence) + "; " + str(self.length) + "; " + str(self.assemb_type)

    def __unicode__(self):
        return str(self.id) + "; " + str(self.sequence) + "; " + str(self.length) + "; " + str(self.assemb_type)


class UndefinedScaffoldWrap(models.Model):
    id = models.IntegerField(primary_key = True)
    scaff_id = models.IntegerField()
    sequence = models.TextField()
    start_bp = models.FloatField()
    end_bp = models.FloatField()
    length_all_bp = models.FloatField()
    order = models.FloatField()
    assemb_type = models.IntegerField() # 0 - Arachne, 1 - Celera

    def __init__(self, id_, scaff_id, seq, start, end, length, order, assemb_type):
        self.id = id_
        self.scaff_id = scaff_id
        self.sequence = seq
        self.start_bp = start
        self.end_bp = end
        self.length_all_bp = length
        self.order = order
        self.assemb_type = assemb_type

    def __str__(self):
        return str(self.id) + "; " + str(self.scaff_id) + "; " + str(self.start_bp) + "; " + str(self.end_bp) + "; " + str(self.length_all_bp) + " --> " + str(self.order) + "; " + str(self.assemb_type)

    def __unicode__(self):
        return str(self.id) + "; " + str(self.scaff_id) + "; " + str(self.start_bp) + "; " + str(self.end_bp) + "; " + str(self.length_all_bp) + " --> " + str(self.order) + "; " + str(self.assemb_type)
