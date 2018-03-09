from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import sys
from django.shortcuts import render
from itinerary.forms import ItineraryInputsForm
# To load the Django app, as per https://stackoverflow.com/questions/25537905/
# django-1-7-throws-django-core-exceptions-
# appregistrynotready-models-arent-load:
import os
import json
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

from itinerary.popup import Popup


def index(request):
    """
    This function is the main view. It either takes users' inputs
    or renders a map with the results.
    Inputs:
        - request (request object): the Django request object

    Outputs:
        - redirects users to either the main page (index.html) or a results map (map.html)
    """
    context = {}
    # Process user inputs:
    if request.method == 'GET':
        # Instantiate form we created in forms.py
        form = ItineraryInputsForm(request.GET)

        # Insert defaults into a dictionary
        args = {"location": "Chicago",
                "price": "1,2,3,4",
                "term": "Chicago",
                "categories": "bar",
                "attributes": "",
                "sort": "distance"}

        # Validate the inputs are legal:
        if form.is_valid():
            for i in form.__dict__['fields']:
                args[i] = form.cleaned_data[i]

           # Go get results, render as json and output
            results = matching.final_result(args) 
            if results.shape[0] > 0: 
                output = point_content(results)  # Place the info we want into json
                return render(request, 'map.html', {'output':output})  # Render the map       

            # Return to main page if we get no results
            else:
               form = ItineraryInputsForm() 
    else:
        form = ItineraryInputsForm()  

    # If this is the first time, render the main page
    context["form"] = form
    return render(request, 'index.html', context)


def point_content(results):
    """
    This function takes the DataFrame of matched results and
    places them into a list in the form (latitude, longitude, content)
    which is then used to generate the points on a map.

    Input:
        - results (DataFrame): object where each row is a single business
        
    Output:
        - output (json): a json object which is added to a list
          to be made into a Javascript array in map.html
    """
    output = []
    for i in results.itertuples():  # Insert marker content
        content = Popup(i)
        output.append([content.latitude, content.longitude, content.to_html()])
        
    output = mark_safe(json.dumps(output))  # Make sure Django doesn't block it

    # References for json/marking safe:
    # https://stackoverflow.com/questions/4698220/django-template-convert-
    # a-python-list-into-a-javascript-object
    # https://stackoverflow.com/questions/739942/how-to-pass-an-array-in
    # -django-to-a-template-and-use-it-with-javascript#739974

    return output
