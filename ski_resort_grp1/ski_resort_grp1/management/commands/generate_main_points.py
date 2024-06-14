import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from ski_resort_grp1.models import SkiRoute, SkiLift, MainPoint

class Command(BaseCommand):
    help = 'Create main points for Ski Routes and Ski Lifts'

    def handle(self, *args, **kwargs):
        self.create_main_points_for_ski_routes()
        self.create_main_points_for_ski_lifts()

    def create_main_points_for_ski_routes(self):
        ski_routes = SkiRoute.objects.all()
        for route in ski_routes:
            coords = list(route.geometry.coords)
            for idx, coord in enumerate(coords):
                point_name = f'{route.name} - Point {idx + 1}'
                self.create_main_point(point_name, Point(coord), route=route)

    def create_main_points_for_ski_lifts(self):
        ski_lifts = SkiLift.objects.all()
        for lift in ski_lifts:
            coords = list(lift.geometry.coords)
            for idx, coord in enumerate(coords):
                point_name = f'{lift.name} - Point {idx + 1}'
                self.create_main_point(point_name, Point(coord), lift=lift)

    def create_main_point(self, name, location, route=None, lift=None):
        main_point, created = MainPoint.objects.get_or_create(
            name=name,
            location=location,
            defaults={'route': route, 'lift': lift}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created MainPoint: {name}'))
        else:
            self.stdout.write(self.style.WARNING(f'MainPoint already exists: {name}'))
