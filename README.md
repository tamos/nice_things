# We Can Have Nice Things

Repository for CAPP 30122 Winter 2018 Project

  * Alexander Tyan (AlexanderTyan)
  * Kevin Sun (Sun-Kev)
  * Tyler Amos (tamos)

### Overall code description:

This django web app takes user-defined inputs and searches for bars/restaurants and other businesses based on those inputs. It returns information about that business, including information on issues users care about (e.g., labour code violations). Armed with this information, users can make better decisions about where they spend their money. 

The project is implemented in Django. Every time a user uses the front-end (html in `index.html`, interacting with Django forms in `forms.py`, with html requests processed by `views.py`), the code makes an API request to Yelp to find relevant businesses according to that search criteria. The package used for Yelp API was deprecated, but Tyler Amos updated it via a GitHub contribution (details below in "Python Modules and Tools Used").

The program then does record linkage with data in the database (Yelp request and matching code is in `matching.py`). During the project set-up, the database schema is constructed using Django models (`models.py`, with database access settings stored in `settings.py`). We populate the database from CSV files using `update_db.py`. The CSVs are from sources listed in the Data Sources section at the end of this `README.md`. These sources present "social consciousness" data that may be interesting to 
a user, such as establishments' environment, labour, and food records, as well as nearby Divvy bike stations.

Once matches are made with the Yelp results, the user is redirected to search results rendered by `map.html` in conjunction with `forms.py` and html request handler `views.py`.

### Set up:

### 1. Install dependencies:

`cd` into your local clone of the repository nice_things, where requirements.txt is located. If you are using UChicago's student Ubuntu VM, we recommend installing and following the  rest of the instructions using sudo's -H flag  (e.g. `sudo -H apt-get install postgresql postgresql-contrib` for PostgreSQL installation later). If on UChicago's Student Ubuntu VM, enter :

`sudo -H pip3 install -r requirements.txt`

Otherwise, enter:

`pip3 install -r requirements.txt`

(We are assuming you have pip3 already installed)

### 2. Install PostgreSQL

Follow the instructions on django-girls (URL below) for PostgreSQL install according to your OS. (NOTE: For creating the database user and the database, follow step 3 in this README instead of django-girls).

`https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/`

### 3. Let's create a PostgreSQL user nice_things and our nice_things_db database:

Let's go to psql. If ON UChicago's Student Ubuntu VM, enter into terminal:

`sudo -H -u postgres psql`

Otherwise:

`sudo -u postgres psql`

Now, we should see the command line starting with something like `postgres=#`.

Now, let's create the database user. If NOT ON UChicago's Student Ubuntu VM, enter:

`CREATE USER nice_things;`

If ON UChicago's Student Ubuntu VM, enter :
  
`CREATE USER nice_things LOGIN password 'uccs';`

You should see `CREATE ROLE` in the console if the user was created successfully.

If ON UChicago's Student Ubuntu VM, you also need to specify the "uccs" password to Django settings. To do so, go to `nice_things/nice_things_django_project/settings.py`and change the `DATABASES` variable's line:

`'PASSWORD': ''`
  
to:
  
`'PASSWORD': 'uccs'`
  
Next, let's create the database owned by our new nice_things user. Back in our 
`psql`, enter: 
  
`CREATE DATABASE nice_things_db OWNER nice_things;`

If the database was created successfully, you should see `CREATE DATABASE`
in the console.

### 4. Let's start our PostgreSQL server and create the schema (which our project predefined in Django's models.py) in nice_things_db database:

Start PostgreSQL server. In UChicago's Student Ubuntu VM terminal:

`sudo -H /etc/init.d/postgresql start`

If you are on MacOS and installed Postgres.app from django-girls instructions in step 2, you can start this installed app and start server from there. Otherwise, enter this into your terminal:

`sudo /etc/init.d/postgresql start`

Leave the server running and in a NEW terminal window, `cd` to `nice_things/nice_things_django_project/`, where `manage.py` is and enter:
  
`python3 manage.py makemigrations`

Once that is done running, enter:
  
`python3 manage.py migrate`

This will have created our database schema.
  
### 5. Let's now push all of our data into the nice_things_db database. 

Open the Django manage.py shell (in the same directory as in step 4):
  
`python3 manage.py shell`
  
Once in the python shell, let's run:
  
`import update_db`

Then:
  
`update_db.update_database()`

This will populate our nice_things_db with the data in the CSV files (stored in the `data` folder). Once that's done, you may `exit()` the shell.
  
### 6. Let's start our Django development server to see our app in action:
  
In the same folder, where `manage.py` is, enter in terminal:

`python3 manage.py runserver`
  
### 7. Enjoy your nice things: 

Copy the address (something like `http://127.0.0.1:8000/` from the command in step 6) into your web browser and try some search queries. When you search for results in Los Angeles or Miami, you will get the base results (address, name, location on a map) but none of our supplemental data. At present, supplemental data is only provided for Chicago.

#### Queries to Try:

Where: "Hyde Park"
Search Term ("Don't make us guess.."): "burgers"

Where: "Pilsen"
Search Term: "bar"
Sort by: Yelp Rating
What kind: Drink

# Code Attribution

Due to the design of the project, all areas of code were worked on by all members. See lists of "Authors" in respective Python code files for all contributors. Primary authorship is enumerated below. We use the following authorship scheme:

"DIRECT COPY"  ~ Generated by installed package (Django or other) and few edits made
               

"MODIFIED"     ~ Generated by installed package (Django or other) and meaningful edits made   OR   heavily utilized template(s) provided by tutorial sessions (TA- or Django-generated)                                     

"ORIGINAL"     ~ Original code or heavily modified given structure 

Here are primary authors for most significant code (see within files for secondary authors):

index.html: Tyler Amos

map.html: Tyler Amos

matching.py: Kevin Sun

models.py: Kevin Sun, Tyler Amos, Alexander Tyan

views.py: Tyler Amos, Alexander Tyan

popup.py: Tyler Amos

api_pulls.py: Alexander Tyan

file_list.py: Alexander Tyan

geocoding.py: Tyler Amos, Alexander Tyan

forms.py: Kevin Sun, Tyler Amos, Alexander Tyan

requirements.txt: Alexander Tyan

update_db.py: Alexander Tyan

# References

* Python documentation (python.org)
* W3Schools (w3schools.com)
* Leaflet (leafletjs.com)
* For each package or API used, our code draws from examples and tutorials provided in the documentation.
* When external resources, e.g., StackOverflow were consulted, they are cited in the code. 

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
 
# Python Modules and Tools Used:

 * yelpapi: https://github.com/gfairchild/yelpapi
 
    * This package was updated by the group and submitted as a pull request. See https://github.com/gfairchild/yelpapi/pull/8
 
 * pandas: https://pandas.pydata.org
 
 * requests: http://docs.python-requests.org/en/master/
 
 * dominate: https://github.com/Knio/dominate
 
 * leaflet: http://leafletjs.com

 * django-leaflet: https://django-leaflet.readthedocs.io

 * record_linkage: http://recordlinkage.readthedocs.io

 See requirements.txt for a full list of modules.
 
 # All API keys are provided in the Gitlab repository (tylera). The main APIs used are:

Google Maps: https://developers.google.com/maps/documentation/geocoding/intro

Mapbox (for vector tile layers): https://www.mapbox.com

Chicago Data Portal: https://data.cityofchicago.org

Yelp: https://www.yelp.com/developers
  
