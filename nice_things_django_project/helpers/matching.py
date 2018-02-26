#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 20:17:53 2018

@author: ty & ks
"""
import pandas as pd
#from api_keys import yelp
from jellyfish import jaro_distance
from yelpapi import YelpAPI
from itertools import product
import recordlinkage as rl
import numpy as np
# will need to change this directory path below
import os
from dateutil import parser
from django.core.wsgi import get_wsgi_application
os.chdir('../')
os.environ['DJANGO_SETTINGS_MODULE'] = "nice_things_django_project.settings"
application = get_wsgi_application()
from itinerary.models import Food, Wages, Flag
from django_pandas.managers import DataFrameManager


default_term = "La fuente restaurant"
default_lat = 41.8194
default_lon = -87.6990
default_lim = 50 # defaults at 20 and 50 is limit
default_sort = "distance" # sorts by distance (other options are
# best_match, rating, review_count)

# this is how the yelp api works
#yelp_api = YelpAPI(yelp)

#temporarily use Kevin's API Key
yelp_api = YelpAPI("GsAgBiywduecH_D-DDeB-ctBkWbUnFP_6w_b0CG4utMCu3s9Z3XIrNuyJum_NJ-FuIIsljD_7KTrOaHuZZjos6v-5-o5GSzfSsAVwySWhmlV4vnlN9ElxCE0xOBrWnYx")
search_results = yelp_api.search_query(term = default_term, \
                                       latitude = default_lat,\
                                       longitude = default_lon,\
                                       limit = default_lim,\
                                       sort_by = default_sort)


# use region key to get lattitude, longitude


def extract_yelp_data(search_results):
    """
    This function takes search results (a dictionary) and obtains the 
    name, zip code, address of the possible restaurant matches in the
    form of a pandas dataframe.

    Inputs:
        - search_results: a dictionary of Yelp query results based on 
                          a user's search.
    Ouputs:
        - yelp_results: a pandas dataframe containing the zip code,
                        name, address,  of each potential result.
    """
    # initialize lists for each planned column
    addresses = []
    names = []
    zip_code = []
    latitude = []
    longitude = []
    
    # obtain business information
    businesses = search_results['businesses']
    for i in businesses:
        addresses.append(i['location']['display_address'][0])
        names.append(i['name'])
        # need to create filter that works to filter out missing zipcodes
        if i['location']['zip_code'] != '':
            zip_code.append(i['location']['zip_code'])
        latitude.append(i['coordinates']['latitude'])
        longitude.append(i['coordinates']['longitude'])

    # cast into pandas dataframe
    yelp_results = pd.DataFrame()
    yelp_results['zip_code'] = zip_code
    yelp_results['name'] = names
    yelp_results['addr'] = addresses
    yelp_results['latitude'] = latitude
    yelp_results['longitude'] = longitude 

    # change columns to appropriate data types
    yelp_results['zip_code'] = pd.to_numeric(yelp_results['zip_code'])
    #yelp_results['name'] = yelp_results['name'].astype(str)
    # yelp_results = yelp_results['addr'].astype(str)

    return yelp_results


def define_filters(yelp_results):
    """
	This function creates the filters we will use to query
	our database to obtain wages, food, etc. 

	Input:
		- yelp_results: a pandas dataframe of the Yelp query
						results
	Ouput:
		- zip_filter: a set of unique zip codes in the Yelp results
		- latitude_filter: a set of unique truncated atitude coordinates
		- longitude_filter: a numpy array of unique truncated longitude coordinates
	"""
    # remove rows that don't have a zip_code
    #yelp_results = yelp_results[yelp_results.zip_code != " '' "]
    latitude_filter = set()
    longitude_filter = set()

    # obtain unique zip codes and cast as integers
    zip_filter = yelp_results['zip_code'].unique()
    # need to handle businesses without zip codes
    # for zip_code in zip_filter:
    # 	if zip_code == " '' ":
    # 		np.delete
    zip_filter = set(zip_filter.astype(int))

    # truncate latitudes and obtain unique truncated latitudes
    lat_filter = set(yelp_results['latitude'].apply(truncate_coordinate))

    # truncate longitudes and obtain unique truncated longitudes
    long_filter = set(yelp_results['longitude'].apply(truncate_coordinate))

    return zip_filter, lat_filter, long_filter

def truncate_coordinate(coordinate):
    """
    This is a function that truncates coordinates to 3-decimal places.
	"""
    s = '{}'.format(coordinate)
    i, p, d = s.partition('.')
    #truncate to 3 decimal places
    trunc_coordinate = '.'.join([i, (d+'0'*3)[:3]])
    
    return trunc_coordinate

def get_filtered_database_dfs(zip_filter, lat_filter, long_filter):
    """
	This function takes the zip code, latitude, and longitude filters
	and queries the database to obtain wage information based
	on those filters and returns a pandas dataframe of filtered database
	information.

	Input:
		- zip_filter: a set of unique zip codes in the Yelp results
		- lat_filter: a set of unique truncated atitude coordinates
		- long_filter: a numpy array of unique truncated longitude coordinates
    Output:
    	- wages_df: a pandas dataframe of wages information
    	- food_df: a pandas dataframe of food information
    """
    # filter django object based on zip code, latitude, & longitude
    food_filtered = Food.objects.filter(zip__in=zip_filter, 
        latitude__range=(min(lat_filter), max(lat_filter)), 
        longitude__range=(max(long_filter), min(long_filter)))
    wages_filtered = Wages.objects.filter(zip_cd__in=zip_filter, 
        latitude__range=(min(lat_filter), max(lat_filter)), 
        longitude__range=(max(long_filter), min(long_filter)))

    
    # cast as pandas dataframes if filtered result is not empty
    if food_filtered.exists():
        food_df = food_filtered.to_dataframe(fieldnames=['zip', 'aka_name', 
            'address', 'inspection_id', 'latitude', 'longitude'])
        food_df = food_df.rename(index=str, columns={"zip": "zip_code", 
            "aka_name": "name", "address": "addr"})
    else:
        food_df = []

    if wages_filtered.exists():
        wages_df = wages_filtered.to_dataframe(fieldnames=['zip_cd', 'trade_nm', 
            'street_addr_1_txt', 'case_id', 'latitude', 'longitude'])
        wages_df = wages_df.rename(index=str, columns={"zip_cd": "zip_code", 
            "trade_nm": "name", "street_addr_1_txt": "addr"})
    else:
        wages_df = []
        
    return food_df, wages_df
    

def link_datasets(yelp_results_df, dj_df, thresholds):
    """
	This functions compares yelp results to django results 
    and produces the best matches based on computing the
    jaro-winkler score between the zip_code, business 
    name, address strings, latitude, and longitude. 

    Inputs:
        - yelp_results: a pandas dataframe of yelp business
                        results based on a user's input
        - dj_df: a pandas dataframe of django results.
                 Ex. wages, healthcode violations, etc.
        - thresholds: tuple of floats of thresholds categorizing string
                      match levels based on Jaro-Winkler score
    Outputs:
        - results: a dictionary with restaurants/businesses 
    """
    # create dictionary of all possible match combinations
    # name_thresh = 0.50 | addr_thresh = 0.6
    
    name_thresh, addr_thresh = thresholds
    results = dict()
    for i in product(['high','low'], repeat = 3):
        if i not in results:
            results[i] = dict()

    # Indexation
    indexer = rl.FullIndex()
    # having issues with Block Index - CHECK
    indexer = rl.BlockIndex(on='zip_code')
    pairs = indexer.index(yelp_results, dj_df)

    # Comparison
    compare = rl.Compare()
    compare.numeric('zip_code', 'zip_code', method='linear', 
        scale=30.0, label='zip_score')
    compare.string('name', 'name', method='qgram', 
        threshold=name_thresh, label='name_score')
    compare.string('addr', 'addr', method='qgram', 
        threshold=addr_thresh, label='addr_score')
    compare.geo('latitude', 'longitude', 'latitude', 'longitude', 
        method='linear', scale=30.0, label='coord_score')

    features = compare.compute(pairs, yelp_results, dj_df)

    # Classification
    # set strict conditions for zip_score and coordinates_scores
    # zip_score = 1.0
    # coordinate_score >= 0.98
    # 

    # fill in dictionary with business information mapped to match level
    verdict_tuple = (zip_verdict, name_verdict, addr_verdict)
    if y_tuple not in results[verdict_tuple]:
        results[verdict_tuple][y_tuple] = (dj_zip, dj_name, dj_addr, dj_id)
    
    return results

def best_matches(how_well, search_results, dj_df, thresholds):
    # how well is tuple of High, High, Low, etc.
    yelp_results = extract_yelp_data(search_results)
    
    results = compare_distance(yelp_results, dj_df, thresholds)
    # find the ones that match well enough
    if len(results[how_well]) > 0:
        return results[how_well]  # dictionary of tuples (yelp) (flags data)
    else:

        return   yelp_results

