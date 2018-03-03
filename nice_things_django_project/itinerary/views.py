from django.http import HttpResponse
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
from helpers import matching


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

    else:
        form = ItineraryInputsForm()

    # Respond to user inputs:
    df = matching.extract_yelp_data(term="La fuente restaurant",
                                    limit=20, sort_by="distance")
    print(df)
    '''if "restaurant_name" in args:
        results = find_results(args)
        if results.exists():
            print("EXISTS!")
            context["result"] = results'''

    context["form"] = form

    return render(request, 'index.html', context)


def find_results(args):
    """
    Dumb testing function
    :return:
    """
    rest_name_str = args["restaurant_name"]
    return Food.objects.filter(aka_name=rest_name_str)




