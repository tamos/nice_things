from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


PRICE_CHOICES = (
    ("1", '$'),
    ("2", '$$'),
    ("3", '$$$'),
    ("4", '$$$$'),
)
ATTRIBUTE_CHOICES = (
    ('Gender Neutral Restrooms'))

CATEGORY_CHOICES = (
    ("bars", 'Eat'),
    ("restaurants", 'Drink'))

SORT_CHOICES = (
    ("distance", "How far?"),
    ("review_count", "No. Yelp Reviews"),
    ("rating", "Yelp Rating"),
    ("best_match", "Most Relevant"))


class ItineraryInputsForm(forms.Form):
    loc = forms.CharField(max_length=100,
                                  required=True,
                                 widget=forms.TextInput(
                                      attrs={"class": "w3-input w3-border",
                                             "placeholder": "Where in Chicago?"})
                                  )
    price = forms.MultipleChoiceField(required=False,
                                      widget=forms.CheckboxSelectMultiple(
                                          attrs={"display": "inline-block"}
                                      ),
                                      choices=PRICE_CHOICES)

    term = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={"class": "w3-input w3-border",
                                             "placeholder": "Southern BBQ Karaoke"})
                                  )
    attributes = forms.BooleanField(required=False)
    
    categories = forms.MultipleChoiceField(required=False,
                                      widget=forms.CheckboxSelectMultiple(
                                          attrs={"display": "inline-block"}
                                      ),
                                      choices=CATEGORY_CHOICES)
    sort_by = forms.MultipleChoiceField(required=False,
                                      widget=forms.CheckboxSelectMultiple(
                                          attrs={"display": "inline-block"}
                                      ),
                                      choices=SORT_CHOICES)
    
