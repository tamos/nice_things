from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


PRICE_CHOICES = (
    ("1", '$'),
    ("2", '$$'),
    ("3", '$$$'),
)
ATTRIBUTE_CHOICES = (
    ('Gender Neutral Restrooms'))

CATEGORY_CHOICES = (
    ("bars", 'Eat'),
    ("restaurants", 'Drink'))


class ItineraryInputsForm(forms.Form):
    destination = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={"class": "w3-input w3-border",
                                             "placeholder": "BoBo-ville, Chicago"})
                                  )
    price = forms.MultipleChoiceField(required=False,
                                      widget=forms.CheckboxSelectMultiple(
                                          attrs={"display": "inline-block"}
                                      ),
                                      choices=PRICE_CHOICES)

    aka_name = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={"class": "w3-input w3-border",
                                             "placeholder": "nickname"})
                                  )
    term = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={"class": "w3-input w3-border",
                                             "placeholder": "Southern BBQ Kareoke"})
                                  )
    attributes = forms.BooleanField(required=False)
    
    categories = forms.MultipleChoiceField(required=False,
                                      widget=forms.CheckboxSelectMultiple(
                                          attrs={"display": "inline-block"}
                                      ),
                                      choices=CATEGORY_CHOICES)    
    
