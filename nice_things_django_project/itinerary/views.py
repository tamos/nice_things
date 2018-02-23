from django.http import HttpResponse

from django.shortcuts import render
#from django import forms

def index(request):
    #HttpResponse("Hello, world. You're at the Itinerary index.")
    return render(request, 'index.html')
