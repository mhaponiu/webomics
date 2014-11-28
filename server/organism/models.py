from django.db import models

class Organism(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __unicode__(self):
        return str(self.id) + " --> " + str(self.name) + "; " + str(self.description)
