import json
import math
import folium
from shapely.geometry import LineString, Point
import math

def json_savefile(jsondata, filename):
    with open(filename, 'w') as output_file:
        json.dump(jsondata, output_file, indent=4)
    print(f'json output file saved to {filename}')
        
def hash_json(jsondata):
    return frozenset((str(x), str(y)) for x, y in jsondata.items())

def divide_rectangle(box, limit):
    width = abs(box['east_bound'] - box['west_bound'])
    height = abs(box['north_bound'] - box['south_bound'])
    num_width = math.ceil(width / math.sqrt(limit / height))
    num_height = math.ceil(height / math.sqrt(limit / width))
    
    sub_width = width / num_width
    sub_height = height / num_height
    
    sub_boxes = []
    for i in range(num_height):
        south_bound = box['south_bound'] + i * sub_height
        north_bound = south_bound + sub_height
        for j in range(num_width):
            west_bound = box['west_bound'] + j * sub_width
            east_bound = west_bound + sub_width
            sub_box = {'west_bound': west_bound, 'east_bound': east_bound,
                       'south_bound': south_bound, 'north_bound': north_bound}
            sub_boxes.append(sub_box)
    return sub_boxes


def visualize_boxes(boxes):
    m = folium.Map(location=[(boxes[0]['north_bound'] + boxes[0]['south_bound']) / 2,
                             (boxes[0]['west_bound'] + boxes[0]['east_bound']) / 2],
                   zoom_start=11)

    for box in boxes:
        folium.Polygon([[box['north_bound'], box['west_bound']],
                        [box['north_bound'], box['east_bound']],
                        [box['south_bound'], box['east_bound']],
                        [box['south_bound'], box['west_bound']],
                        [box['north_bound'], box['west_bound']]],
                       color='red', fill=False).add_to(m)

    return m

def point_to_line_dist(point, line):
    # Convert the list of tuples into a LineString object
    poly_line = LineString(line)

    # Define a point for which you want to calculate the closest distance to the coastline
    poly_point = Point(point[0], point[1])

    # Calculate the closest distance from the point to the coastline
    distance = poly_line.distance(poly_point)

    # Convert the distance from decimal degrees to kilometers
    distance_km = distance * 111.32
    
    return distance_km

def euclid_dist(p1, p2):
    point1 = Point(p1[0], p1[1])
    point2 = Point(p2[0], p2[1])
    
    distance = point1.distance(point2)
    distance_km = distance * 111.32
    
    return distance_km