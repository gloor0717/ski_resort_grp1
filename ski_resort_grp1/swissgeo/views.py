from django.shortcuts import render
from django.http import HttpResponse
from .models import Canton, City
from django.shortcuts import render
from django.http import Http404
from django.core.serializers import serialize 

# Create your views here.

def index(request):    
    return HttpResponse("Hi there this is Switzerland")


def cities(request):       
    top_cities=City.objects.order_by('-city_name')[:3]    
    context = { 'top_cities':top_cities, }       
    return render(request,'swissgeo/cities.html',context)

def city(request,city_id):    
    try: city=City.objects.get(pk=city_id)    
    except City.DoesNotExist: raise Http404("City not found!!") 
    return render(request,'swissgeo/city.html',{'city':city})

def canton(request,canton_name):            
    cantons=Canton.objects.filter(name=canton_name)    
    return render(request,'swissgeo/canton.html', {'cantonobj':cantons[0]})

def cantons(request):         
    context ={    }           
    return render(request,'swissgeo/cantons.html',context)

def cantonsjson(request):    
    cantons=Canton.objects.all()    
    ser=serialize('geojson',cantons, geometry_field='geom', fields=('name',))          
    return HttpResponse(ser)