from django.contrib.gis.db import models

# Create your models here.
class City(models.Model):    
    city_name = models.CharField(max_length=100) 
    class Meta: verbose_name_plural = "cities" 
    def __str__(self): return self.city_name

class Hospital(models.Model): 
    hospital_name = models.CharField(max_length=100)    
    pub_date = models.DateTimeField('date published')    
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class Canton(models.Model):            
    id=models.PositiveIntegerField(primary_key=True)     
    name=models.CharField(max_length=200)             
    geom=models.MultiPolygonField(srid=4326,null=True)  

    class Meta:                
        db_table = "cantons" 
                            
        def __str__(self):                
            return self.name