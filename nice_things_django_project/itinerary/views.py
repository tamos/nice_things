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


def point_content2(results):
    # fornow
    business = results[0:2]
    output = {'content': []}
    for i in results:
        pop_content = format_html("<b>{}</b> <br> Food Inspection Result: {} {}",
                    mark_safe(i.aka_name),
                    i.results,
                    'is')
        lat = i.latitude
        lon = i.longitude
        output['content'].append([pop_content, lat, lon])
        print(output)
    return output






def point_content(results):
    # For now we will hard code this as separate keys until we figure out
    # how to unpack them in javascript. Ugly, but it works.
    print(len(results))
    num_results = len(results)
    output = {}
    if num_results >= 1:
        output['content0'] = format_html("<b>{}</b> <br> Food Inspection Result: {} {}",
                        mark_safe(results[0].aka_name),
                        results[0].results,
                        "more data")
        output['lat0'] = results[0].latitude
        output['lon0'] = results[0].longitude
    if num_results >= 2:
        output['content1'] = format_html("<b>{}</b> <br> Food Inspection Result: {} {}",
                        mark_safe(results[1].aka_name),
                        results[1].results,
                        "more datassss")
        output['lat1'] = results[1].latitude
        output['lon1'] = results[1].longitude
    '''if num_results >= 3:
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

    print(len(output))
    print(output.keys())
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


