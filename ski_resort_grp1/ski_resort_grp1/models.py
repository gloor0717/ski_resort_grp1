from django.contrib.gis.db import models

class SkiRoute(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    geometry = models.LineStringField()

    def __str__(self):
        return self.name

class SkiLift(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    geometry = models.LineStringField()

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    geometry = models.PointField()

    def __str__(self):
        return self.name

class BusStation(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.PointField()

    def __str__(self):
        return self.name
