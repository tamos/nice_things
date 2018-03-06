# Notes

## March 6

 - Will do attributions as ### attribute  ######
 
 - Gender neutral washrooms as a feature/points of conciousness
 - have radius functionality
 - Offset function
 - New archview resto
 - Uchicago pub - all pass
 - falcon inn - all pass
 - bracket room - failed
 - rajun cajun - failed
 
File style:

"""
This file does blab blah
"""
 
'#####' this code comes from: link  '#######'
 
Comment style:

"""
blablahballabahah

Double quotes

Input:
    - variable_name (type): description
Output
 
"""

 - double quotes everywhere

'#####' below is We Can's code  '#######'





# log in

sudo -u postgres psql

# IN PostgreSQL

CREATE USER nice_things LOGIN password 'uccs';

CREATE DATABASE nice_things_db OWNER nice_things;

# now switch to terminal and 

python3 manage.py makemigrations

# Now actually do the migrations

python3 manage.py migrate

# then run python commands to load in data

manage.update_food_table()

# etc

from itinerary.models import *

# access objects

Food.objects.all() # all the rows

# start up the shell

python3 manage.py shell

# start the server

python3 manage.py runserver



 
