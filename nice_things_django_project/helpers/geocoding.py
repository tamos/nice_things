#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORIGINAL (with the help of API and Python documentation)

Tyler Amos, Alexander Tyan

This file contains functions for geocoding our address data. BLS csv addresses
are not geocoded, but we need coordinates for later record linkage. These
function do that.
"""
from random import uniform
import requests
import pandas as pd
import time
from urllib.parse import quote
import json
import csv
import sys
import os

# Find files directories:
nice_things_django_project_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, nice_things_django_project_dir)
from helpers import file_list
from helpers.api_keys import OPEN_CAGE_DATA

DEFAULT_GEOCODED_PATH = "{}{}".format(nice_things_django_project_dir,
                                      file_list.labor_stats_geocoded)
DEFAULT_UNGEOCODED_PATH = "{}{}".format(nice_things_django_project_dir,
                                        file_list.labor_stats)


def geocode_using_opencagedata(address, city, state, zip_code,
                               country, api_key=OPEN_CAGE_DATA):
    """
    Takes an address and uses https://geocoder.opencagedata.com/ service
    to geocode each.

    Inputs:
        - address: str, e.g. "1234 Wacker Dr"
        - city: str, e.g. "Chicago"
        - state: str, e.g. "IL"
        - zip_code: str, e.g. "60615"
        - country: str, e.g. "United States"
        - api_key: str, pass key for open cage data API,
        e.g. "213jroijg_dafafd-dfa1424"

    Outputs:
        - latitude, longitude: tuple, in which each item is a str,
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
    # Wait some time between 2 and 4 seconds to avoid using getting locked out:
    time.sleep(uniform(2, 4))

    return latitude, longitude


def geocode_bls_addresses(output_csv=DEFAULT_GEOCODED_PATH,
                          original_bls_csv=DEFAULT_UNGEOCODED_PATH):
    """
    Takes a CSV of BLS labour code violations and geocodes each address row.

    Inputs:
        - output_csv: string, path with file name to output geocoded dataframe
        - original_bls_csv: string, path to file with the original BLS data

    Outputs:
        - no return, saves csv file to original_bls_csv file path
    """

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

        # Geocode (Print to see progress):
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

    csv_file.close()
