#!/usr/bin/env python3
import os
import pandas as pd
from dateutil import parser
import pytz
import sys
import numpy as np

# To load the Django app, as per https://stackoverflow.com/questions/25537905/
# django-1-7-throws-django-core-exceptions-
# appregistrynotready-models-arent-load:
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "nice_things_django_project.settings"
application = get_wsgi_application()

# Used to interact with database tables:
from itinerary.models import Food, Wages, Divvy, Env_Complaints, Env_Enforce 

# Find files directories:
nice_things_django_project_dir = os.path.dirname(__file__)
sys.path.insert(0, nice_things_django_project_dir)
from helpers import file_list, geocoding

BLS_WAGES_GEOCODED_DIR = "{}{}".format(nice_things_django_project_dir,
                                       file_list.labor_stats_geocoded)
CDP_FOOD_INPSPECTIONS_DIR = "{}{}".format(nice_things_django_project_dir,
                                         file_list.food_j2017_m2018)
DIVVY_DIR = "{}{}".format(nice_things_django_project_dir,
                                         file_list.divvy_stats)
ENVIRO_DIR = "{}{}".format(nice_things_django_project_dir,
                                         file_list.enviro_stats)


def update_wages_table(csv_path=BLS_WAGES_GEOCODED_DIR,
                       geocode=None):
    """
    Updates the Wages table in the nice_things db.

    :param csv_path: string, csv path file

    :param geocode: str, "google" or "opendatacage"; default None.

    :return: Update the Wages table in nice_things database
    """
    use_cols = ["case_id", "trade_nm", "legal_name", "street_addr_1_txt",
                "cty_nm", "st_cd", "zip_cd", "case_violtn_cnt", "latitude", "longitude"]
    df = pd.read_csv(filepath_or_buffer=csv_path,
                     dtype={"case_id": int,
                            "trade_nm": str,
                            "legal_name": str,
                            "street_addr_1_txt": str,
                            "cty_nm": str,
                            "st_cd": str,
                            "zip_cd": int,
                            "case_violtn_cnt": int,
                            "latitude": float,
                            "longitude": float},
                     usecols=use_cols)

    # Clean out nulls to avoid nullable entries into the itinerary_wages table
    # in the nice_things database:
    df = df.dropna()

    # Squirt into the database:
    geocode_counter = 1
    for index, row in df.iterrows():
        # Prepare row names:
        case_id = row["case_id"]
        trade_nm = row["trade_nm"]
        legal_name = row["legal_name"]
        street_addr_1_txt = row["street_addr_1_txt"]
        cty_nm = row["cty_nm"]
        st_cd = row["st_cd"]
        zip_code = row["zip_cd"]
        case_violtn_cnt = row["case_violtn_cnt"]
        latitude = row["latitude"]
        longitude = row["longitude"]

        # In case we are geocoding straight from Google or OpenCageData
        # geocoding API:
        if geocode == "google":
            google_query = "{}, {}, {}".format(street_addr_1_txt, cty_nm, st_cd)
            print("ATTEMPTING TO GEOCODE ADDRESS", geocode_counter, ":")
            print(google_query)
            address, longitude, latitude = \
                geocoding.geo_code_single_address(google_query)
            geocode_counter += 1
        elif geocode == "opendatacage":
            print("ATTEMPTING TO GEOCODE ADDRESS", geocode_counter, ":")
            print(street_addr_1_txt, cty_nm, st_cd, zip_cd)
            latitude, longitude = geocoding.geocode_using_opencagedata(
                                                    address=street_addr_1_txt,
                                                    city=cty_nm, state=st_cd,
                                                    zip_code=zip_cd,
                                                    country="United States")
            geocode_counter += 1


        # Squirt the data into the db:
        obj, created = Wages.objects.get_or_create(
            case_id=case_id,
            trade_nm=trade_nm,
            legal_name=legal_name,
            street_addr_1_txt=street_addr_1_txt,
            cty_nm=cty_nm,
            st_cd=st_cd,
            zip_code=zip_code,
            case_violtn_cnt=case_violtn_cnt,
            longitude=longitude,
            latitude=latitude)


def update_food_table(csv_path=CDP_FOOD_INPSPECTIONS_DIR):
    """
    Updates the Food table in the nice_things db.

    :param csv_path: string, csv path file

    :return: Update the Food table in nice_things database
    """
    use_cols = ["inspection_id", "dba_name", "aka_name", "license_",
                "facility_type", "risk", "address", "city", "state",
                "zip", "inspection_date", "inspection_type", "results",
                "violations", "longitude", "latitude"]
    df = pd.read_csv(filepath_or_buffer=csv_path,
                     dtype={"inspection_id": int,
                            "dba_name": str,
                            "aka_name": str,
                            "license_": int,
                            "facility_type": str,
                            "risk": str,
                            "address": str,
                            "city": str,
                            "state": str,
                            "zip": int,
                            "inspection_date": str,
                            "inspection_type": str,
                            "results": str,
                            "violations": str,
                            "longitude": float,
                            "latitude": float},
                     usecols=use_cols)
    # Clean out nulls to avoid nullable entries into the itinerary_food table
    # in the nice_things database:
    df = df.dropna()

    # Squirt into the database:
    for index, row in df.iterrows():
        # Prepare row names:
        inspection_id = row["inspection_id"]
        dba_name = row["dba_name"]
        aka_name = row["aka_name"]
        license_num = row["license_"]
        facility_type = row["facility_type"]
        risk = row["risk"]
        address = row["address"]
        city = row["city"]
        state = row["state"]
        zip_code = row["zip"]
        converted_date = parser.parse(row["inspection_date"])
        converted_date = converted_date.replace(tzinfo=pytz.UTC)
        inspection_date = converted_date
        inspection_type = row["inspection_type"]
        results = row["results"]
        violations = row["violations"]
        longitude = row["longitude"]
        latitude = row["latitude"]


        # Squirt the data into the db:
        obj, created = Food.objects.get_or_create(
            inspection_id=inspection_id,
            dba_name=dba_name,
            aka_name=aka_name,
            license_num=license_num,
            facility_type=facility_type,
            risk=risk,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            inspection_date=inspection_date,
            inspection_type=inspection_type,
            results=results,
            violations=violations,
            longitude=longitude,
            latitude=latitude)


def update_enviro_chicago_tables(csv_path=ENVIRO_DIR):
    """
    Updates the Enviro_Chicago table in the nice_things db.

    :param csv_path: string, csv path file

    :return: Update the Enviro_Chicago table in nice_things database
    """
    def split_y_and_url(df_column):
        """ 
        Splits a column in form Y (url)
        """
        
        split_df = df_column.str.extract(r'(^Y) \((.*)\)', expand=True).fillna('False')
        split_df.replace('Y', True, inplace=True)  # make boolean
        return split_df[0], split_df[1]

    def concatenate_address(row):
        address_as_list = [str(row[i]) for i in cols_to_concat]
        return " ".join(address_as_list)

    def extract_coordinates(df):
        lat_lon_extracted = df['MAP LOCATION'].str.extract(r'\((.*),(.*)\)')
        cast_coordinate_to_float = lambda x: [i for i in map(float, x)]
        lat = cast_coordinate_to_float(lat_lon_extracted[0])
        lon = cast_coordinate_to_float(lat_lon_extracted[1])
        # Ideally at this point we geocode the missing coordinates
        return lat, lon

    df_dirty = pd.read_csv(filepath_or_buffer = csv_path).fillna('False')
    complaints, complaints_url = split_y_and_url(df_dirty['COMPLAINTS'])
    enviro_enforcement, enviro_enforcement_url = split_y_and_url(df_dirty['ENFORCEMENT'])

    cols_to_concat = ['STREET NUMBER FROM', 'DIRECTION', 'STREET NAME', 'STREET TYPE']

    address = df_dirty.apply(func=concatenate_address, axis=1)

    latitude, longitude = extract_coordinates(df_dirty)

    attribute_list = [complaints, complaints_url, enviro_enforcement, enviro_enforcement_url,
                          latitude, longitude]
    
    if sum(map(len, attribute_list)) % len(attribute_list) == 0:

        df = pd.DataFrame()
        df['complaints'] = complaints
        df['complaints_url'] = complaints_url
        df['enviro_enforcement'] = enviro_enforcement
        df['enviro_enforcement_url'] = enviro_enforcement_url
        df['latitude'] = latitude
        df['longitude'] = longitude


        df_complaints = df.copy().drop(['enviro_enforcement', 'enviro_enforcement_url'], axis=1)
        df_enviro = df.copy().drop(['complaints', 'complaints_url'], axis=1)

        df_complaints = df_complaints.replace(to_replace='False', value=np.nan).dropna()
        df_enviro = df_enviro.replace(to_replace='False', value=np.nan).dropna()
       
        for index, row in df_complaints.iterrows():
            # Prepare row names:
            longitude_complaints = row["longitude"]
            latitude_complaints = row["latitude"]
            address_complaints = row["city"]
            complaints_complaints = row["dpcapacity"]
            complaints_url = row["latitude"]

        # Squirt the data into the db:
        obj, created = Env_Complaints.objects.get_or_create(
            longitude = longitude_complaints,
            latitude = latitude_complaints,
            address = address_complaints,
            complaints = complaints_complaints,
            complaints_url = complaints_url_complaints)
            
        # Squirt the data into the db:
        obj, created = Env_Enforce.objects.get_or_create(
            longitude = longitude_enforce,
            latitude = latitude_enforce,
            address = address_enforce,
            enviro_enforcement = enviro_enforcement_enforce,
            enviro_enforcement_url = enviro_enforcement_url_enforce)
            

def update_divvy_table(csv_path=DIVVY_DIR):
    use_cols = ["id", "name", "city", "latitude", "longitude", "dpcapacity"]
    df = pd.read_csv(filepath_or_buffer=csv_path,
                     dtype={"id": int,
                            "name": str,
                            "city": str,
                            "latitude": float,
                            "longitude": float,
                            "dpcapacity": int},
                     usecols=use_cols)
 
    df = df.dropna()

    # Squirt into the database:
    for index, row in df.iterrows():
        # Prepare row names:
        _id = row["id"]
        name = row["name"]
        city = row["city"]
        latitude = row["latitude"]
        longitude = row["longitude"]   
        capacity = row["dpcapacity"]

        obj, created = Divvy.objects.get_or_create(
            _id=_id,
            name=name,
            city=city,
            longitude=longitude,
            latitude=latitude,
            capacity=capacity)




