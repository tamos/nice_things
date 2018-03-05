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
import helpers.matching as matching  
os.chdir( '../')

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
            output = point_content(results)  # place the info we want into a dict
            return render(request, 'map.html', output) # render the map       
            
    else:
        form = ItineraryInputsForm()
        
    context["form"] = form
    return render(request, 'index.html', context)



def point_content(results):
    """ This function takes a queryset result and places it into a dictionary
    for use in the map page.
    """
    # For now we will hard code this as separate keys until we figure out
    # how to unpack them in javascript. Ugly, but it works.
    num_results = results.shape[0]
    output = {}
    if num_results >= 1:
        output['content0'] = format_html("<b>{}</b> <br> {} <br> #: {} <br> {}",
                        mark_safe(results.iloc[0]['name']),
                        results.iloc[0]["addr"],
                        results.iloc[0]["phone"],
                        results.iloc[0]["price"])
        output['lat0'] = results.iloc[0]["latitude"]
        output['lon0'] = results.iloc[0]["longitude"]
    
    if num_results >= 2:
        output['content1'] = format_html("<b>{}</b> <br> {} <br> #: {} <br> {}",
                        mark_safe(results.iloc[1]['name']),
                        results.iloc[1]["addr"],
                        results.iloc[1]["phone"],
                        results.iloc[1]["price"])
        output['lat1'] = results.iloc[1]["latitude"]
        output['lon1'] = results.iloc[1]["longitude"]
        '''
        # We need to figure out a way to account for few results
        # the javascript breaks if we are missing a key
    if num_results >= 3:
        output['content2'] = format_html("<b>{}</b> <br> Food Inspection Result: {} {}",
                        mark_safe(results[2].aka_name),
                        results[2].results,
                        "more datassss")
        output['lat2'] = results[2].latitude
        output['lon2'] = results[2].longitude
    if num_results >= 4:
        output['content3'] = format_html("<b>{}</b> <br> Food Inspection Result: {} {}",
                        mark_safe(results[3].aka_name),
                        results[3].results,
                        "more datassss")
        output['lat3'] = results[3].latitude
        output['lon3'] = results[3].longitude
    if num_results >= 5:
        output['content4'] = format_html("<b>{}</b> <br> Food Inspection Result: {} {}",
                        mark_safe(results[4].aka_name),
                        results[4].results,
                        "more datassss")
        output['lat4'] = results[4].latitude
        output['lon4'] = results[4].longitude'''
    return output
    


def find_results(aka_name):
    """
    Dumb testing function
    :return:
    """
    #rest_name_str = args["restaurant_name"]
    query_result = Food.objects.filter(aka_name=aka_name)
    return query_result


