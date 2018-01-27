#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 15:08:51 2018

@author: ty
 
Modified code from: https://github.com/Yelp/yelp-fusion/blob/master/
                     fusion/python/sample.py
                     
 ---Original Comments from Yelp-----
                   
# -*- coding: utf-8 -*-
Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
# Next import from We Can
from collections import namedtuple


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
  
 # Import out API key (We Can)
from api_keys import yelp
API_KEY= yelp
REQUEST_COUNT = 24990


# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults 
DEFAULT_TERM = 'bar'
DEFAULT_LOCATION = 'Chicago, IL'
SEARCH_LIMIT = 3


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)
    return response

def yelp_run_query(term, location):#, request_count = REQUEST_COUNT):
    '''
    This function takes the Yelp API documentation code designed to be run
    from the command line, and turns it into a function which returns results
    rather than printing to the terminal. All code is from Yelp, unless 
    otherwise noted. 
    
    Inputs:
        term: a term for which to search, string, e.g., "bars"
        location: a place in which to search, string, e.g., "Chicago"
    Outputs:
        JSON dictionary of request result
    '''
    
    
    # These next few lines are We Can's code, all else is Yelp
    # Decrement our request count and let us know
    #print('\n Remaining Queries: ', request_count - 1)
    # Set input values
    #input_value_tuple = namedtuple('inputs', ('term', 'location'))
    #input_values = input_value_tuple(term, location)
    
    try:
        return_val = query_api(term, location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    return return_val#, request_count -= 1


# -------- Business Joins ------ 
    
# Yelp business matching 


# https://www.yelp.com/developers/documentation/v3/business_match
#  provide incomplete info and yelp will match it w/ 1 or 10 options
    

# ----- Autocomplete ----------

# yelp also has autocomplete functionality
    

# https://www.yelp.com/developers/documentation/v3/autocomplete
    

# ------ Reviews --------
    
# https://www.yelp.com/developers/documentation/v3/business_reviews
    


# ------- Detailed business data -------
    
# https://www.yelp.com/developers/documentation/v3/business




# ---------- Transaction type -----
    
# can check for restos that do delivery, etc. Most interesting is reservations
# https://www.yelp.com/developers/documentation/v3/transactions_search
