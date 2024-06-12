from django.contrib.gis.db import models

class SkiRoute(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    length = models.FloatField(help_text="Length in kilometers")
    geometry = models.LineStringField()

    def __str__(self):
        return self.name

class WeatherStation(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.PointField()
    temperature = models.FloatField()
    wind_speed = models.FloatField()

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    geometry = models.PointField()

    def __str__(self):
        return self.name
