#!/usr/bin/env python3
import os
import pandas as pd
from dateutil import parser
import pytz
import sys

# To load the Django app, as per https://stackoverflow.com/questions/25537905/
# django-1-7-throws-django-core-exceptions-
# appregistrynotready-models-arent-load:
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "nice_things_django_project.settings"
application = get_wsgi_application()

# Used to interact with database tables:
from itinerary.models import Food, Wages

# Find files directories:
nice_things_django_project_dir = os.path.dirname(__file__)
sys.path.insert(0, nice_things_django_project_dir)
from helpers import file_list, geocoding

BLS_WAGES_GEOCODED_DIR = "{}{}".format(nice_things_django_project_dir,
                                       file_list.labor_stats_geocoded)
CDP_FOOD_INPSPECTIONS_DIR = "{}{}".format(nice_things_django_project_dir,
                                         file_list.food_inspections)


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
