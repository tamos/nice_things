######### Structure & Steps ##########
from jellyfish import jaro_distance
import numpy as np
from collections import namedtuple
from queue import PriorityQueue


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



##### STEP 5 #####
# Match Yelp results with database 

def name_distance(yelp_result, candidates, threshold = 0.75):
    """In: yelp_results (string)
    candidates (list of strings)
    Out: distance between strings
    """
    eligible_matches = PriorityQueue()
    for i in candidates:
        eligible_matches.put((1 - jaro_distance(yelp_result, i), i))
    return eligible_matches.get()[1]
            
    
    
    


##### STEP 6 #####
# Return results