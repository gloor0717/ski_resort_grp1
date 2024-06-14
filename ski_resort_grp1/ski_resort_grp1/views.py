from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import SkiRoute, SkiLift, Restaurant, BusStation

def index(request):
    return render(request, 'ski_resort_grp1/index.html')

def map_view(request):
    return render(request, 'ski_resort_grp1/map.html')

def ski_routes(request):
    ski_routes = SkiRoute.objects.all()
    return render(request, 'ski_resort_grp1/ski_routes.html', {'ski_routes': ski_routes})

def ski_lifts(request):
    ski_lifts = SkiLift.objects.all()
    return render(request, 'ski_resort_grp1/ski_lifts.html', {'ski_lifts': ski_lifts})

def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'ski_resort_grp1/restaurants.html', {'restaurants': restaurants})

def bus_stations(request):
    bus_stations = BusStation.objects.all()
    return render(request, 'ski_resort_grp1/bus_stations.html', {'bus_stations': bus_stations})

def ski_lifts_geojson(request):
    ski_lifts = SkiLift.objects.all()
    ser = serialize('geojson', ski_lifts, geometry_field='geometry', fields=('name', 'type'))
    return HttpResponse(ser, content_type='application/json')

def ski_routes_geojson(request):
    ski_routes = SkiRoute.objects.all()
    ser = serialize('geojson', ski_routes, geometry_field='geometry', fields=('name', 'difficulty'))
    return HttpResponse(ser, content_type='application/json')

def restaurants_geojson(request):
    restaurants = Restaurant.objects.all()
    ser = serialize('geojson', restaurants, geometry_field='geometry', fields=('name', 'website'))
    return HttpResponse(ser, content_type='application/json')

def bus_stations_geojson(request):
    bus_stations = BusStation.objects.all()
    ser = serialize('geojson', bus_stations, geometry_field='geometry', fields=('name'))
    return HttpResponse(ser, content_type='application/json')

def weather(request):
    return render(request, 'ski_resort_grp1/weather.html')
