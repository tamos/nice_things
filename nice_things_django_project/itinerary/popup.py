# This is the Popup class

import dominate
from dominate.tags import html, head, body, b, br
from dominate.document import document

class Popup(object):
    """
    This is a popup which will be displayed on the result map.
    """
    
    def __init__(self, result):
        """
        This instantiates a Popup object.
        
        Attributes:
            - name (str): the name of the business
            - phone (str): phone number
            - price (str): a Yelp-style price rating $, $$...
            - food_status (str): a comma-delimited string with one of:
                - 'pass': successful food inspection pass
                - 'pass w/ conditions': conditional pass
                - 'fail': failure
            - food_date (str): a comma-delimited string with inspection dates
            - wages_violations (str): a comma-delimited string with the number
              labour violations incurred by the establishment (from BLS data)
            - divvy_stations (str): a comma-delimited string with nearby divvy
               bicycle stations.
            - env_complaints (str): the number of environmental complaints
               registered against this business
            - env_complaints_url (str): the url of the csv file which details
              environmental complaints
            - env_enforce (str): the number of environmental enforcements
              levied against this business
            - env_enforce_url (str): the url of the csv file which details
               environmental enforcements
            - rendered_html (str): a string of which contains html code
              that will be passed into a javascript array. See self.to_html()
              
            - to_label (list of tuples): a list in the form:
                (attribute, <prefix>)
        """
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
        
        # This is a list of attributes and their specified prefix
        self.to_label = [(self.phone, ""), (self.price, ""),
                         (self.food_status, "Food Inspections: "),
                         (self.food_date, "Inspection Date: "),
                         (self.wages_violations, "Recorded Bureau of Labor Violations: "),
                         (self.divvy_stations, "Nearby Divvy Stations: "),
                         (self.env_complaints, "Environmental Complaints: "),
                         (self.env_complaints_url, "Complaints Links: "),
                         (self.env_enforce, "Environmental Penalties Levied: "),
                         (self.env_enforce_url, "Environmental Penalties Links: ")]

    def to_html(self):
        """
        This method renders html to a string which is then passed as the
        popup label.

        Inputs:
            - the popup object

        Outputs:
            - rendered_html (str): html, cast to a string, for the popup label
        """
        self.rendered_html.add(b(self.name))  # Bold the name
        # Next the address, br() is line break
        self.rendered_html.add(br(), self.addr, br())
        
        for attr, prefix in self.to_label:
            if attr:
                # Loop through and bold prefixes, render attributes as strings
                # and add to the document
                self.rendered_html.add(b(prefix), str(attr), br())

        return str(self.rendered_html)
            

        

