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
from itinerary.models import Food, Wages, Flag

default_term = "restaurants, Chinese"
default_lat = 41.8369
default_lon = -87.6847
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
    latitude_filter = set()
    longitude_filter = set()

    # obtain unique zip codes and cast as integers
    zip_filter = yelp_results['zip_code'].unique()
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

def get_filtered_database_info(zip_filter, lat_filter, long_filter):
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
    Food_filtered = Food.objects.filter(zip__in=zip_filter, latitude__in=lat_filter, 
    	longitude__in=long_filter)

    Wages_filtered = Wages.objects.filter(zip__in=zip_filter, latitude__in=lat_filter, 
    	longitude__in=long_filter)
    


def django_to_df_wages(food_df):
    """
    This function takes a django object from U.S. Department of 
    Labour wages data and turns relevant columns of information for
    specified businesses into a pandas dataframe.

    Input:
        - django_result
    Output:
        - dj_df: a pandas dataframe of Dept. of Labour wages data
    """

    dj_df = pd.DataFrame
    zip_code = []
    name = []
    addr = []
    case_id = []
    for i in django_result:
        zip_code.append(i.zip_cd)
        name.append(i.trade_nm)
        addr.append(i.street_addr_1_txt)
        case_id.append(i.case_id)
    dj_df['zip_code'] = zip_code
    dj_df['name'] = name
    dj_df['addr'] = addr
    dj_df['case_id'] = case_id
    return dj_df

def django_to_df_food(wages_df):
    """
    This functions takes a django object from the City of Chicago
    healthcode violations data and turnbs relevant columns of
    information for specified businesses into a pandas dataframe.

    Input:
        - django_result:
    Output:
        - dj_df: a pandas dataframe of healthcode violations
                 by business
    """
    dj_df = pd.DataFrame
    zip_code = []
    name = []
    addr = []
    inspection_id = []
    for i in django_result:
        zip_code.append(i.zip)
        name.append(i.aka_name)
        addr.append(i.address)
        inspection_id.append(i.inspection_id)
    dj_df['zip_code'] = zip_code
    dj_df['name'] = name
    dj_df['addr'] = addr
    dj_df['inspection_id'] = inspection_id
    
    return dj_df


def link_datasets(yelp_results, dj_df, thresholds):
    """
	This functions compares yelp results to django results 
    and produces the best matches based on computing the
    Levenshtein distance (LD) between the zip_code, business 
    name, and address strings. 

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
    zip_threshold, name_threshold, addr_threshold = thresholds
    results = dict()
    for i in product(['high','low'], repeat = 3):
        if i not in results:
            results[i] = dict()

    # Indexation
    indexer = recordlinkage.BlockIndex(on='zip_code')
    pairs = indexer.index(yelp_results, dj_df)

    # Comparison


    # Classification


    # fill in dictionary with business information mapped to match level
    verdict_tuple = (zip_verdict, name_verdict, addr_verdict)
    if y_tuple not in results[verdict_tuple]:
        results[verdict_tuple][y_tuple] = (dj_zip, dj_name, dj_addr, dj_id)
    
    return results



def compare_distance(yelp_results, dj_df, thresholds):
    """ 
    This functions compares yelp results to django results 
    and produces the best matches based on computing the
    Levenshtein distance (LD) between the zip_code, business 
    name, and address strings. 

    Inputs:
        - yelp_results: a pandas dataframe of yelp business
                        results based on a user's input
        - dj_df: a pandas dataframe of django results.
                 Ex. wages, healthcode violations, etc.
        - thresholds: tuple of floats of thresholds categorizing string
                      match levels based on Jaro-Winkler score
    Outputs:
        - results: a dictionary 
    """
    zip_threshold, name_threshold, addr_threshold = thresholds
    results = dict()
    for i in product(['high','low'], repeat = 3):
        if i not in results:
            results[i] = dict()
    
    # inspired by pa4 util function
    for i in yelp_results.iterrows():

        y_ind, y_zip, y_name, y_addr = i[0], i[1][0], i[1][1], i[1][2] 
        y_tuple  = (y_ind, y_zip, y_name, y_addr)
        # ensure all values are strings prior to using jaro-winkler
        y_zip=str(y_zip)
        y_name=str(y_name)
        y_addr=str(y_addr)
        
        for j in dj_df.iterrows():
            dj_zip, dj_name, dj_addr, dj_id = j[1][0], j[1][1], j[1][2], j[1][3]
            # ensure all values are strings prior to using jaro-winkler
            dj_zip=str(dj_zip)
            dj_name=str(dj_name)
            dj_addr=str(dj_addr)

            dj_tuple = (dj_zip, dj_name, dj_addr, dj_id)

            zip_jaro = jaro_distance(y_zip, dj_zip)
            if zip_jaro >= zip_threshold:
                zip_verdict = 'high'
            else:
                zip_verdict = 'low'
                
            name_jaro = jaro_distance(y_name, dj_name)            
            if name_jaro >= name_threshold:
                name_verdict = 'high'
            else:
                name_verdict = 'low'
                
            addr_jaro = jaro_distance(y_addr, dj_addr)
            if addr_jaro >= addr_threshold:
                addr_verdict = 'high'
            else:
                addr_verdict = 'low'

            # consider making this enforce a requirement of 2 high 1 low minimum
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
    

            
            
#compare_distance(yelp_results, dj_df, (0.5, 0.5, 0.5))
    


