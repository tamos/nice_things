######### Structure & Steps ##########

##### STEP 1 #####
# Get user inputs

# User input form - a python dictionary with the keys and values:
	# Location: named tuple of floats
	# Price: 1, 2, 3, 4 (Ex. $ is 1, $$ is 2)
	# Type: 1, 2, 3 (Ex. Restaurant is 1, Bar is 2)


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



##### STEP 6 #####
# Return results