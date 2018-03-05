from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import sys
from django.shortcuts import render
from itinerary.forms import ItineraryInputsForm
# To load the Django app, as per https://stackoverflow.com/questions/25537905/
# django-1-7-throws-django-core-exceptions-
# appregistrynotready-models-arent-load:
import os

nice_things_project_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, nice_things_project_dir)
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = "nice_things_django_project.settings"
application = get_wsgi_application()
# https://stackoverflow.com/questions/40206569/
# django-model-doesnt-declare-an-explicit-app-label:
from itinerary.models import Food, Wages
from django.utils.html import format_html, mark_safe
os.chdir('helpers')
import helpers.matching as matching   # has to be a better way to do this
os.chdir( '../')

from django.core import serializers

def index(request):
    context = {}
    # Process user inputs:
    if request.method == 'GET':
        # Instantiate form we created in forms.py
        form = ItineraryInputsForm(request.GET)

        # Convert form input into dictionary for search.py:
        # Place defaults
        args = {"location": "Chicago",
                "price": "1,2,3,4",
                "term": "Chicago",
                "categories": "bar",
                "attributes": "",
                "sort": "distance" }

        # Validate the inputs are legal:
        if form.is_valid():
            args["location"] = form.cleaned_data["loc"]
            args["price"] = form.cleaned_data["price"]
            args["term"] = form.cleaned_data["term"]
            args["categories"] = form.cleaned_data["categories"]
            args["attributes"] = form.cleaned_data["attributes"]
            args["sort"] = form.cleaned_data["sort_by"]
            # Go get results
            results = matching.final_result(args)  # search criterion
            # consider accounting for no results corner case
            output = point_content(results)# place the info we want into a dict
            return render(request, 'map.html', {'output':output}) # render the map       
            
    else:
        form = ItineraryInputsForm()
        
    context["form"] = form
    return render(request, 'index.html', context)

import json

def point_content(results):
    """ This function takes a queryset result and places it into a dictionary
    for use in the map page.
    """
    output = []
    for i in results.itertuples():
        output.append([i.latitude, i.longitude, i.name])
    output = mark_safe(json.dumps(output))
    # References for json/marking safe:
    # https://stackoverflow.com/questions/4698220/django-template-convert-a-python-list-into-a-javascript-object
    # https://stackoverflow.com/questions/739942/how-to-pass-an-array-in-django-to-a-template-and-use-it-with-javascript#739974
    return output
 


