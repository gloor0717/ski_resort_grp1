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
from django.http import JsonResponse
from .models import SkiRoute, SkiLift
from django.contrib.gis.geos import Point, MultiLineString, LineString
from django.contrib.gis.db.models.functions import Distance

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

def find_connected_routes_and_lifts(start_geometry, end_geometry):
    routes = SkiRoute.objects.all()
    lifts = SkiLift.objects.all()

    path = []
    visited_routes = set()
    visited_lifts = set()

    def find_path(current_geometry, target_geometry):
        nonlocal path
        while True:
            nearest_route = routes.filter(geometry__intersects=current_geometry).exclude(id__in=visited_routes).annotate(distance=Distance('geometry', current_geometry)).order_by('distance').first()
            nearest_lift = lifts.filter(geometry__intersects=current_geometry).exclude(id__in=visited_lifts).annotate(distance=Distance('geometry', current_geometry)).order_by('distance').first()

            if not nearest_route and not nearest_lift:
                break

            if nearest_route and (not nearest_lift or nearest_route.distance < nearest_lift.distance):
                segment = nearest_route.geometry
                visited_routes.add(nearest_route.id)
            else:
                segment = nearest_lift.geometry
                visited_lifts.add(nearest_lift.id)

            path.append(segment)
            current_geometry = segment

            if current_geometry.intersects(target_geometry):
                path.append(target_geometry)
                return True

        return False

    if find_path(start_geometry, end_geometry):
        return MultiLineString(path, srid=4326)
    else:
        return None
    
def shortest_path_view(request):
    try:
        start_x = float(request.GET.get('start_x'))
        start_y = float(request.GET.get('start_y'))
        end_x = float(request.GET.get('end_x'))
        end_y = float(request.GET.get('end_y'))

        start_point = Point(start_x, start_y, srid=4326)  # Convertir en Point
        end_point = Point(end_x, end_y, srid=4326)        # Convertir en Point

        start_polygon = BaseStation.objects.filter(geometry__contains=start_point).first() or Restaurant.objects.filter(geometry__contains=start_point).first()
        end_polygon = BaseStation.objects.filter(geometry__contains=end_point).first() or Restaurant.objects.filter(geometry__contains=end_point).first()

        if not start_polygon or not end_polygon:
            return JsonResponse({'error': 'Start or end point not within any base station or restaurant'}, status=400)

        path = find_connected_routes_and_lifts(start_polygon.geometry, end_polygon.geometry)

        if path:
            return JsonResponse({'type': 'Feature', 'geometry': path.geojson, 'properties': {}}, safe=False)
        else:
            return JsonResponse({'error': 'No path found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)