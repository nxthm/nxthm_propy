# nxthm_propy - nxthm.com

A simple method to capture addresses that are within a radius of a given focus address

Python packages employed include googlemaps for retrieving the latitude and longitude of a given address, and geopy for measuring geo-distance between addresses

## Background

Predictive analytics or machine learning algorithms will use comparable properties to derive a valuation for a subject property.  A machine learning feature set will use property features such as square footage, number of bedrooms, etc.  When sampling a population of comparable properties, the distance between the subject property and a comparable property will factor heavily towards answering the question on every home owner's mind - 'What's my home worth?'.

## Approach

Depending on jurisdiction, a local real estate board will make property transaction files available for download to authorized brokers.  The files will contain property addresses, features and transaction data.

As the saying goes, real estate is about location, location, location.  The code in this repository outlines an approach to capturing addresses from a population set that are within a radius of an address for the purposes in a broader algorithm to determine home value

### Notes

The attached CSV file is a random sampling of addresses in the Toronto E02 municipal district

To test this code, you will have to procure and insert a google maps API key in the get_googlemaps_latlng function.  These keys are free, but come with limitations.  The key can be set to NONE, but this imposes a cap of 2500 requests per day and 50 requests per second (this is subject to change) For details see: console.developers.google.com/apis/

An alternative is to use the Geopy as a wrapper to the free OpenStreetMap Nominatim to resolve raw street addresses to longitude and latitude counterparts.  For diversity sake, the code sample uses both the google maps API to resolve raw addresses, and Nominatim to calculate distance between addresses

To specify a radius in miles or km instead of metres, change

return distance.distance(latlng1, latlng2).m

to

return distance.distance(latlng1, latlng2).miles

or

return distance.distance(latlng1, latlng2).km

## How to use

Set the subject property raw address in test_address
Supply the address population in address_list as a list of raw addresses.  In the sample code, a CSV file of addresses is loaded into a pandas dataframe.  The column in the dataframe containing the raw addresses is set in address_column.

Finally, call address_in_radius with test_address, address_list and a parameter defining a radius (in metres).

The return value will be a list of [address, distance to test_address] list pairs.  If no addresses fall within the radius of the subject property, an empty list is returned
