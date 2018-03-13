"""
ORIGINAL (using dominate documentation)

Authors: Tyler Amos
"""

from dominate.tags import b, br
from dominate.document import document
from pandas.core.series import Series


class Popup(object):
    """
    This is a popup which will be displayed on the result map.
    """     
    
    def __init__(self, result):
        """
        This instantiates a Popup object from a single DataFrame row's data.
        That is the 1-index element in a single row from the method
        self.iterrows()
        
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
            - rendered_html (str): a string which contains html code
              that will be passed into a javascript array. See self.to_html()
            - to_label (list of tuples): a list in the form:
                (attribute, prefix)
        """
        result = check_is_Series(result)  # ensure the right type
        
        ### REQUIRED FIELDS ###
        
        straight_no_default = ["name", "addr", "latitude", "longitude"]
        
        for i in straight_no_default:  # loop through row's contents
                self.__dict__[i] = result[i]

        lists_to_be_joined = ["food_status", "food_date", "wages_violations",
                              "divvy_stations",
                              "env_complaints_url",
                              "env_enforce_url"]
        
        ### FIELDS WHICH ARE LISTS ###
        # joined by ", " with none as the default
        
        for i in lists_to_be_joined:
            try:
               self.__dict__[i] = ", ".join(result[i])
            except:
                self.__dict__[i] = None

        leftovers = ["phone", "price", "env_complaints", "env_enforce"]

        ### ITEMS WHICH REQUIRE NO ACTION, JUST ADD THEM TO OUTPUT ####
        # items which require no action, just add to the output
        
        for i in leftovers:
            try:
                self.__dict__[i] = result[i]
            except:
                self.__dict__[i] = None
              
        self.rendered_html = document()
        
        # This is a list of attributes and their specified prefix
        # this is what is written in to the popup
        
        self.to_label = [(self.phone, ""), (self.price, ""),
                         (self.food_status, "Food Inspections: "),
                         (self.food_date, "Food Inspection Dates: "),
                         (self.wages_violations, "Recorded Bureau of Labor Violations: "),
                         (self.divvy_stations, "Nearby Divvy Stations: "),
                         (self.env_complaints, "Environmental Complaints: "),
                         (self.env_complaints_url, "Environmental Complaints Links: "),
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
            print("PREFIX:", prefix, "ATTRIBUTE:", attr)
            if attr:
                print("PREFIX:", prefix, "ATTRIBUTE:", attr)
                # Loop through and bold prefixes, render attributes as strings
                # and add to the document
                self.rendered_html.add(b(prefix), str(attr), br())

        return str(self.rendered_html)


### Helper function ####


def check_is_Series(result):
    """
    Ensures we get inputs in the right format.

    Input:
        - result (as described in Popup.__init__)

    Output:
        - The result, correctly formatted as the 1-index element
        from the row.

    """
    if type(result) == Series:  # ready for liftoff
        return result
    elif type(result) == tuple:  # correct the issue
        return check_is_Series(result[1])
    else:  # issue is not fixable
        raise TypeError("Received the wrong data type, try iterrows()")

            

