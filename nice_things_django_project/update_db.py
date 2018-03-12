#!/usr/bin/env python3
import os
import pandas as pd
from dateutil import parser
import pytz
import sys
from django.db import transaction
from django.apps import apps
from django.utils import timezone

# To load the Django app, as per (https://stackoverflow.com/questions/25537905/
# django-1-7-throws-django-core-exceptions-
# appregistrynotready-models-arent-load):
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "nice_things_django_project.settings"
application = get_wsgi_application()

# Used to interact with database tables:
from itinerary.models import Food, Wages, Divvy, Env_Complaints

# Find files directories:
nice_things_django_project_dir = os.path.dirname(__file__)
sys.path.insert(0, nice_things_django_project_dir)
from helpers import file_list, geocoding

BLS_WAGES_GEOCODED_CSV = "{}{}".format(nice_things_django_project_dir,
                                       file_list.labor_stats_geocoded)
CDP_FOOD_INPSPECTIONS_CSV = "{}{}".format(nice_things_django_project_dir,
                                         file_list.food_j2017_m2018)
DIVVY_CSV = "{}{}".format(nice_things_django_project_dir,
                                         file_list.divvy_stats)
ENVIRO_CSV = "{}{}".format(nice_things_django_project_dir,
                                         file_list.enviro_stats)


def split_y_and_url(df_column):
    """
    Helper to preprocess_enviro_df. Splits a column in form Y (url)

    Inputs:
        - df_column: df series, representing a column like "Y <url>"
        - comp_or_enf: string, "complaints" or "enforcement", for renaming
        the split columns

    Outputs:
        - split_df: Pandas dataframe, (<bool of complaint or enforcement>,
        <url string of complaint or enforcement>)
    """
    # Split "Y" from the URL and convert "Y" to True's
    split_df = df_column.str.extract(r'(^Y) \((.*)\)', expand=True)
    split_df.replace('Y', True, inplace=True)  # make boolean

    # Rename columns:
    if df_column.name == 'COMPLAINTS':
        split_df.columns = ["complaints", "complaints_url"]
    else:
        split_df.columns = ["enviro_enforcement", "enviro_enforcement_url"]

    return split_df


def extract_coordinates(map_location_series):
    """
    Helper to preprocess_enviro_df. Produces a dataframe of latitudes and
    longitudes.

    Inputs:
        - map_location_series: pandas series, contains strings, each
        containing (<latitude>, <longitude>) parts of the string
    Outputs:
        - lat_lon_extracted_df: pandas df, columns of latitudes and longitudes
    """
    # Extract ("lat", "long") part of the string and split into lat and long:
    lat_lon_extracted_df = map_location_series.str.extract(r'\((.*),(.*)\)')

    # Convert to float:
    lat_lon_extracted_df = lat_lon_extracted_df.astype(float)

    # Rename columns:
    lat_lon_extracted_df.columns = ["latitude", "longitude"]

    return lat_lon_extracted_df


def preprocess_enviro_df(enviro_df):
    """
    Takes the raw pandas df of the cdp environment dataset and prepares it for
    updating the nice_things db.

    Inputs:
        - enviro_df: pandas dfof the original cdp environment file
        - output_csv_path: string, directory path for the processed csv file

    Outputs:
        - returns a processed csv file into a specified directory path
    """
    complaints_split_df = split_y_and_url(enviro_df['COMPLAINTS'])
    enforcement_split_df = split_y_and_url(enviro_df['ENFORCEMENT'])
    coord_df = extract_coordinates(enviro_df['MAP LOCATION'])
    cols_to_concat = ['STREET NUMBER FROM', 'DIRECTION', 'STREET NAME', 'STREET TYPE']
    # https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-
    # in-dataframe-in-pandas-python:
    full_address_ser = enviro_df[cols_to_concat].apply(lambda x: " ".join(x),
                                                       axis=1)

    # Concatenate all together:
    df = pd.concat([complaints_split_df, enforcement_split_df,
                    full_address_ser.rename("address"), coord_df], axis=1)

    # Make sure that the lengths of the dataframes/series are preserved:
    assert len(complaints_split_df) == len(enforcement_split_df) \
        == len(coord_df) == len(full_address_ser)

    return df


# Squirt the data into the db, using atomic transactions, rolls back all
# db changes if at least one transaction was unsuccessful:
# (https://docs.djangoproject.com/en/2.0/topics/db/transactions/#
# django.db.transaction.atomic):
@transaction.atomic
def update_db_table(csv_path, db_table_to_update):
    """
    Updates a in the nice_things db.

    Inputs:
        - csv_path: string, csv path file to the data with which to update db
        - db_table_to_update: string, which table in nice_things db to update;
        options: "Food", "Wages", "Env_Complaints", "Divvy"

    Outputs:
        - no return, update the db_table_to_update table in nice_things db
    """
    # Determine the model
    # (https://stackoverflow.com/questions/411810/how-do-i-retrieve-a-django-
    # model-class-dynamically/28380435):
    model = apps.get_model('itinerary', db_table_to_update)

    # To shrink amount of data to handle, define only the columns we'd need;
    # plus, determine data types as keys' values to enforce data in read_csv:
    if db_table_to_update == "Wages":
        keep_cols = {"case_id": int, "trade_nm": str, "legal_name": str,
                     "street_addr_1_txt": str, "cty_nm": str, "st_cd": str,
                     "zip_cd": int, "case_violtn_cnt": int, "latitude": float,
                     "longitude": float}
    elif db_table_to_update == "Food":
        keep_cols = {"inspection_id": int, "dba_name": str, "aka_name": str,
                     "license_": int, "facility_type": str, "risk": str,
                     "address": str, "city": str, "state": str, "zip": int,
                     "inspection_date": str, "inspection_type": str,
                     "results": str, "violations": str, "longitude": float,
                     "latitude": float}
    elif db_table_to_update == "Divvy":
        keep_cols = {"id": int, "name": str, "city": str, "latitude": float,
                     "longitude": float, "dpcapacity": int}
    else:
        keep_cols = {'MAP LOCATION': str, 'STREET NUMBER FROM': str,
                     'DIRECTION': str, 'STREET NAME': str, 'STREET TYPE': str,
                     'COMPLAINTS': str, 'ENFORCEMENT': str}

    # For ease of data and fields handling, let's use pandas:
    df = pd.read_csv(filepath_or_buffer=csv_path,
                     dtype=keep_cols,
                     usecols=keep_cols)

    # Clean out nulls to avoid nullable entries into the table in the
    # nice_things database:
    df = df.dropna()

    # Drop duplicates (CDP mentions there may be duplicates in their data);
    # Also, Django's get_or_create() should also prevent duplicate
    # at the time of database injection:
    df = df.drop_duplicates()

    # Some general data pre-processing; column renaming, time formatting:
    if db_table_to_update == "Food":
        # To conform date-time formats:
        df["inspection_date"] = df["inspection_date"].apply(func=parser.parse)
        df["inspection_date"] = df["inspection_date"].apply(
            func=timezone.make_aware, args=(pytz.UTC, ))
        df.rename(columns={"license_": "license_num",
                           "zip": "zip_code"}, inplace=True)

    elif db_table_to_update == "Wages":
        df.rename(columns={"zip_cd": "zip_code"}, inplace=True)

    elif db_table_to_update == "Divvy":
        df.rename(columns={"dpcapacity": "capacity"}, inplace=True)
        df.rename(columns={"id": "station_id"}, inplace=True)
    # For enviro data, split the complaints/enforcement fields into bool and
    # url, concatenate address into a string, and add latitude and
    # longitude columns:
    elif db_table_to_update == "Env_Complaints":
        df = preprocess_enviro_df(df)

    # Doing PostgreSQL injection row by row (slow) because bulk inject doesn't
    # work for our environmental table because it has automatically generated
    # primary keys:
    for index, row in df.iterrows():
        # Prepare row for a **kwargs input
        # (https://docs.djangoproject.com/en/2.0/ref/models/querysets/#get-or-create):
        row_to_dict = row.to_dict()
        # Squirt the data into the db:
        model.objects.get_or_create(**row_to_dict)


def update_database(wages_csv=BLS_WAGES_GEOCODED_CSV,
                    food_csv=CDP_FOOD_INPSPECTIONS_CSV,
                    divvy_csv=DIVVY_CSV,
                    enviro_csv=ENVIRO_CSV):
    """
    Updates all database tables

    Inputs:
        - wages_csv: str, BLS Labour Violations csv path
        - food_csv: str, CDP Food Inspections csv path
        - divvy_csv: str, Chicago Divvy stations csv path
        - enviro_csv: str, CDP Enviroment violations csv path

    Outputs:
        - no return, updates all database tables
    """
    update_db_table(csv_path=wages_csv, db_table_to_update="Wages")
    update_db_table(csv_path=food_csv, db_table_to_update="Food")
    update_db_table(csv_path=divvy_csv, db_table_to_update="Divvy")
    update_db_table(csv_path=enviro_csv, db_table_to_update="Env_Complaints")





