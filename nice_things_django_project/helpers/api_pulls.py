"""
ORIGINAL (with assistance from Python and requests documentation and
https://dev.socrata.com/docs/app-tokens.html for Socrata API)

Authors: Alexander Tyan

Description: functions for CDP API pulls. Note that CDP's environmental data
is only available in a lookup format (e.g. table where one can find a
violation then one must follow the url to go to another CDP table). So this
environmental CSV ("cdp_environment.csv" in the "data" folder) was a direct
download from the CDP, without using the API.
"""
import requests
import sys
import os

# Find files directories (from PA3):
nice_things_django_project_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, nice_things_django_project_dir)
from helpers import api_keys

LEGAL_DICT_INPUTS = {"inspection_id", "dba_name", "aka_name", "license_",
                     "facility_type", "risk", "address", "city", "state",
                     "zip", "inspection_date", "inspection_type", "results",
                     "violations", "latitude", "longitude", "location",
                     "location_city", "location_address", "location_zip",
                     "location_state"}


def pull_cdp_health_api(output_csv, where_date=None, input_dict={}, limit=None,
                        legal_dict_inputs=LEGAL_DICT_INPUTS):
    """
    Connects to the Chicago Data Portal and downloads the Food Inspections
    data set according to user preferences specified in the function
    parameters

    Inputs:
        - where_date: tuple of dates ("yyyy-mm-dd", "yyyy-mm-dd"), start and end
        - output_csv: string, write out a csv file with this string as a name.
                       WILL OVERWRITE EXISTING FILE IF NAME MATCHES!

        - input_dict: dictionary of params for what fields from the dataset
        to include and how to filter them. Dict keys are strings. For full field
        interpretation see "cdp_food_inspections_description.pdf" in the
        "data" folder
        Options for keys:
            inspection_id: number
            dba_name: text, all capital letters
            aka_name: text, all capital letters
            license_: number
            facility_type: text
            risk: text
            address: text, all capital letters
            city: text, all capital letters
            state: text
            zip: number
            inspection_date: floating_timestamp
            inspection_type: text
            results: text
            violations: text
            latitude: number
            longitude: number
            location: point
            location_city: text
            location_address: text
            location_zip: text
            location_state: text
        - limit: integer, limit how many most recent rows. API returns 1000 by
                  default.
        - legal_dict_inputs: possible keys for the input_dict

    Outputs:
        - no return, writes out the csv
    """
    # Check input_dict is a dictionary:
    if not isinstance(input_dict, dict):
        raise AssertionError("Not a dictionary in input_dict input!")

    # Check output_csv is a string:
    if output_csv and not isinstance(output_csv, str):
        raise AssertionError("Not a string in output_csv input!")

    # Concatenate URL:
    source_url = "https://data.cityofchicago.org/resource/cwig-ma7x.csv"
    # Make sure to get the latest inspection rows by date:
    concatenate_url = source_url + "?$order=inspection_date DESC"
    if limit:  # If want to limit how many rows
        concatenate_url += "&$limit=" + str(limit)

    # Apply non-null filter to numeric fields, to avoid pandas
    # dealing with null numeric types:
    non_null_filter = "&$where=inspection_id IS NOT NULL AND " \
                      "dba_name IS NOT NULL AND " \
                      "aka_name IS NOT NULL AND " \
                      "license_ IS NOT NULL AND " \
                      "facility_type IS NOT NULL AND " \
                      "risk IS NOT NULL AND " \
                      "address IS NOT NULL AND " \
                      "city IS NOT NULL AND " \
                      "state IS NOT NULL AND " \
                      "zip IS NOT NULL AND " \
                      "inspection_date IS NOT NULL AND " \
                      "inspection_type IS NOT NULL AND " \
                      "results IS NOT NULL AND " \
                      "violations IS NOT NULL AND " \
                      "longitude IS NOT NULL AND " \
                      "latitude IS NOT NULL"
    concatenate_url += non_null_filter

    # Apply date filter:
    if where_date:
        start, end = where_date
        date = " AND inspection_date between '{}T00:00:00' and '{}T00:00:00'".format(start, end)
        concatenate_url += date

    # Other filters as specifed by the input_dict in the function inputs:
    for key, value in input_dict.items():
        # Foolproof key inputs:
        if key not in legal_dict_inputs:
            raise AssertionError("Not a valid key provided in the input dictionary!")
        api_string_to_add = "&{}={}".format(key, value)
        concatenate_url += api_string_to_add

    # Get into API (with app tokens, there's no throttling limit):
    app_token = api_keys.CDP_APP_TOKEN
    socrata_headers = {'X-App-Token': app_token}
    r = requests.get(url=concatenate_url, headers=socrata_headers)

    # Process the data and write out:
    csv_data = r.text
    csv_file = open(output_csv, "w")
    csv_file.write(csv_data)
    csv_file.close()
