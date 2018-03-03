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
        results = find_results(args["aka_name"])
        if results.exists():
            context["result"] = [i.aka_name for i in results]
            print(context)
            return HttpResponseRedirect('results')
        
    return render(request, 'index.html', context)

def result_map(request):# results):
    response = "You're looking at the results of question "
    return render(request, 'map.html')


def find_results(aka_name):
    """
    Dumb testing function
    :return:
    """
    #rest_name_str = args["restaurant_name"]
    query_result = Food.objects.filter(aka_name=aka_name)
    return query_result
