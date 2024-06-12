from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import SkiRoute, WeatherStation, Amenity

def index(request):
    return HttpResponse("Welcome to the Anzère Ski Resort")

def map_view(request):
    return render(request, 'ski_resort_grp1/map.html')

def ski_routes(request):
    ski_routes = SkiRoute.objects.all()
    ser = serialize('geojson', ski_routes, geometry_field='geometry', fields=('name', 'difficulty', 'length'))
    return HttpResponse(ser, content_type='application/json')

def weather_stations(request):
    weather_stations = WeatherStation.objects.all()
    ser = serialize('geojson', weather_stations, geometry_field='geometry', fields=('name', 'temperature', 'wind_speed'))
    return HttpResponse(ser, content_type='application/json')

def amenities(request):
    amenities = Amenity.objects.all()
    ser = serialize('geojson', amenities, geometry_field='geometry', fields=('name', 'type'))
    return HttpResponse(ser, content_type='application/json')
