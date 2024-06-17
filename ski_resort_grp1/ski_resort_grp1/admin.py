from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import SkiRoute, SkiLift, Restaurant, BusStation, BaseStation

@admin.register(SkiRoute)
class SkiRouteAdmin(LeafletGeoAdmin):
    list_display = ('name', 'difficulty')
    settings_overrides = {
        'DEFAULT_CENTER': (46.31415226088029, 7.402238579358967),
        'DEFAULT_ZOOM': 13,
        'TILES': [
            ('OpenStreetMap', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
            ('OpenSnowMap', 'https://tiles.opensnowmap.org/pistes/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.opensnowmap.org/iframes/data.html">www.opensnowmap.org</a> <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
        ],
    }

@admin.register(SkiLift)
class SkiLiftAdmin(LeafletGeoAdmin):
    list_display = ('name', 'type')
    settings_overrides = {
        'DEFAULT_CENTER': (46.31415226088029, 7.402238579358967),
        'DEFAULT_ZOOM': 13,
        'TILES': [
            ('OpenStreetMap', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
            ('OpenSnowMap', 'https://tiles.opensnowmap.org/pistes/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.opensnowmap.org/iframes/data.html">www.opensnowmap.org</a> <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
        ],
    }

@admin.register(Restaurant)
class RestaurantAdmin(LeafletGeoAdmin):
    list_display = ('name', 'website')
    settings_overrides = {
        'DEFAULT_CENTER': (46.31415226088029, 7.402238579358967),
        'DEFAULT_ZOOM': 13,
        'TILES': [
            ('OpenStreetMap', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
            ('OpenSnowMap', 'https://tiles.opensnowmap.org/pistes/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.opensnowmap.org/iframes/data.html">www.opensnowmap.org</a> <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
        ],
    }

@admin.register(BusStation)
class BusStationAdmin(LeafletGeoAdmin):
    list_display = ('name',)
    settings_overrides = {
        'DEFAULT_CENTER': (46.31415226088029, 7.402238579358967),
        'DEFAULT_ZOOM': 13,
        'TILES': [
            ('OpenStreetMap', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
            ('OpenSnowMap', 'https://tiles.opensnowmap.org/pistes/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.opensnowmap.org/iframes/data.html">www.opensnowmap.org</a> <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
        ],
    }

@admin.register(BaseStation)
class BaseStationAdmin(LeafletGeoAdmin):
    list_display = ('name',)
    settings_overrides = {
        'DEFAULT_CENTER': (46.31415226088029, 7.402238579358967),
        'DEFAULT_ZOOM': 13,
        'TILES': [
            ('OpenStreetMap', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
            ('OpenSnowMap', 'https://tiles.opensnowmap.org/pistes/{z}/{x}/{y}.png', {'attribution': 'Map data: &copy; <a href="https://www.opensnowmap.org/iframes/data.html">www.opensnowmap.org</a> <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
        ],
    }
