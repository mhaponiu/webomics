from django.db import models

class Chromosome(models.Model):
    name = models.CharField(max_length = 50)
    organism_id = models.IntegerField()

    def __unicode__(self):
        return self.name + " -> " + str(self.organism_id)

class ChromosomeLength(models.Model):
    chr_id = models.IntegerField()
    assemb_id = models.IntegerField()
    length = models.FloatField()
    
    def __unicode__(self):
        return str(self.chr_id) + "; " + str(self.assemb_id) + " --> " + str(self.length)

class Assemb(models.Model):
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    organism_id = models.IntegerField()
    
    def __unicode__(self):
        return self.name + "; " + self.description + " -> " + str(self.organism_id)