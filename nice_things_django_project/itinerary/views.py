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


def index(request):
    context = {}
    # Process user inputs:
    if request.method == 'GET':
        # Instantiate form we created in forms.py
        form = ItineraryInputsForm(request.GET)

        # Convert form input into dictionary for search.py:
        args = {}

        # Validate the inputs are legal:
        if form.is_valid():
            args["destination"] = form.cleaned_data["destination"]
            args["price"] = form.cleaned_data["price"]
            args["aka_name"] = form.cleaned_data["aka_name"]

    else:
        form = ItineraryInputsForm()
        
    context["form"] = form
        
    # Respond to user inputs:
    if "aka_name" in args.keys():
        results = find_results(args["aka_name"])   # search criterion
        if results.exists():
            output = point_content(results)  # place the info we want into a dict
            return render(request, 'map.html', output) # render the map
        
    return render(request, 'index.html', context)

def point_content(results):
    # fornow
    business = results[0]
    output = {}
    output['content'] = format_html("<b>{}</b> <br> Food Inspection Result: {} {}",
                    mark_safe(business.aka_name),
                    business.results,
                    business.violations)
    output['lat'] = business.latitude
    output['lon'] = business.longitude
    return output
    


def find_results(aka_name):
    """
    Dumb testing function
    :return:
    """
    #rest_name_str = args["restaurant_name"]
    query_result = Food.objects.filter(aka_name=aka_name)
    return query_result

'''
#NOT NECESSARY BUT KEEP JUST IN CASE
from geojson import dumps
from geojson import Feature, Point, FeatureCollection
from django.utils.html import format_html, mark_safe
from django.urls import reverse

def result_map(request, results):
    output = {}
    #print(results)
    output['lat'] = 41.8765
    output['lon'] = -87.6244
    output['content'] = format_html("<b>{}</b> {} {}",
                    mark_safe('atl'),
                    "MOTE",
                    "HDH")
    return render(request, 'map.html', output)
'''




