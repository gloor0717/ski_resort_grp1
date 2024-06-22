from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
import json
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from urllib.error import HTTPError
from .models import SkiRoute, SkiLift, Parking, Restaurant, BusStation, BaseStation
from itertools import groupby
from operator import attrgetter

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

def parkings(request):
    parkings = Parking.objects.all()
    return render(request, 'ski_resort_grp1/parkings.html', {'parkings': parkings})

def restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'ski_resort_grp1/restaurants.html', {'restaurants': restaurants})

def bus_stations(request):
    bus_stations = BusStation.objects.all()
    return render(request, 'ski_resort_grp1/bus_stations.html', {'bus_stations': bus_stations})

def base_stations(request):
    base_stations = BaseStation.objects.all().order_by('name')
    grouped_stations = {k: list(v) for k, v in groupby(base_stations, key=attrgetter('name'))}
    return render(request, 'ski_resort_grp1/base_stations.html', {'grouped_stations': grouped_stations})
    

def ski_lifts_geojson(request):
    ski_lifts = SkiLift.objects.all()
    ser = serialize('geojson', ski_lifts, geometry_field='geometry', fields=('name', 'type', 'state'))
    return HttpResponse(ser, content_type='application/json')

def ski_routes_geojson(request):
    ski_routes = SkiRoute.objects.all()
    ser = serialize('geojson', ski_routes, geometry_field='geometry', fields=('name', 'difficulty'))
    return HttpResponse(ser, content_type='application/json')

def parkings_geojson(request):
    parkings = Parking.objects.all()
    ser = serialize('geojson', parkings, geometry_field='geometry', fields=('name', 'capacity'))
    return HttpResponse(ser, content_type='application/json')

def restaurants_geojson(request):
    restaurants = Restaurant.objects.all()
    ser = serialize('geojson', restaurants, geometry_field='geometry', fields=('name', 'website'))
    return HttpResponse(ser, content_type='application/json')

def bus_stations_geojson(request):
    bus_stations = BusStation.objects.all()
    ser = serialize('geojson', bus_stations, geometry_field='geometry', fields=('name',))
    return HttpResponse(ser, content_type='application/json')

def base_stations_geojson(request):
    base_stations = BaseStation.objects.all()
    ser = serialize('geojson', base_stations, geometry_field='geometry', fields=('name', 'type', 'schedule'))
    return HttpResponse(ser, content_type='application/json')

def weather(request):
    api_key = 'eda0603a64034145873152333241506'
    city = 'Ayent'
    city_encoded = quote_plus(city)
    weather_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_encoded}&days=7&aqi=no&alerts=no'
    
    try:
        req = Request(weather_url)
        with urlopen(req) as response:
            response_data = response.read()
            encoding = response.info().get_content_charset('utf-8')
            weather_data = json.loads(response_data.decode(encoding))
    except HTTPError as e:
        error_message = e.read().decode()
        return HttpResponse(f"HTTP error: {e.code}. Response: {error_message}", status=e.code)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
    context = {
        'weather_data': weather_data
    }
    return render(request, 'ski_resort_grp1/weather.html', context)

def transport(request):
    from_station = request.GET.get('from', 'Anzere')
    to_station = request.GET.get('to', 'Sion')
    date = request.GET.get('date')
    time = request.GET.get('time')

    from_station_encoded = quote_plus(from_station)
    to_station_encoded = quote_plus(to_station)
    transport_url = f'https://transport.opendata.ch/v1/connections?from={from_station_encoded}&to={to_station_encoded}'
    
    if date:
        transport_url += f'&date={date}'
    if time:
        transport_url += f'&time={time}'

    try:
        req = Request(transport_url)
        with urlopen(req) as response:
            response_data = response.read()
            encoding = response.info().get_content_charset('utf-8')
            transport_data = json.loads(response_data.decode(encoding))
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

    context = {
        'transport_data': transport_data
    }
    return render(request, 'ski_resort_grp1/transport.html', context)