import networkx as nx
from django.contrib.gis.geos import Point, LineString
from .models import SkiRoute, SkiLift, BaseStation

def build_ski_resort_graph():
    graph = nx.Graph()

    for route in SkiRoute.objects.all():
        coords = list(route.geometry.coords)
        for i in range(len(coords) - 1):
            start = coords[i]
            end = coords[i + 1]
            graph.add_edge(start, end, type='ski_route', name=route.name, length=LineString([start, end]).length)

    for lift in SkiLift.objects.all():
        coords = list(lift.geometry.coords)
        start = coords[0]
        end = coords[-1]
        graph.add_edge(start, end, type='ski_lift', name=lift.name, length=LineString([start, end]).length)

    for base in BaseStation.objects.all():
        coords = list(base.geometry.exterior.coords)
        for i in range(len(coords) - 1):
            start = coords[i]
            end = coords[i + 1]
            graph.add_edge(start, end, type='base_station', name=base.name, length=LineString([start, end]).length)
    
    for route1 in SkiRoute.objects.all():
        for route2 in SkiRoute.objects.all():
            if route1 != route2 and route1.geometry.intersects(route2.geometry):
                intersection = route1.geometry.intersection(route2.geometry)
                if intersection.geom_type == 'Point':
                    coords = intersection.coords[0]
                    graph.add_node(coords, type='intersection')
                    graph.add_edge(route1.geometry.coords[0], coords, length=0)
                    graph.add_edge(route2.geometry.coords[0], coords, length=0)

    return graph

def find_route(graph, start, end):
    try:
        path = nx.shortest_path(graph, source=start, target=end, weight='length')
        return path
    except nx.NetworkXNoPath:
        return None
