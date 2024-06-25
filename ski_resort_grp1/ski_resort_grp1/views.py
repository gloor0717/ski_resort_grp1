import json
from urllib.error import HTTPError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .utils import build_ski_resort_graph, find_route
from .models import BusStation, Restaurant, SkiRoute, SkiLift, BaseStation
from django.core.serializers import serialize
from shapely.geometry import Point


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

def base_stations(request):
    base_stations = BaseStation.objects.all()
    return render(request, 'ski_resort_grp1/base_stations.html', {'base_stations': base_stations})

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

def base_stations_geojson(request):
    base_stations = BaseStation.objects.all()
    ser = serialize('geojson', base_stations, geometry_field='geometry', fields=('name'))
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

def get_first_coordinate(geometry):
    if geometry.geom_type == 'Point':
        return geometry
    elif geometry.geom_type in ['LineString', 'Polygon']:
        return Point(geometry.coords[0])
    else:
        raise ValueError(f"Unsupported geometry type: {geometry.geom_type}")

def calculate_route(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_id = data.get('start_id')
        end_id = data.get('end_id')
        start_type = data.get('start_type')
        end_type = data.get('end_type')
        
        # Get start object
        start_object = None
        if start_type == 'ski_route':
            start_object = get_object_or_404(SkiRoute, id=start_id)
        elif start_type == 'ski_lift':
            start_object = get_object_or_404(SkiLift, id=start_id)
        elif start_type == 'base_station':
            start_object = get_object_or_404(BaseStation, id=start_id)
        
        # Get end object
        end_object = None
        if end_type == 'ski_route':
            end_object = get_object_or_404(SkiRoute, id=end_id)
        elif end_type == 'ski_lift':
            end_object = get_object_or_404(SkiLift, id=end_id)
        elif end_type == 'base_station':
            end_object = get_object_or_404(BaseStation, id=end_id)

        if not start_object or not end_object:
            return JsonResponse({"error": "Invalid start or end object"})

        try:
            start_point = Point(start_object.geometry.centroid.x, start_object.geometry.centroid.y)
            end_point = Point(end_object.geometry.centroid.x, end_object.geometry.centroid.y)
        except Exception as e:
            return JsonResponse({"error": str(e)})

        graph = build_ski_resort_graph()
        path = find_route(graph, (start_point.x, start_point.y), (end_point.x, end_point.y))

        if path:
            return JsonResponse({"path": path})
        else:
            return JsonResponse({"error": "No path found"})
    
    ski_routes = SkiRoute.objects.all()
    ski_lifts = SkiLift.objects.all()
    base_stations = BaseStation.objects.all()
    
    context = {
        'ski_routes': ski_routes,
        'ski_lifts': ski_lifts,
        'base_stations': base_stations
    }
    return render(request, 'ski_resort_grp1/calculate_route.html', context)