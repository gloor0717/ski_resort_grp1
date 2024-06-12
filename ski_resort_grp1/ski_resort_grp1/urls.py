from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # This line includes the admin URLs
    path('', views.index, name='index'),
    path('map/', views.map_view, name='map'),
    path('ski_routes/', views.ski_routes, name='ski_routes'),
    path('weather_stations/', views.weather_stations, name='weather_stations'),
    path('amenities/', views.amenities, name='amenities'),
]
