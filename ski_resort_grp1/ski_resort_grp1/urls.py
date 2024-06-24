from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('map/', views.map_view, name='map'),
    path('ski_routes/', views.ski_routes, name='ski_routes'),
    path('ski_lifts/', views.ski_lifts, name='ski_lifts'),
    path('parkings/', views.parkings, name='parkings'),
    path('restaurants/', views.restaurants, name='restaurants'),
    path('bus_stations/', views.bus_stations, name='bus_stations'),
    path('base_stations/', views.base_stations, name='base_stations'),
    path('weather/', views.weather, name='weather'),
    path('transport/', views.transport, name='transport'),
     path('shortest_path/', views.shortest_path_view, name='shortest_path'),
    path('ski_routes_geojson/', views.ski_routes_geojson, name='ski_routes_geojson'),
    path('ski_lifts_geojson/', views.ski_lifts_geojson, name='ski_lifts_geojson'),
    path('parkings_geojson/', views.parkings_geojson, name='parkings_geojson'),
    path('restaurants_geojson/', views.restaurants_geojson, name='restaurants_geojson'),
    path('bus_stations_geojson/', views.bus_stations_geojson, name='bus_stations_geojson'),
    path('base_stations_geojson/', views.base_stations_geojson, name='base_stations_geojson'),
]
