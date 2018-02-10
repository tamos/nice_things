#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 12:34:16 2018

@author: ty

This file contains functions for geocoding our address data.
"""
from geopy.geocoders import GoogleV3
import pandas as pd
import time
from api_keys import google_key

def get_whd(google_key, file_location = 'datasets/whd/whd_whisard.csv', default_city = 'Chicago'):
    """
    This function gets the whd data and geocodes it. 
    Inputs:
        - google_key: the google api key, as a string
        - file_location: the location of the file to use
        - default_city: a string of the city name
    Outputs:
        - whd: a pandas dataframe with the whd data and geocoded coordinates
    """
    
    whd = pd.read_csv(file_location, low_memory = False)
    whd = whd[list(whd.columns[1:9])]
    #whd = whd[keep_cols]
    whd = whd[whd.cty_nm == default_city]
    whd = whd[0:10]
    whd.zip_cd = whd.zip_cd.astype(int)
    # Make a list of addresses
    address_list = []
    for i, j in whd.iterrows():
        street = j.street_addr_1_txt
        city = j.cty_nm
        state = j.st_cd
        zip_code = str(j.zip_cd)
        address = " ".join([street, city, state, zip_code])
        address_list.append(address)
    # run the geocode on all the addresses
    location_list_results, failures = geo_code_address(google_key, address_list, 20)
    # write these into the pandas df
    rowindex = 0
    whd['full_address'] = 0
    whd['latitude'] = 0
    whd['longitude'] = 0
    print('here')
    for i in location_list_results:
        print(i)
        whd.full_address.iloc[rowindex] = i[0]
        whd.latitude.iloc[rowindex] = i.latitude
        whd.longitude.iloc[rowindex] = i.longitude
        rowindex += 1
    return whd
    
# define geocoding function
def geo_code_address(google_key, address_list, limit = 200):
    """
    This function takes a list of addresses as strings and returns the 
    location as a geopy Location instance. 
    
    Inputs:
        - address_list: a list of strings
        - limit: the maximum number of requests to make to google
        - api_key: the google api key, as a string
    Outputs:
        - loc_list: a list of Location objects
        - try_again: a list of location strings
            indicating failed geo coding requests
    """
    geolocator = GoogleV3(api_key = google_key)
    loc_list = []
    try_again = []
    counter = 0
    for i in address_list:
        print("\n", i)
        counter += 1
        print("looking for address", i, "\n")
        try:
            location  = geolocator.geocode(i)
        except:
            try_again.append(location)
            location = 'PLACEHOLDER'
        loc_list.append(location) 
        #try_again.append('PLACEHOLDER')
        time.sleep(5)
        if counter == limit:
            break
    return loc_list, try_again
    
whd_df = get_whd(google_key = google_key)

'''
Please keep for the moment, just as reference
# One option = can't get it work with real data but test data works
#Unique ID, Street address, City, State, ZIP
#geo_requirements = ['case_id', 'street_addr_1_txt', 'cty_nm', 'st_cd', 'zip_cd']
#whd[geo_requirements].to_csv('datasets/whd/address_for_geocode.csv', index=False)
# still figuring out how to do curl from python
#curl --form addressFile=@addys.csv --form benchmark=9 https://geocoding.geo.census.gov/geocoder/locations/addressbatch --output geocoderesult.csv
#geo_coded = pd.read_csv('datasets/whd/geocode_result.csv')
'''
