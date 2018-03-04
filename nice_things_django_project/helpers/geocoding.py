#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 12:34:16 2018

@author: ty

Modified on Sat Feb 17 22:10:17 2018 by Sasha
Modified on Fri Mar 02 17:34:17 2018 by Sasha


This file contains functions for geocoding our address data.
"""
from geopy.geocoders import GoogleV3
from collections import namedtuple
from random import uniform
import requests
import pandas as pd
import random
import time
from urllib.parse import quote
import json
import csv
import sys
import os

from pathlib import Path
#nice_things_django_project_dir = str(Path(__file__).resolve()) + "/.."
nice_things_django_project_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, nice_things_django_project_dir)

from helpers import file_list
from helpers.api_keys import GOOGLE_KEY
#from helpers.api_keys import GOOGLE_KEYS
from helpers.api_keys import OPEN_CAGE_DATA


# Found on https://stackoverflow.com/questions/12082314/
# how-to-convert-a-url-string-to-safe-characters-with-python:


# Upon import, this will set current working directory to
# file_list.nice_things_django_project_dir:
# working = os.environ.get("WORKING_DIRECTORY",
#                          file_list.nice_things_django_project_dir)
# if len(sys.argv) > 1:
#     working = sys.argv[1]
# os.chdir(working)
#
# sys.path.insert(0, file_list.nice_things_django_project_dir)


DEFAULT_LAT = 41.7830867
DEFAULT_LON = -87.6040276

geocoded_address = namedtuple('geocode_address', ['address', 'lat', 'lon'])


def get_whd(file_location='datasets/whd/whd_whisard.csv', default_city='Chicago'):
    """
    This function gets the Wages and Hourly data and geocodes it. 
    WHD data comes from: https://www.dol.gov/whd/
    
    
    Inputs:
        - google_key: the google api key, as a string
        - file_location: the location of the file to use
        - default_city: a string of the city name
    Outputs:
        - whd: a pandas dataframe with the whd data and geocoded coordinates
    """
    
    whd = pd.read_csv(file_location, low_memory=False)
    whd = whd[list(whd.columns[1:9])]
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
    location_list_results, failures = geo_code_address(address_list, 20)
    # write these into the pandas df
    whd['full_address'] = [i[0] for i in location_list_results]
    whd['latitude'] = [i[1] for i in location_list_results]
    whd['longitude'] = [i[2] for i in location_list_results]
    return whd


# define geocoding function
def geo_code_address(address_list, limit=200):
    """
    This function takes a list of addresses as strings and returns the 
    location as a geopy Location instance using Google's Geocode API.
    
    Inputs:
        - address_list: a list of strings
        - limit: the maximum number of requests to make to google
        - api_key: the google api key, as a string
    Outputs:
        - loc_list: a list of Location objects
        - try_again: a list of location strings
            indicating failed geo coding requests
    """
    geolocator = GoogleV3(api_key=GOOGLE_KEY)
    loc_list = []
    try_again = []
    counter = 0
    for i in address_list:
        print("\n", i)
        counter += 1
        print("looking for address", i, "\n")
        try:
            location = geolocator.geocode(i)
            lat = location.latitude
            lon = location.longitude
            place = location[0]
            loc_list.append(geocoded_address(place, lat, lon)) 
        except:
            try_again.append(place)
            lat = DEFAULT_LAT
            lon = DEFAULT_LON
            place = i
        #loc_list.append(geocoded_address(place, lat, lon))
        time.sleep(5)
        if counter == limit:
            break
    return loc_list, try_again


def geo_code_single_address(address_str):
    """
    Takes an address and outputs Google's address, and latitude, longitude
    coordinates using Google's Geocode API.

    :param address_str: string, address, e.g. "1234 U. st., Chicago, IL"

    :return: tuple of address string, latitude float, and longitude float,
    e.g. ("1234 U. st., Chicago, IL", -12.12134, 53.345345)
    """
    api_key = GOOGLE_KEY#random.choice(GOOGLE_KEYS)
    print("API KEY:", api_key)
    geolocator = GoogleV3(api_key=api_key)
    location = geolocator.geocode(address_str)
    address = location.address
    lat = location.latitude
    lon = location.longitude
    time.sleep(uniform(4, 5))

    return address, lat, lon


def geocode_using_opencagedata(address, city, state, zip_code,
                               country, api_key=OPEN_CAGE_DATA):
    """
    Takes an address and uses https://geocoder.opencagedata.com/ service
    to geocode each.

    :param address: str, e.g. "1234 Wacker Dr"

    :param city: str, e.g. "Chicago"

    :param state: str, e.g. "IL"

    :param zip_code: str, e.g. "60615"

    :param country: str, e.g. "United States"

    :param api_key: str, pass key for open cage data API,
    e.g. "213jroijg_dafafd-dfa1424"

    :return latitude, longitude: tuple, in which each item is a str,
    representing floats of latitude and longitude
    """
    full_address = "{}, {}, {}, {}, {}".format(address, city, state, zip_code,
                                               country)
    # Get into API (with app tokens, there's a usage limit of 1
    # request per 1 second):
    concatenate_url = "https://api.opencagedata.com/geocode/v1/json?" \
                      "key={}&q={}&pretty=1&no_annotations=1".\
                      format(api_key, quote(full_address))
    r = requests.get(url=concatenate_url)
    response_dict = json.loads(r.text)
    coordinates_dict = response_dict["results"][0]["geometry"]
    latitude = coordinates_dict["lat"]
    longitude = coordinates_dict["lng"]
    # Wait some time between 2 and 4 seconds to avoid using too frequently:
    time.sleep(uniform(2, 4))

    return latitude, longitude


def geocode_bls_addresses(output_csv="{}{}".
                          format(nice_things_django_project_dir,
                                 file_list.labor_stats_geocoded),
                          original_bls_csv="{}{}".
                          format(nice_things_django_project_dir,
                                 file_list.labor_stats)):
    # print(original_bls_csv)
    # print(output_csv)

    use_cols = ["case_id", "trade_nm", "legal_name", "street_addr_1_txt",
                "cty_nm", "st_cd", "zip_cd", "case_violtn_cnt"]

    df = pd.read_csv(filepath_or_buffer=original_bls_csv,
                     dtype={"case_id": int,
                            "trade_nm": str,
                            "legal_name": str,
                            "street_addr_1_txt": str,
                            "cty_nm": str,
                            "st_cd": str,
                            "zip_cd": int,
                            "case_violtn_cnt": int},
                     usecols=use_cols)

    # Clean out nulls to avoid nullable entries into the itinerary_wages table
    # in the nice_things database:
    df = df.dropna()

    csv_file = open(output_csv, "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(use_cols + ["latitude", "longitude"])

    # Squirt into the csv:
    geocode_counter = 1
    for index, row in df.iterrows():
        # Prepare row names:
        case_id = row[use_cols[0]]
        trade_nm = row[use_cols[1]]
        legal_name = row[use_cols[2]]
        street_addr_1_txt = row[use_cols[3]]
        cty_nm = row[use_cols[4]]
        st_cd = row[use_cols[5]]
        zip_cd = row[use_cols[6]]
        case_violtn_cnt = row[use_cols[7]]

        # Geocode:
        print("ATTEMPTING TO GEOCODE ADDRESS", geocode_counter, ":")
        print(street_addr_1_txt, cty_nm, st_cd, zip_cd)
        latitude, longitude = geocode_using_opencagedata(
            address=street_addr_1_txt,
            city=cty_nm, state=st_cd,
            zip_code=zip_cd,
            country="United States")
        print("WRITE ROW:", [case_id, trade_nm, legal_name, street_addr_1_txt,
                             cty_nm, st_cd, zip_cd, case_violtn_cnt,
                             latitude, longitude])

        csv_writer.writerow([case_id, trade_nm, legal_name, street_addr_1_txt,
                             cty_nm, st_cd, zip_cd, case_violtn_cnt,
                             latitude, longitude])
        geocode_counter += 1
        # if geocode_counter > 7:
        #     break

    csv_file.close()


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
