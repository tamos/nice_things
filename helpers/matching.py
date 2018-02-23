#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 20:17:53 2018

@author: ty
"""
import pandas as pd
from data.api_keys import yelp
from jellyfish import jaro_distance
from yelpapi import YelpAPI
from itertools import product
# query yelp


default_term = "bars"
default_lat = 41.8369
default_lon = -87.6847
# this is how the yelp api works
yelp_api = YelpAPI(yelp)
search_results = yelp_api.search_query(term=default_term,
                                       latitude=default_lat,
                                       longitude=default_lon)

# use region key to get lattitude, longitude


def extract_yelp_data(search_results):
    """
    Takes search results and gets the name, zip, address
    """
    # display address
    # zip code
    # name
    col_names = ['zip_code', 'addr', 'name']
    addresses = []
    names = []
    zip_code = []
    businesses = search_results['businesses']
    for i in businesses:
        #print(i.keys())
        addresses.append(i['location']['display_address'][0])
        names.append(i['name'])
        zip_code.append(i['location']['zip_code'])
    
    yelp_results = pd.DataFrame()
    yelp_results['zip_code'] = zip_code
    yelp_results['names'] = names
    yelp_results['addr'] = addresses
    return yelp_results


def django_to_df_wages(django_result):
    dj_df = pd.DataFrame
    names = []
    addr = []
    zip_code = []
    case_id = []
    for i in django_result:
        names.append(i.trade_name)
        addr.append(i.street_addr1_txt)
        zip_code.append(i.zip_cd)
        case_id.append(i.case_id)
    dj_df['names'] = names
    dj_df['addr'] = addr
    dj_df['zip_code'] = zip_code
    dj_df['case_id'] = case_id
    return dj_df


def django_to_df_food(django_result):
    dj_df = pd.DataFrame
    names = []
    addr = []
    zip_code = []
    inspection_id = []
    for i in django_result:
        names.append(i.aka_name)
        addr.append(i.address)
        zip_code.append(i.zip)
        inspection_id.append(i.inspection_id)
    dj_df['names'] = names
    dj_df['addr'] = addr
    dj_df['zip_code'] = zip_code
    dj_df['inspection_id'] = inspection_id
    return dj_df


yelp_results = extract_yelp_data(search_results)
dj_df = yelp_results.copy()
dj_df['inspection_id'] = 0


def compare_distance(yelp_results, dj_df, thresholds):
    """ 
    Compare yelp results to django results and produce best
    matches
    """
    zip_threshold, name_threshold, addr_threshold = thresholds
    results = dict()
    for i in product(['high','low'], repeat = 3):
        if i not in results:
            results[i] = dict()
    
    # inspired by pa4 util function
    for i in yelp_results.iterrows():
        
        y_id, y_zip, y_name, y_addr = i[0], i[1][0], i[1][1], i[1][2] 
        y_tuple  = (y_id, y_zip, y_name, y_addr)
            
        for j in dj_df.iterrows():
            print(j)
            dj_index, dj_zip, dj_name, dj_addr, dj_id = j[0], j[1][0], j[1][1], j[1][2], j[1][3]
            
            zip_score = jaro_distance(y_zip, dj_zip)
            if zip_score >= zip_threshold:
                zip_verdict = 'high'
            else:
                zip_verdict = 'low'
                
            name_score = jaro_distance(y_name, dj_name)            
            if name_score >= name_threshold:
                name_verdict = 'high'
            else:
                name_verdict = 'low'
                
            addr_score = jaro_distance(y_addr, dj_addr)
            if addr_score >= addr_threshold:
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
        return yelp_results
        
        

    #       
            
            
#compare_distance(yelp_results, dj_df, (0.5, 0.5, 0.5))
    


