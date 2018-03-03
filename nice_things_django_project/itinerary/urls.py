from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('result_map', views.result_map, name='result_map'),
]

