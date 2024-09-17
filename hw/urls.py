## hw/urls.py

## description: the app-specifics URLS for the hw application

from django.urls import path 
from django.conf import settings
from . import views

## create a list of urls for this app:
urlpatterns = [
    path(r'', views.home, name="home"), ## first url
]