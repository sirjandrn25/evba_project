# import requests


# def get_current_location():
#     res = requests.get('https://ipinfo.io')
#     data = res.json()
#     address = data.get('city')
#     location = data.get('loc').split(',')
#     lat = float(location[0])
#     lon = float(location[1])
#     d = {
#         'address':address,
#         'lat':lat,
#         'lon':lon
#     }
#     return d

import math

# using haversine formula 
def distance(loc1,loc2):

	radius = 6371
	
	lat1 = (loc1['lat']*math.pi/180)
	lat2 = (loc2['lat']*math.pi/180)

	lon1 = (loc1['lon']*math.pi/180)
	lon2 = (loc2['lon']*math.pi/180)

	inside_sqrt = ((math.sin((lat2-lat1)/2))**2)+math.cos(lat1)*math.cos(lat2)*((math.sin((lon2-lon1)/2))**2)
	# print(inside_sqrt)
	d = 2*radius*math.asin(math.sqrt(inside_sqrt))
	return d*1000


def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def bubble_sort(data):
    for i in range(len(data)-1):
        for j in range(i+1,len(data)):
            if data[i]['distance']>data[j]['distance']:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
    return data

