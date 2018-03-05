# We Can Have Nice Things

Repository for CAPP 30122 Winter 2018 Project

  * Alexander Tyan (AlexanderTyan)
  * Kevin Sun (Sun-Kev)
  * Tyler Amos (tamos)
  
  
# Dependencies:

 * django-geojson: https://django-geojson.readthedocs.io/en/latest/installation.html

 * leaflet: http://leafletjs.com

 * django-leaflet: https://django-leaflet.readthedocs.io

 * record_linkage: http://recordlinkage.readthedocs.io
 
 * yelpapi: https://github.com/gfairchild/yelpapi
 
 * pandas: https://pandas.pydata.org
 
 * requests: 


# Sign up for the following API's:

Google Maps: https://developers.google.com/maps/documentation/geocoding/intro

Mapbox (for tile layers): https://www.mapbox.com

Chicago Data Portal: https://data.cityofchicago.org
  
  
# To Set Up The App:

## 1. Install PostgreSQL

Recommended: https://postgresapp.com


## 2. Create a PostgrSQL User nice_things

#### On Mac/Linux

  ``` sudo -u postgres psql ```
  
  ```CREATE USER nice_things LOGIN password ''; ```
  
  ```CREATE DATABASE nice_things_db OWNER nice_things;```
  
  Leave PostgresSQL running and now, in terminal:
  
  ```python3 manage.py makemigrations```
  
  ```python3 manage.py migrate```
  
  Open the shell:
  
  ```python3 manage.py shell```
  
  ```import update_db```
  
  ```update_db.update_food_table()```
  
  ```update_db.update_wages_table()```
  
  ```python3 manage.py runserver```
  
  
 # Data Sources
 
 
 Bureau of Labour Statistics: https://enforcedata.dol.gov/views/data_summary.php
 
 
