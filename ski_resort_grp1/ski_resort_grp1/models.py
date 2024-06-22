from django.contrib.gis.db import models

class SkiRoute(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    geometry = models.MultiLineStringField()

    def __str__(self):
        return self.name
    
class SkiLift(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    state = models.BooleanField()
    geometry = models.LineStringField()

    def __str__(self):
        return self.name
    
class Parking(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    geometry = models.PolygonField()

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    geometry = models.PolygonField()

    def __str__(self):
        return self.name

class BusStation(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.PointField()

    def __str__(self):
        return self.name
    
class BaseStation(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    schedule = models.CharField(max_length=100)
    geometry = models.PolygonField()

    def __str__(self):
        return self.name
