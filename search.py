######### Structure & Steps ##########
from jellyfish import jaro_distance
from queue import PriorityQueue
# This package that was deprecated. We updated it and submitted a pull
# request to the author, this is the updated package. 
from yelpapi import YelpAPI
# Our API key is stored in a separate file
import api_keys


def go():
    """
    This function ties it all together.
    """
    pass
    
    



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