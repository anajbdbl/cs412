## hw/views.py
## Description: logic that handles url requests 

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

# def home(request):
#     ''' A function to respond to the /hw URL. '''

#     # create text
#     response_text = f''' 
#     <html>
#     <h1> Hello, world! </h1>
#     <p>
#     This is our first Django webpage!
#     <p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     '''

#     # return response to client
#     return HttpResponse(response_text)

def home(request):
    ''' A function to respond to the /hw URL. 
        Delegating the work to HTML template'''
    
    # template will present response
    template_name = "hw/home.html"

    # dictionary for context variables
    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65, 90)),
        'letter2': chr(random.randint(65, 90)),
        'number': random.randint(1, 10), 
    }

    # delegate response to template
    return render(request, template_name, context)
