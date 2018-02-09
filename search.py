######### Structure & Steps ##########
from jellyfish import jaro_distance
from queue import PriorityQueue
# This package that was deprecated. We updated it and submitted a pull
# request to the author, this is the updated package. 
from yelpapi import YelpAPI
# Our API key is stored in a separate file
import api_keys
import cdp_tokens
import requests
import pandas as pd
import io

default_term = "bars"
default_lat = 41.8369
default_lon = -87.6847

# empty set for now
places_set = set()
inputs = {'location': (default_lat, default_lon), 'price': 1, 'type': 1}

def go(inputs, places_set):
    """
    This function ties all of the steps together.

    Input:
    	-
    Output:
    	- 

    """
    pass

##### STEP 1 #####
def get_user_inputs():
	"""
	!!! This step will actually need to be completed in views !!! 

	This function gets the python dictionary that contains the
	preferences the user has input into the front-end of the
	application.

	Input:
		- Location: a tuple of floats (longitude and latitude)
		- Price: an integer 1, 2, 3, 4 (Ex. $ is 1, $$ is 2)
		- Type: a string (ex. "restaurant" or "bar")

	Output:
		- user_pref_dict: a dictionary that maps the keys (location, price,
		type) to the values input by the user.
	"""
	pass
	return user_pref_dict

##### STEP 2A #####	
LEGAL_DICT_INPUTS = {"inspection_id", "dba_name", "aka_name", "license_",
					 "facility_type", "risk", "address", "city", "state",
					 "zip", "inspection_date", "inspection_type", "results",
					 "violations", "latitude", "longitude", "location",
					 "location_city","location_address", "location_zip",
					 "location_state"}

def query_database(user_pref_dict):
	"""
	This function queries the database containing FLAGS, FOOD,
	and WAGES tables and returns a list of relevant business names
	and accompanying attributes of that business.

	Input:
		- user_pref_dict: a dictionary containing user's preferences on
						  Location, price, and type of business they are
						  looking for
	Output:
		- database_list: list of lists containing results from querying the
						 database. Each list contains the following:
						- business name: string 
						- longitude: float
						- latitude: float
						- business type: a string (ex. "restaurant" or "bar")
	"""
	pass
	database_list =[]
	return database_list

##### STEP 2B #####
def query_yelp(user_pref_dict):
	"""
	This function queries YELP using the Yelp API and returns a list of
	relevant business names and accompanying attributes of that business.

	Input:
		- user_pref_dict: a dictionary containing user's preferences on
						  Location, price, and type of business they are
						  looking for
	Output:
		- yelp_list: list of lists containing results from querying the
						 database. Each list contains the following:
						- business name: string 
						- longitude: float
						- latitude: float
						- business type: a string (ex. "restaurant" or "bar")

	"""
            
	default_term = "bars"
	default_lat = 41.8369
	default_lon = -87.6847
	yelp_list = []
	return yelp_list

    # this is how the yelp api works

	#yelp_api = YelpAPI(api_keys.yelp)
	#search_results = yelp_api.search_query(term = default_term, \
                                       #latitude = default_lat,\
                                       #longitude = default_lon)

    # some pseudocode
    #yelp_api = YelpAPI(api_keys.yelp)
    #inputs['location'] = trunc_coordinates(inputs['location'])
    #search_results = yelp_api.search_query(term = default_term, \
                                      # latitude = default_lat,\
                                       #longitude = default_lon)
    #if match_places(inputs['location'], places_set):
        #query_results = query(inputs_to_query)
        #result_names = [i['name']for i in search_results['businesses']]
        #for i in result_names:
            #if name_distance(i, query_results.name):
                #add the query result to the yelp result
            # return to the user the results


##### STEP 3 #####
def join_by_name_distance(yelp_result, candidates, threshold = 0.75):
    """ 
    ### Kevin's suggestion: change match to match_list 
    ### Edit: function needs to match on yelp_list and database_list

    This function calculates the Jaro distance between two strings. 
    If this is above the threshold, it returns the best match.
    
    Inputs:
        - yelp_results: A yelp result (name) as a string (string)
        - candidates: A list of candidate matching names (strings)
        
    Outputs:
        - match: best match for the yelp_result (string)
        If there is no match above the threshold, then None
        
    """
    yelp_result = yelp_list
    #match_list = []
    eligible_matches = PriorityQueue()
    # for now candidates and yelp_result are simple strings
    # we can make that more complex if needed
    for i in candidates:
        eligible_matches.put((1 - jaro_distance(yelp_result, i), i))
    match = eligible_matches.get()[1]
    if match >= threshold:
        return match
    else:
        return None

##### STEP 4 #####
def rank_matches(match_list):
	"""
	This function ranks the matches to be returned to the user.

	Inputs:
		- match_list: a list of lists of matched businesses and
					  relevant attributes
	Outputs:
		- ranked_match_list: a list of lists of ranked matched
							 businesses and relevant attributes
	"""
	return ranked_match_list

##### STEP 5 ##### 
def final_result(ranked_match_list):
	"""
	# This function may not be necessary

	This functions takes the ranked_match_list and transforms it into
	an appropriate form to be delivered to Django.

	Input:
		- ranked_match_list: a list of lists of ranked matched
							 businesses and relevant attributes

	Output:
		- final_result: TBD
	"""

	return final_result

##### Auxilary Functions to be sorted #####

def pull_cdp_health_api(input_dict, output_csv=None, limit=None,
						legal_dict_inputs=LEGAL_DICT_INPUTS):
	"""
	Connects to the Chicago Data Portal and downloads the Food Inspections
	data set according to user preferences specified in the function
	parameters
	:param input_dict: dictionary of params for what fields from the dataset
	to include and how to filter them. Dict keys are strings. For full field
	interpretation see "cdp_food_inspections_description.pdf"
		Options for keys:
			inspection_id: number
			dba_name: text, all capital letters
			aka_name: text, all capital letters
			license_: number
			facility_type: text
			risk: text
			address: text, all capital letters
			city: text, all capital letters
			state: text
			zip: number
			inspection_date: floating_timestamp
			inspection_type: text
			results: text
			violations: text
			latitude: number
			longitude: number
			location: point
			location_city: text
			location_address: text
			location_zip: text
			location_state: text
	:param output_csv: string, write out a csv file with this string as a name.
					   WILL OVERWRITE EXISTING FILE IF NAME MATCHES!
	:param limit: integer, limit how many most recent rows. API returns 1000 by
				  default.
	:param legal_dict_inputs: possible keys for the input_dict
	:return: pandas filtered dataframe.
	"""
	# Check input_dict is a dictionary:
	if not isinstance(input_dict, dict):
		raise AssertionError("Not a dictionary in input_dict input!")

	# Check output_csv is a string:
	if output_csv and not isinstance(output_csv, str):
		raise AssertionError("Not a string in output_csv input!")

	# Concatenate URL:
	source_url = "https://data.cityofchicago.org/resource/cwig-ma7x.csv"
	# Make sure to get the latest inspection rows by date:
	concatenate_url = source_url + "?$order=inspection_date DESC"
	if limit:  # If want to limit how many rows
		concatenate_url += "&$limit=" + str(limit)

	for key, value in input_dict.items():
		# Foolproof key inputs:
		if key not in legal_dict_inputs:
			raise AssertionError("Not a valid key provided in the input dictionary!")
		api_string_to_add = "&{}={}".format(key, value)
		concatenate_url += api_string_to_add

	# Get into API (with app tokens, there's no throttling limit):
	app_token = cdp_tokens.APP_TOKEN
	socrata_headers = {'X-App-Token': app_token}
	r = requests.get(url=concatenate_url, headers=socrata_headers)

	# Process the data:
	csv_data = r.text
	df = pd.read_csv(io.StringIO(csv_data), index_col="inspection_id")

	# Dump into csv, if necessary:
	if output_csv:
		df.to_csv(output_csv)

	return df


def trunc_coordinates(coordinate, n):
    """
    This function truncates a coordinate of a user's location.

    Inputs:
        - coordinate: a float (longitude or latitude)

    Outputs:
        - new_coordinate: a float (longitude or latitude) truncated
	
	Citation: 
		https://stackoverflow.com/questions/783897/truncating-floats-in-python
    """
    s = '{}'.format(coordinate)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(coordinate, n)
    i, p, d = s.partition('.')
    new_coordinate = '.'.join([i, (d+'0'*n)[:n]])
    return new_coordinate

### This function is removed for now - not currently in use ###
def match_places(coordinates, places_set):
    """
    This function checks whether the user's now-truncated coordinates
    are contained within the set of longitude/latitude coordinates.

    Inputs:
        - coordinates: a tuple (longitude, latitude)

    Outputs:
        - a boolean
    """
    if coordinates in places_set:
        return True
    else:
        return False

