from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('main/', views.main, name='main'), ## the view for the main page
    path('order/', views.order, name='order'), ## the view for the ordering page
    path('confirmation/', views.confirmation, name='confirmation'), ## the view to process the submission of an order, and display a confirmation page
]
