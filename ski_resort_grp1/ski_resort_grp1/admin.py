from django.contrib.gis import admin
from .models import SkiRoute, WeatherStation, Amenity

admin.site.register(SkiRoute, admin.OSMGeoAdmin)
admin.site.register(WeatherStation, admin.OSMGeoAdmin)
admin.site.register(Amenity, admin.OSMGeoAdmin)
