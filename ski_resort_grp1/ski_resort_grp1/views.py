import json
from urllib.error import HTTPError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .models import BusStation, Restaurant, SkiRoute, SkiLift, BaseStation, Parking
from django.core.serializers import serialize
from django.contrib.gis.geos import Point, LineString, MultiLineString
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db.models.functions import Distance

def index(request):
    # Fetch data for the ski lifts, bus stations, ski routes, and restaurants
    ski_lifts = SkiLift.objects.all()
    bus_stations = BusStation.objects.all()
    ski_routes = SkiRoute.objects.all()
    restaurants = Restaurant.objects.all()

    # Fetch weather data (replace with your actual weather API call)
    weather_data = None
    try:
        api_key = 'eda0603a64034145873152333241506'
        city = 'Ayent'
        city_encoded = quote_plus(city)
        weather_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_encoded}&days=7&aqi=no&alerts=no'
        
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
        'ski_lifts': ski_lifts,
        'bus_stations': bus_stations,
        'ski_routes': ski_routes,
        'restaurants': restaurants,
        'weather_data': weather_data,
    }
    
    return render(request, 'ski_resort_grp1/index.html', context)

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

def parkings(request):
    parkings = Parking.objects.all()
    return render(request, 'ski_resort_grp1/parkings.html', {'parkings': parkings})

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
    ser = serialize('geojson', bus_stations, geometry_field='geometry', fields=('name',))
    return HttpResponse(ser, content_type='application/json')

def base_stations_geojson(request):
    base_stations = BaseStation.objects.all()
    ser = serialize('geojson', base_stations, geometry_field='geometry', fields=('name', 'type', 'schedule'))
    return HttpResponse(ser, content_type='application/json')

def parkings_geojson(request):
    parkings = Parking.objects.all()
    ser = serialize('geojson', parkings, geometry_field='geometry', fields=('name', 'capacity'))
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

        start_point = Point(start_x, start_y, srid=4326)
        end_point = Point(end_x, end_y, srid=4326)

        start_base_station = BaseStation.objects.filter(geometry__contains=start_point).first()
        start_restaurant = Restaurant.objects.filter(geometry__contains=start_point).first()

        end_base_station = BaseStation.objects.filter(geometry__contains=end_point).first()
        end_restaurant = Restaurant.objects.filter(geometry__contains=end_point).first()

        if not start_base_station and not start_restaurant:
            return JsonResponse({'error': 'Start point not within any base station or restaurant'}, status=400)
        if not end_base_station and not end_restaurant:
            return JsonResponse({'error': 'End point not within any base station or restaurant'}, status=400)

        start_geometry = start_base_station.geometry if start_base_station else start_restaurant.geometry
        end_geometry = end_base_station.geometry if end_base_station else end_restaurant.geometry

        path = find_connected_routes_and_lifts(start_geometry, end_geometry)

        if path:
            path_geojson = json.loads(path.geojson)
            return JsonResponse({'type': 'Feature', 'geometry': path_geojson, 'properties': {}}, safe=False)
        else:
            return JsonResponse({'error': 'No path found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
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
