from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


PRICE_CHOICES = (
    ('$', '$'),
    ('$$', '$$'),
    ('$$$', '$$$'),
)


class ItineraryInputsForm(forms.Form):
    destination = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={"class": "w3-input w3-border",
                                             "placeholder": "Chicago only, yo"})
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
    
