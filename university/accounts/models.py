from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name
    
from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    total_programs = models.IntegerField()
    approximate_students = models.IntegerField()
    naac_grade = models.CharField(max_length=10)
    website = models.URLField()
    contact_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
