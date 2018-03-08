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


def index(request):
    """ This function is the main view. It either takes users' inputs
    or renders a map with the results.
    Inputs:
        - request: the Django request object

    Outputs:
        - redirects users to either the main page (index.html) or a map (map.html)
    """
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
                "sort": "distance"}

        # Validate the inputs are legal:
        if form.is_valid():
            args["location"] = form.cleaned_data["loc"]
            args["price"] = form.cleaned_data["price"]
            args["term"] = form.cleaned_data["term"]
            args["categories"] = form.cleaned_data["categories"]
            args["attributes"] = form.cleaned_data["attributes"]
            args["sort"] = form.cleaned_data["sort_by"]
            
            # Go get results, render as json and output
            results = matching.final_result(args) 
            if results.shape[0] > 0: 
                output = point_content(results)  # place the info we want into json
                return render(request, 'map.html', {'output':output}) # render the map       
            # Return to main page if we get no results
            else:
                form = ItineraryInputsForm() 
    else:
        form = ItineraryInputsForm()  
        
    context["form"] = form
    return render(request, 'index.html', context)  # Render main page


from dominate.tags import html, head, body, b, a
from dominate.util import raw
from dominate.document import document


def point_content(results):
    """ This function takes the DataFrame of matched results and
    places them into a list in the form (latitude, longitude, content)
    which is then used to generate the points on a map.

    Inputs:
        - results (DataFrame): object where each row is a single business
    Outputs:
        - output (json): a json object which is passed to render in
        a dictionary to be made into a Javascript array in map.html
    """
    output = []
    for i in results.itertuples():
        # This is where we insert the marker content
        content = popup(i)
        output.append([content.latitude, content.longitude, content.to_html()])
        print(content.to_html())
        
    output = mark_safe(json.dumps(output))  # make sure Django doesn't block it

    # References for json/marking safe:
    # https://stackoverflow.com/questions/4698220/django-template-convert-a-python-list-into-a-javascript-object
    # https://stackoverflow.com/questions/739942/how-to-pass-an-array-in-django-to-a-template-and-use-it-with-javascript#739974
    return output


import dominate
from dominate.tags import html, head, body, b, br
from dominate.document import document 


class popup(object):
    """
    This is a class which holds generates popup content in html
    should be in another file, but is giving me errors
    """
    def __init__(self, result):
        self.name = result.name
        self.addr = result.addr
        self.latitude = result.latitude
        self.longitude = result.longitude
        try:
            self.phone = result.phone
        except:
            self.phone = None
        try:
            self.price = result.price
        except:
            self.price = None
        try:
            self.food_status = ", ".join(result.food_status)
        except:
            self.food_status = None
        try:
            self.food_date = ", ".join(result.food_date)
        except:
            self.food_date = None
        try:
            self.wages_violations = ", ".join(result.wages_violations)
        except:
            self.wages_violations = None
        try:
            self.divvy_stations = ", ".join(result.divvy_stations)
        except:
            self.divvy_stations = None
        try:
            self.env_complaints = ", ".join(result.env_complaints)
        except:
            self.env_complaints = None
        try:
            # complaint_urls = []
            # for link in result.env_complaints_url:
            #     complaint_urls.append(a(link, href=link))
            #self.env_complaints_url = ", ".join(complaint_urls)

            self.env_complaints_url = ", ".join(result.env_complaints_url)

        except:
            self.env_complaints_url = None
        try:
            self.env_enforce = ", ".join(result.env_enforce)
        except:
            self.env_enforce = None
        try:
            self.env_enforce_url = ", ".join(result.env_enforce_url)
        except:
            self.env_enforce_url = None
        
        self.rendered_html = document()
        self.to_label = [(self.phone, ""), (self.price, ""),
                         (self.food_status, b("Food Inspections: ")),
                         (self.food_date, b("Inspection Date: ")),
                         (self.wages_violations, b("Recorded Bureau of Labor Violations: ")),
                         (self.divvy_stations, b("Nearby Divvy Stations: ")),
                         (self.env_complaints, b("Environmental Complaints: ")),
                         (self.env_complaints_url, b("Complaints Links: ")),
                         (self.env_enforce, b("Environmental Penalties Levied: ")),
                         (self.env_enforce_url, b("Environmental Penalties Links: "))]

# iterating from: https://stackoverflow.com/questions/25150955/python-iterating-through-object-attributes
    def to_html(self):
        """
        Renders to a STRING representation of html
        """
        self.rendered_html.add(b(self.name))  # bold the name
        self.rendered_html.add(br(), self.addr, br())  # next the address, br is line break
        for attr, prefix in self.to_label:  # catch nones?
            if attr:
                self.rendered_html.add(prefix, str(attr), br())  # loop through attributes and add
        return str(self.rendered_html)
            

        


