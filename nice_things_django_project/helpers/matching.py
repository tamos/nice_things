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
from itinerary.models import Food, Wages, Divvy, Env_Complaints
from django_pandas.managers import DataFrameManager

##### YELP QUERY PARAMETERS #####
#                               #
# THE DEFAULT VALUES BELOW ARE  #
#  DETERMINED BY USER INPUTS    #
#                               #
#################################

default_term = ""  # can do a string of mult vals
default_categories = ""  # can do a string of mult vals
default_price = "4"  #"1, 2, 3"  # can do a comma del. list of values
default_location = "Hyde Park, Chicago"#"Lincoln Square, Chicago"  # create drop down for this
default_lim = 10
default_sort = "distance" #"review_count"
default_attributes = ""#"gender_neutral_restrooms"
# sorts by distance (other options are best_match, rating, review_count)

# temporarily use Kevin's API Key (abstract this into another film)
yelp_api_key = "GsAgBiywduecH_D-DDeB-ctBkWbUnFP_6w_b0CG4utMCu3s9Z3XIrNuyJum_NJ-FuIIsljD_7KTrOaHuZZjos6v-5-o5GSzfSsAVwySWhmlV4vnlN9ElxCE0xOBrWnYx"


def extract_yelp_data(yelp_api_key=yelp_api_key, term=default_term, 
    categories=default_categories, price=default_price, 
    location=default_location, limit=default_lim, sort_by=default_sort,
    attributes=default_attributes):
    """
    This function takes search results (a dictionary) and obtains the 
    name, zip code, address of the possible restaurant matches in the
    form of a pandas dataframe.

    Inputs:
        - yelp_api_key: a string of the Yelp API Key
        - term: a string of search terms input by the user
        - lat: a float representing either a user's current location 
                latitude or their desired location latitude
        - long: a float representing either a user's current location 
                longitude or their desired location longitude
        - limit: an integer of maximum number of Yelp results that
                    will be returned from the query
        - sort_by: string representing a user's sorting preference
                    (options are: distance, best_match, rating,
                    review_count)

    Outputs:
        - yelp_results: a pandas dataframe containing the zip code,
                        name, address, of each potential result.
    """
    yelp_api = YelpAPI(yelp_api_key)
    search_results = yelp_api.search_query(term=term,
                                           categories=categories,
                                           price=price,
                                           location=location,
                                           limit=limit,
                                           sort_by=sort_by,
                                           attributes=attributes)

    if not search_results:
        return None
    # initialize lists for each planned column in yelp_results df
    addresses = []
    names = []
    zip_code = []
    latitude = []
    longitude = []
    phone = []
    price = []
    
    # obtain business information
    businesses = search_results['businesses']
    for i in businesses:
        # print("LENGTH OF ADDRESSES:", len(addresses))
        # print("LENGTH OF NAMES:", len(names))
        # print("LENGTH OF ZIP:", len(zip_code))
        # print("LENGTH OF LAT:", len(latitude))
        # print("LENGTH OF LONG:", len(longitude))
        # print("LENGTH OF PHONE:", len(phone))
        # print("LENGTH OF PRICE:", len(price))
        # print("=============================================")

        # In case a Yelp business is missing a field:
        try:
            a_address = i['location']['display_address'][0]
            a_name = i['name']
            a_zip = i['location']['zip_code']
            a_latitude = i['coordinates']['latitude']
            a_longitude = i['coordinates']['longitude']
            a_phone = i['phone']
            a_price = i['price']

            if a_address != "" and a_name != "" and a_zip != "" \
                    and a_latitude != "" and a_longitude != "" and \
                    a_phone != "" and a_price != "":
                addresses.append(a_address)
                names.append(a_name)
                # filter out businesses without zip codes
                # if i['location']['zip_code'] != '':
                zip_code.append(a_zip)
                latitude.append(a_latitude)
                longitude.append(a_longitude)
                phone.append(a_phone)
                price.append(a_price)

        except KeyError:
            print("Key Error, some missing field from the Yelp return!")

    # cast into pandas dataframe
    yelp_results = pd.DataFrame()
    yelp_results['zip_code'] = zip_code
    yelp_results['name'] = names
    yelp_results['addr'] = addresses
    yelp_results['phone'] = phone
    yelp_results['price'] = price
    yelp_results['latitude'] = latitude
    yelp_results['longitude'] = longitude

    # yelp_results['lgbtq'] = 
    # yelp_results['gen_neutral'] =  

    # change zip code column to appropriate data type
    yelp_results['zip_code'] = pd.to_numeric(yelp_results['zip_code'])

    return yelp_results


def define_filters(yelp_results):
    """
    This function creates filters based on the Yelp query results
    we will use to query our database to obtain wages, food, etc.
    The zip codes represented in the Yelp result and latitudes/longitudes
    within the range represented in the Yelp result will be defined
    as the filters for querying the database.

    Input:
        - yelp_results: a pandas dataframe of the Yelp query results

    Output:
        - zip_filter: a set of unique zip codes in the Yelp results
        - latitude_filter: a set of unique truncated latitude coordinates
        - longitude_filter: a a set of unique truncated longitude coordinates
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
    This is function truncates coordinates to 3-decimal places.
	"""
    s = '{}'.format(coordinate)
    i, p, d = s.partition('.')
    trunc_coordinate = '.'.join([i, (d+'0'*3)[:3]])
    
    return trunc_coordinate


def get_filtered_food_df(zip_filter, lat_filter, long_filter):
    """
    This function takes the zip code, latitude, and longitude filters
    and queries the database to obtain information that fits within
    those filters. A pandas dataframe of filtered database
    information gets returned.

    Input:
        - zip_filter: a set of zip codes in the Yelp results
        - lat_filter: a set of truncated latitude coordinates
        - long_filter: a set of truncated longitude coordinates

    Output:
        - food_df: a pandas dataframe of food information
    """
    # filter django Food object based on zip code, latitude, & longitude
    food_filtered = Food.objects.filter(zip_code__in=zip_filter, 
        latitude__range=(min(lat_filter), max(lat_filter)), 
        longitude__range=(max(long_filter), min(long_filter)))

    # cast django FOOD object as dataframe if there is data
    if food_filtered.exists():
        food_df = food_filtered.to_dataframe(fieldnames=['zip_code', 'aka_name', 
            'address', 'inspection_id', 'latitude', 'longitude'])
        food_df = food_df.rename(index=str, columns={"aka_name": "name", 
            "address": "addr"})
    else:
        food_df = []
        
    return food_df
    

def get_filtered_wages_df(zip_filter, lat_filter, long_filter):
    """
    This function takes the zip code, latitude, and longitude filters
    and queries the database to obtain information that fits within
    those filters. A pandas dataframe of filtered database
    information gets returned.

    Input:
        - zip_filter: a set of zip codes in the Yelp results
        - lat_filter: a set of truncated latitude coordinates
        - long_filter: a set of truncated longitude coordinates
    Output:
        - wages_df: a pandas dataframe of wages information
    """
    #filter django Wages object based on zip code, latitude, & longitude
    wages_filtered = Wages.objects.filter(zip_code__in=zip_filter, 
        latitude__range=(min(lat_filter), max(lat_filter)), 
        longitude__range=(max(long_filter), min(long_filter)))

    # cast django WAGES object as dataframe is there is data
    if wages_filtered.exists():
        wages_df = wages_filtered.to_dataframe(fieldnames=['zip_code', 'trade_nm', 
            'street_addr_1_txt', 'case_id', 'latitude', 'longitude'])
        wages_df = wages_df.rename(index=str, columns={"zip_cd": "zip_code", 
            "trade_nm": "name", "street_addr_1_txt": "addr"})
    else:
        wages_df = []

    return wages_df


def get_filtered_divvy_df(lat_filter, long_filter):
    divvy_filtered = Divvy.objects.filter(
        latitude__range=(min(lat_filter), max(lat_filter)), 
        longitude__range=(max(long_filter), min(long_filter)))

    # cast django WAGES object as dataframe is there is data
    if divvy_filtered.exists():
        divvy_df = divvy_filtered.to_dataframe(fieldnames=['_id', 'name', 
            'city', 'latitude', 'longitude', 'capacity'])
        #divvy_df = divvy_df.rename(index=str, columns={  "street_addr_1_txt": "addr"})
    else:
        divvy_df = []

    return divvy_df


def get_filtered_enviro_df(lat_filter, long_filter):
    enviro_filtered = Env_Complaints.objects.filter(
        latitude__range=(min(lat_filter), max(lat_filter)),
        longitude__range=(max(long_filter), min(long_filter)))

    # cast django ENVIRONMENT object as dataframe is there is data
    if enviro_filtered.exists():
        enviro_df = enviro_filtered.to_dataframe(fieldnames=['pk',
                                                             'longitude',
                                                             'latitude',
                                                             'address'])
        enviro_df = enviro_df.rename(index=str, columns={"address": "addr"})
    else:
        enviro_df = pd.DataFrame()

    return enviro_df


def link_datasets(yelp_results, dj_df, df_type="wages"):
    """
    This functions compares Yelp results to database results and produces
    the best matches based on computing the qgram score between the
    zip_code, business name, address strings, latitude, and longitude. 

    Inputs:
        - yelp_results: a pandas dataframe of yelp business results based 
                        on a user's input
        - dj_df: a pandas dataframe of django results.
                 Ex. wages, healthcode violations, etc.

    Outputs:
        - link: a tuple containing the indices of Yelp results df and
        databse results df AND the best matches qgram scores
    """
    # set thresholds for comparing strings using qgram method
    name_thresh = 0.55
    addr_thresh = 0.55
    strong_addr_thresh = 0.90
    compare = rl.Compare()
    
    # Indexation 
    if df_type == "wages" or df_type == "food": 
        indexer = rl.BlockIndex(on='zip_code')
        compare.numeric('zip_code', 'zip_code', method='linear',
                        scale=30.0, label='zip_score')
        compare.string('name', 'name', method='qgram', 
            threshold=name_thresh, label='name_score')
        compare.string('addr', 'addr', method='qgram', 
            threshold=addr_thresh, label='addr_score')
    elif df_type == "enviro":
        indexer = rl.FullIndex()
        compare.string('addr', 'addr', method='qgram',
                       threshold=strong_addr_thresh, label='addr_score')
    else:
        indexer = rl.FullIndex()
    print(type(dj_df), "DF")
    pairs = indexer.index(yelp_results, dj_df)
    compare.geo('latitude', 'longitude', 'latitude', 'longitude',
                method='linear', scale=30.0, label='coord_score')

    # compute record linkage scores
    features = compare.compute(pairs, yelp_results, dj_df)

    # Classification and final filtering
    if df_type == "wages" or df_type == "food": 
        best_matches = features[(features['zip_score'] == 1.0) &
        (features['name_score'] == 1.0) & (features['addr_score'] == 1.0) &
        (features['coord_score'] >= 0.99)]
    elif df_type == "enviro":
        best_matches = features[(features['addr_score'] == 1.0) &
                                (features['coord_score'] >= 0.99)]
    else:
        best_matches = features[(features['coord_score'] >= 0.99)]
    # obtain the index values from best_matches
    index_array = best_matches.index.values

    # create tuple of indices and best matches df
    link = (index_array, best_matches)
    
    return link


def query_database(yelp_results, zip_filter, lat_filter, long_filter):
    """
    This function takes the best matches between the Yelp results and the
    database query and fetches the details of the respective FLAG 

    Input:
        - yelp_results: a dataframe of Yelp results
        - zip_filter: a set of zip codes
        - lat_filter: a set of latitude coordinates
        - long_filter: a set of longitude coordinates

    Output:
        - yelp_results: a dataframe of Yelp results with food inspection
                        information and date columns added
    """
    # obtain details from Food Table
    food_df = get_filtered_food_df(zip_filter, lat_filter, long_filter)
    food_link = link_datasets(yelp_results, food_df, df_type="food")
    f_index_array, f_best_matches = food_link

    # obtain details from Wages Table
    wages_df = get_filtered_wages_df(zip_filter, lat_filter, long_filter)
    wages_link = link_datasets(yelp_results, wages_df, df_type="wages")
    w_index_array, w_best_matches = wages_link

    # obtain details from Divvy table
    divvy_df = get_filtered_divvy_df(lat_filter, long_filter)
    divvy_link = link_datasets(yelp_results, divvy_df, df_type="divvy")
    d_index_array, d_best_matches = divvy_link

    # obtain details from Enviro table
    enviro_df = get_filtered_enviro_df(lat_filter, long_filter)
    print("PRINT ENVIRO DF", enviro_df)
    try:
        enviro_link = link_datasets(yelp_results, enviro_df, df_type="enviro")
        e_index_array, e_best_matches = enviro_link
    except:
        e_index_array = []

    # add relevant columns to yelp_results dataframe
    yelp_results['food_status'] = np.empty((len(yelp_results), 0)).tolist()
    yelp_results['food_date'] = np.empty((len(yelp_results), 0)).tolist()
    yelp_results['wages_violations'] = np.empty((len(yelp_results), 0)).tolist()
    yelp_results['divvy_stations'] = np.empty((len(yelp_results), 0)).tolist()
    yelp_results['env_complaints'] = np.empty((len(yelp_results), 0)).tolist()
    yelp_results['env_complaints_url'] = np.empty((len(yelp_results), 0)).tolist()
    yelp_results['env_enforce'] = np.empty((len(yelp_results), 0)).tolist()
    yelp_results['env_enforce_url'] = np.empty((len(yelp_results), 0)).tolist()


    # Get details from FOOD database table
    for index_pair in f_index_array:
        yelp_index, flag_index = index_pair[0], int(index_pair[1])
        _id = food_df.iloc[flag_index].inspection_id
        # query the relevant database table
        f_row = Food.objects.get(inspection_id=_id)
        result = f_row.results
        # only include non-passes
        #if result != "Pass": 
        # obtain the business name
        name = f_row.aka_name

        # obtain violation information (necessary?)
        #violation = table_row.violations

        # obtain date and format the date 
        d = str(f_row.inspection_date.day)
        m = str(f_row.inspection_date.month)
        y = str(f_row.inspection_date.year)
        format_date = m + " " + d + " " + y

        # obtain inspection type
        insp_type = f_row.inspection_type
        t = (flag_index, name, result, format_date, insp_type)
        
        # add to the yelp results data frame
        yelp_results['food_status'].iloc[yelp_index].append(t[2]) 
        yelp_results['food_date'].iloc[yelp_index].append(t[3])

    # Get details from WAGES database table
    for index_pair in w_index_array:
        yelp_index, flag_index = index_pair[0], int(index_pair[1])
        _id = wages_df.iloc[flag_index].case_id
        # query the relevant database table
        w_row = Wages.objects.get(case_id=_id)

        # obtain the wanted business information
        violations = w_row.case_violtn_cnt
        name = w_row.trade_nm

        t = (flag_index, name, violations)
        
        # add to the yelp results data frame
        yelp_results['wages_violations'].iloc[yelp_index].append(t[2]) 

    # get details for the DIVVY table
    for index_pair in d_index_array:
        yelp_index, flag_index = index_pair[0], int(index_pair[1])
        name = divvy_df.iloc[flag_index]['name']
        
        # ALREADY HAVE NAME ?? query the relevant database table
        # d_name = Divvy.objects.get(name=name)
        
        # add to the yelp results data frame
        yelp_results['divvy_stations'].iloc[yelp_index].append(name)

    # Get details from Environment database table
    for index_pair in e_index_array:
        yelp_index, flag_index = index_pair[0], int(index_pair[1])
        pk = enviro_df.iloc[flag_index].pk

        # query the relevant database table
        e_row = Env_Complaints.objects.get(pk=pk)

        # obtain the wanted business information
        complaints = e_row.complaints
        complaints_url = e_row.complaints_url
        enviro_enforcement = e_row.enviro_enforcement
        enviro_enforcement_url = e_row.enviro_enforcement_url

        #t = (flag_index, name, violations)

        # add to the yelp results data frame
        yelp_results['env_complaints'].iloc[yelp_index].append(complaints)
        yelp_results['env_complaints_url'].iloc[yelp_index].append(complaints_url)
        yelp_results['env_enforce'].iloc[yelp_index].append(enviro_enforcement)
        yelp_results['env_enforce_url'].iloc[yelp_index].append(enviro_enforcement_url)
    
    return yelp_results


def final_result(dict_from_views):
    """
    This function takes the users inputs as a dictionary, queries Yelp,
    defines the zip/lat/long filters, completes record linkage between
    Yelp and the tables within the databse, and returns a final dataframe
    to be sent back to Views.

    Input:
        - dict_from_views: a dictionary of user inputs
    Output:
        - final_result a pandas dataframe

    """
    term = dict_from_views['term']
    categories = dict_from_views['categories']
    price = dict_from_views['price']
    location = dict_from_views['location']
    lim = 50
    sort = dict_from_views['sort']
    attributes = dict_from_views['attributes']

    yelp_results = extract_yelp_data(yelp_api_key=yelp_api_key, term=term, 
        categories=categories, price=price, location=location, limit=lim, 
        sort_by=sort, attributes=attributes)

    zip_filter, lat_filter, long_filter = define_filters(yelp_results)

    final_result = query_database(yelp_results, zip_filter,
                                  lat_filter, long_filter)

    return final_result
    

