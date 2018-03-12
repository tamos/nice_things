# We Can Have Nice Things

Repository for CAPP 30122 Winter 2018 Project

  * Alexander Tyan (AlexanderTyan)
  * Kevin Sun (Sun-Kev)
  * Tyler Amos (tamos)
  
  
# Dependencies

 * django-geojson: https://django-geojson.readthedocs.io/en/latest/installation.html

 * leaflet: http://leafletjs.com

 * django-leaflet: https://django-leaflet.readthedocs.io

 * record_linkage: http://recordlinkage.readthedocs.io
 
 * yelpapi: https://github.com/gfairchild/yelpapi
    * This package was updated by the group and submitted as a pull request. See https://github.com/gfairchild/yelpapi/pull/8
 
 * pandas: https://pandas.pydata.org
 
 * requests: http://docs.python-requests.org/en/master/
 
 * dominate: https://github.com/Knio/dominate


# Sign up for the following APIs:

Google Maps: https://developers.google.com/maps/documentation/geocoding/intro

Mapbox (for tile layers): https://www.mapbox.com

Chicago Data Portal: https://data.cityofchicago.org
  
  
# Set up

### 1. Install PostgreSQL

Recommended: https://postgresapp.com

### 2. Now create a PostgrSQL user nice_things. In PostgreSQL:
  
  CREATE USER nice_things LOGIN password '';

You may need to specify a password. If that happens, go to nice_things_django_project/settings.py and change the following line:
  'PASSWORD': ''
  
  To:
  
  'PASSWORD': 'uccs'
  
 And then try:
 
  CREATE USER nice_things LOGIN password 'uccs';
  
  CREATE DATABASE nice_things_db OWNER nice_things;
  
### 3. Leave PostgresSQL running and now, in a new terminal:
  
  python3 manage.py makemigrations
  
  python3 manage.py migrate
  
### 4. Open the shell with:
  
  python3 manage.py shell
  
  import update_db
  
  update_db.update_database()
  
### 5. Exit to terminal, and:
  
  python3 manage.py runserver
  
### 6. Enjoy your nice things. 



# Code Attribution

Due to the design of the project, all areas of code were worked on by all members. 


# References

1. Python documentation (python.org)
2. W3Schools (w3schools.com)
3. Leaflet (leafletjs.com)
4. For each package or API used, our code draws from examples and tutorials provided in the documentation.
5. When external resources, e.g., StackOverflow were consulted, they are cited in the code. 

# Data Sources
 
 #### Bureau of Labor Wage and Hour Compliance Data: https://enforcedata.dol.gov/views/data_summary.php
 
"The dataset contains all concluded WHD compliance actions since FY 2005. The dataset includes whether any violations were found and the back wage amount, number of employees due back wages, and civil money penalties assessed. " (Ibid)
 
 #### City of Chicago Data Portal: https://data.cityofchicago.org
 
 1. Environmental Records Lookup: https://data.cityofchicago.org/Environment-Sustainable-Development/CDPH-Environmental-Records-Lookup-Table/a9u4-3dwb
 
 "This dataset serves as a lookup table to determine if environmental records exist in a Chicago Department of Public Health (CDPH) environmental dataset for a given address." (Ibid)
 
 From this dataset, we use: 
 
 "COMPLAINTS: A ‘Y’ indicates that one or more records exist in the CDPH Environmental Complaints dataset." and "ENFORCEMENT: A ‘Y’ indicates that one or more records exist in the CDPH Environmental Enforcement dataset. " (Ibid)
 
 2. Food Inspections: https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5
 
"This information is derived from inspections of restaurants and other food establishments in Chicago from January 1, 2010 to the present. Inspections are performed by staff from the Chicago Department of Public Health’s Food Protection Program using a standardized procedure. The results of the inspection are inputted into a database, then reviewed and approved by a State of Illinois Licensed Environmental Health Practitioner (LEHP). For descriptions of the data elements included in this set, go to http://bit.ly/tS9IE8 "  (Ibid) 

3. Divvy Bike Share Locations: https://www.divvybikes.com/system-data (Q3/4 2017)

Q3 and Q4 data for 2017 was used to identify the locations of Divvy stations. The data was provided with the trips dataset which can be downloaded above. The data used in this repository was downloaded on March 5, 2018.
 
 
 
 
 
