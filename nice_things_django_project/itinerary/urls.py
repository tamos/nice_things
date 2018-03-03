from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('results', views.result_map, name='result_map'),
]

