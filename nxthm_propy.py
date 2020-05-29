
import googlemaps
import pandas as pd
import datetime
from geopy import distance

# Returns a list containing the latitude and longitude for address
# Address must be in the street number, street name, street direction, city, province/state, country
# address must be resolvable by the google maps API
# e.g. 123 Main St, Toronto, Ontario
# This function requires a valid google maps API key, supplied in google_maps_api_key
def get_googlemaps_latlng(address : str) -> list:

    google_maps_api_key : str = 'API Key Here'

    return_lst : list = []

    gmaps = googlemaps.Client(key=google_maps_api_key)
    geocode_result = gmaps.geocode(address)

    if 0 == len(geocode_result):
        return_lst = []
    else:
        return_lst = [geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng']]

    return return_lst

# Distance between two addresses defined by latitude and longitude
# Reference: https://geopy.readthedocs.io/en/latest/#module-geopy.distance
# At the database level, distance between two points in metres can be calculated using
# SELECT CAST(GEOGRAPHY::Point(@lat1, @lng1, 4326).STDistance(GEOGRAPHY::Point(@lat, @lng, 4326)) AS int) AS dist
#
# Returns distance between two lat, lng list pairs in metres, -1 on error
def get_geo_distance(latlng1 : list, latlng2 : list) -> float:

    try:
        return distance.distance(latlng1, latlng2).m
    except:
        return -1

# Return is a list of all addresses within raidus_m metres of address_focus
# Addresses should be in traditional format: 123 Main St, Toronto, Ontario, or any format
# which can be resolved by the google maps API
def address_in_radius(address_focus : str, address_list : list, radius_m : float = 0) -> dict:

    return_addresses    : list = []
    focus_latlng        : list = []
    dist                : float

    if len(address_focus) > 0 and len(address_list) > 0:

        # Get focus address lat, lng
        focus_latlng = get_googlemaps_latlng(address_focus)

        if 2 == len(focus_latlng):
            for add in address_list:
                dist = get_geo_distance(focus_latlng, get_googlemaps_latlng(add))
                if dist <= radius_m:
                    return_addresses.append([add, dist])
        else:
            return_addresses = {}
    else:
        return_addresses = {}

    return return_addresses

# Sample calling
# Test address and sample CSV file are random addresses in the Toronto E2 MLS district

property_file   : str = 'nxthm_prop.csv'
test_address    : str = '108 Balfour Ave, Toronto, ON M4C 1T6, Canada'

df : pd.DataFrame = pd.read_csv(property_file, sep=',')
address_column : str = 'gFormatted'
address_list : list = []

if df is not None:
    print('{}:nxthm_propy:subject address:{}'.format(datetime.date.today(), test_address))
    print('{}:nxthm_propy:property count:{}'.format(datetime.date.today(), df.shape[0]))
    address_list = df[address_column].to_list()
    print(address_in_radius(test_address, address_list, radius_m=1000))
else:
    print('{}:nxthm_propy:failed to import file:{}'.format(datetime.datetime.today, property_file))