## quotes/urls.py

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.quote, name='quote'),  # Main page and /quote
    path('quote/', views.quote, name='quote'),  # Same as main
    path('show_all/', views.show_all, name='show_all'),  # Show all quotes
    path('about/', views.about, name='about'),  # About page
]
