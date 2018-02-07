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
    This function ties it all together.
    """
    pass
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
    

##### STEP 1 #####
# Get user inputs

# User input form - a python dictionary with the keys and values:
    # Location: named tuple of floats
    # Price: 1, 2, 3, 4 (Ex. $ is 1, $$ is 2)
    # Type: 1, 2, 3 (Ex. Restaurant is 1, Bar is 2)

def trunc_coordinates(coordinates):
    """
    This function truncates longitude and latitude coordinates of a user's
    location.

    Inputs:
        - coordinates: a tuple (longitude, latitude)

    Outputs:
        - coordinates: a tuple (longitude, latitude) with values truncated

    """
    l = []
    for coordinate in coordinates:
        l.append('%.3f'%(coordinate))
    new_coordinates = tuple(l)
    return new_coordinates


##### STEP 2 #####
# Match user inputs with places set

# Places set contains tuples of latitudes and longitudes.  

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

##### STEP 3 #####
# If user input in places set then query the database

LEGAL_DICT_INPUTS = {"inspection_id", "dba_name", "aka_name", "license_",
					 "facility_type", "risk", "address", "city", "state",
					 "zip", "inspection_date", "inspection_type", "results",
					 "violations", "latitude", "longitude", "location",
					 "location_city","location_address", "location_zip",
					 "location_state"}


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

# Using "place" as a parameter query flags table. Then go to health, labour,
# environmental, etc. tables and query those tables. 
	# flags JOIN health -> returns healthcode data
	# flags JOIN labour -> returns labour data
	# flags JOIN environment -> returns env data
		# put returned flags data into a queue and have a function match
		# the flags with businesses
		

##### STEP 4 #####
# Query Yelp based on user input
        
default_term = "bars"
default_lat = 41.8369
default_lon = -87.6847
        # this is how the yelp api works
#yelp_api = YelpAPI(api_keys.yelp)
#search_results = yelp_api.search_query(term = default_term, \
                                       #latitude = default_lat,\
                                       #longitude = default_lon)


##### STEP 5 #####
# Match Yelp results with database 

def name_distance(yelp_result, candidates, threshold = 0.75):
    """ 
    This function calculates the Jaro distance between two strings. 
    If this is above the threshold, it returns the best match.
    
    Inputs:
        - yelp_results: A yelp result (name) as a string (string)
        - candidates: A list of candidate matching names (strings)
        
    Outputs:
        - match: the best match for the yelp_result (string)
        If there is no match above the threshold, then None
        
    """
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
        
            
##### STEP 6 #####
# Return results