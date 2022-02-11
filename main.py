'''Lab task 2'''
import folium
import copy
import argparse
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from haversine import haversine


def read_file(path, year_search):
    with open(path, mode='r') as file:
        num = 0
        data = {}
        for line in file:
            if num < 14:
                num += 1
                continue
            if line.startswith(' '):
                continue
            line = line.strip()
            temp = line.split('\t')
            temp = [item for item in temp if len(item)>1]
            idx = temp[0].find('(1')
            if idx == -1:
                idx = temp[0].find('(2')
            year = temp[0][idx+1:idx+5]
            if year != year_search:
                continue
            idx_name = temp[0].find('"', 3)
            name = temp[0][1:idx_name]
            tmp = temp[1].split(',')
            city = tmp[0]
            if year in data.keys():
                if name in data[year]:
                    data[year][name].append(city)
                else:
                    data[year][name] = {}
                    data[year][name] = [city]
            else:
                data[year] = {}
                data[year][name] = [city]
    return data
#print(read_file(r'C:\Users\Andrea\Programing_Basics_2022\locations.list', '2006'))

def location(locations, year):
    '''{'2006': {'#1 Single': 'New York City', '#15SecondScare': 'West Hills'}}'''
    data = locations[year]
    geolocator = Nominatim(user_agent="main.py")
    for name in data.keys():
        for idx in range(len(data[name])):
            location = geolocator.geocode(data[name][idx])
            data[name][idx] = (location.latitude, location.longitude)
    return data
#print(location(read_file(r'C:\Users\Andrea\Programing_Basics_2022\test.list', '2006'), '2006'))


def find_nearest(data, location):
    '''{'#1 Single': [(34.0536909, -118.242766), (40.7127281, -74.0060152)],
    '#15SecondScare': [(52.4081812, -1.510477), (40.8212755, -73.43679367645896)]}'''
    data_copy = copy.deepcopy(data)
    res = []
    coord = {}
    for names in data.keys():
        temp = []
        for idx in range(len(data[names])):
            temp.append(round(haversine(data[names][idx], location)))
        index = temp.index(min(temp))
        coord[names] = data[names][index]
        data_copy[names] = min(temp)
        data[names] = (min(temp))

    lst = []
    for _ in range(9):
        if len(data_copy) == 0:
            break
        key = min(data_copy, key=data_copy.get)
        res.append((key)) #data_copy[key]
        data_copy.pop(key)
    for item in res:
        lst.append((item,coord[item]))
    return lst

#print(find_nearest(location(read_file(r'C:\Users\Andrea\Programing_Basics_2022\test.list', '2006'), '2006'), (49.817545, 24.023932)))

def create_map(data, coord):
    '''[('#15SecondScare', (52.4081812, -1.510477)), ('#1 Single', (40.7127281, -74.0060152))]'''
    map = folium.Map(tiles="Stamen Terrain",
    location=coord,
    zoom_start=17)
    layer1 = folium.FeatureGroup(name="Default")
    layer2 = folium.FeatureGroup(name="Marks")
    layer3 = folium.FeatureGroup(name="UCU")
    layer3.add_child(folium.Marker(location=(49.817567419480966, 24.023825823605176), popup='Colegium', icon=folium.Icon()))
    layer1.add_child(folium.Marker(location=coord, popup='Your location', icon=folium.Icon()))
    for item in data:
        layer2.add_child(folium.Marker(location=item[1], popup=item[0], icon=folium.Icon()))
    map.add_child(layer1)
    map.add_child(layer2)
    map.add_child(layer3)
    map.add_child(folium.LayerControl())
    map.save('My_Map.html')
#print(create_map(find_nearest(location(read_file(r'C:\Users\Andrea\Programing_Basics_2022\test.list', '2013'), '2013'), (37.09274132456057, -118.93703484204748)), (37.09274132456057, -118.93703484204748)))

def main():
    '''python main.py 2000 49.83826 24.02324 path_to_dataset'''
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    parser.add_argument('long', type=float)
    parser.add_argument('lat', type=float)
    parser.add_argument('path', type=str)
    args = parser.parse_args()
    year = str(args.year)
    long = args.long
    lat = args.lat
    path = args.path
    coord = (long, lat)
    data = read_file(path, year)
    loc = location(data, year)
    points = find_nearest(loc, coord)
    create_map(points, coord)
    return 'Map has been created'

def test():
    year = '2012'
    long = 49.83826
    lat = 24.02324
    path = r'C:\Users\Andrea\Programing_Basics_2022\test.list'
    coord = (long, lat)
    data = read_file(path, year)
    loc = location(data, year)
    points = find_nearest(loc, coord)
    create_map(points, coord)
#print(test())
print(main())