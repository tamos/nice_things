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
#os.chdir("/nice_things_django_project")

os.environ['DJANGO_SETTINGS_MODULE'] = "nice_things_django_project.settings"
application = get_wsgi_application()

from itinerary.models import Food, Wages

sys.path.insert(0, './helpers')
from helpers import file_list, geocoding


def update_wages_table(csv_path=file_list.labor_stats, geocode=False):
    """
    Updates the Wages table in the nice_things db.

    :param csv_path: string, csv path file

    :return: Update the Wages table in nice_things database
    """
    use_cols = ["case_id", "trade_nm", "legal_name", "street_addr_1_txt",
                "cty_nm", "st_cd", "zip_cd", "case_violtn_cnt"]
    df = pd.read_csv(filepath_or_buffer=csv_path,
                     dtype={"case_id": int,
                            "trade_nm": str,
                            "legal_name": str,
                            "street_addr_1_txt": str,
                            "cty_nm": str,
                            "st_cd": str,
                            "zip_cd": int,
                            "case_violtn_cnt": int},
                     usecols=use_cols)

    # Clean out nulls to avoid nullable entries into the itinerary_wages table
    # in the nice_things database:
    df = df.dropna()

    # Squirt into the database:
    for index, row in df.iterrows():
        # Prepare row names:
        case_id = row["case_id"]
        trade_nm = row["trade_nm"]
        legal_name = row["legal_name"]
        street_addr_1_txt = row["street_addr_1_txt"]
        cty_nm = row["cty_nm"]
        st_cd = row["st_cd"]
        zip_cd = row["zip_cd"]
        case_violtn_cnt = row["case_violtn_cnt"]

        if geocode:
            google_query = "{}, {}, {}".format(street_addr_1_txt, cty_nm, st_cd)
            address, google_longitude, google_latitude = \
                geocoding.geo_code_single_address(google_query)
        # Empty placeholders if we are not geocoding. Necessary because
        # db does not take nulls:
        else:
            google_longitude = 0.0
            google_latitude = 0.0
        longitude = google_longitude
        latitude = google_latitude

        # Squirt the data into the db:
        obj, created = Wages.objects.get_or_create(
            case_id=case_id,
            trade_nm=trade_nm,
            legal_name=legal_name,
            street_addr_1_txt=street_addr_1_txt,
            cty_nm=cty_nm,
            st_cd=st_cd,
            zip_cd=zip_cd,
            case_violtn_cnt=case_violtn_cnt,
            longitude=longitude,
            latitude=latitude)


def update_food_table(csv_path=file_list.food_inspections):
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
    # Clean out nulls to avoid nullable entries into the itinerary_wages table
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
        zip_ = row["zip"]
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
            zip=zip_,
            inspection_date=inspection_date,
            inspection_type=inspection_type,
            results=results,
            violations=violations,
            longitude=longitude,
            latitude=latitude)
