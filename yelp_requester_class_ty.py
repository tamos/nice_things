
"""

This file contains code for making request to the Yelp API.
 
Modified code is taken from: https://github.com/Yelp/yelp-fusion/blob/master/
                     fusion/python/sample.py
"""



from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

from api_keys import yelp
API_KEY= yelp

#### Below is code from Yelp ####

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

# API constants
API_HOST = "https://api.yelp.com"
SEARCH_PATH = "/v3/businesses/search"
BUSINESS_PATH = "/v3/businesses/"  # Business ID will come after slash.
BEST_MATCH_PATH = BUSINESS_PATH + "matches/best"
TOP_10_MATCHES_PATH = BUSINESS_PATH + "matches/lookup"

# Defaults 
DEFAULT_TERM = 'bar'
DEFAULT_LOCATION = 'Chicago, IL'
DEFAULT_CITY = "Chicago"
DEFAULT_STATE = "IL"
DEFAULT_COUNTRY = "US"
SEARCH_LIMIT = 3

class YelpAPIRequester(object):
    
    def __init__(self):
        from api_keys import yelp
        self.API_KEY = yelp

    def request(self, host, path, url_params=None):
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
            'Authorization': 'Bearer %s' % self.API_KEY,
        }
    
        print(u'Querying {0} ...'.format(url))
    
        response = requests.get(url, headers=headers, params=url_params)
    
        return response.json()
    
    
    def search(self, term, location = DEFAULT_CITY + ", " + DEFAULT_STATE):
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
        return self.request(API_HOST, SEARCH_PATH, url_params=url_params)
    
    
    def get_business(self, business_id):
        """Query the Business API by a business ID.
    
        Args:
            business_id (str): The ID of the business to query.
    
        Returns:
            dict: The JSON response from the request.
        """
        business_path = BUSINESS_PATH + business_id
    
        return self.request(API_HOST, business_path)
    
    
    def query_api(self, term, location):
        """Queries the API by the input values from the user.
    
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        """
        response = self.search(term, location)
    
        businesses = response.get('businesses')
    
        if not businesses:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            return
    
        business_id = businesses[0]['id']
    
        print(u'{0} businesses found, querying business info ' \
            'for the top result "{1}" ...'.format(
                len(businesses), business_id))
        response = self.get_business(business_id)
    
        print(u'Result for business "{0}" found:'.format(business_id))
        pprint.pprint(response, indent=2)
        return response
    
    def yelp_run_query(self, term, location):#, request_count = REQUEST_COUNT):
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
            return_val = self.query_api(term, location)
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
        # got this working, but not very well. 
    
    def match_business(self, business_name):
        """ Matches businesses"""
        
        return self.request(API_HOST, TOP_10_MATCHES_PATH, url_params = {'name': business_name, \
                                                                'city': DEFAULT_CITY,\
                                                                'state': DEFAULT_STATE, \
                                                                'country': DEFAULT_COUNTRY})
        


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
