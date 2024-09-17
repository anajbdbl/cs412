## quotes/views.py
## Description: logic that handles url requests 

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.

# Lists of quotes and images from Anthony Bourdain
QUOTES = [
    "Your body is not a temple, it's an amusement park. Enjoy the ride.",
    "Travel isn't always pretty. It isn't always comfortable. Sometimes it hurts, it even breaks your heart. But that's okay. The journey changes you.",
    "For me, the cooking life has been a long love affair, with moments both sublime and ridiculous."
]

IMAGES = [
    "bourdain_1.jpg",  
    "bourdain_2.jpg",
    "bourdain_3.jpg"
]

# View for the main page that shows one random quote and image
def quote(request):
    random_index = random.randint(0, len(QUOTES) - 1)
    selected_quote = QUOTES[random_index]
    selected_image = IMAGES[random_index]
    context = {
        'quote': selected_quote,
        'image': selected_image
    }
    return render(request, 'quotes/quote.html', context)

# View to show all quotes and images
def show_all(request):
    context = {
        'quotes': zip(QUOTES, IMAGES)
    }
    return render(request, 'quotes/show_all.html', context)

# View for the about page
def about(request):
    context = {
        'bio': "Anthony Bourdain was a chef, author, and travel documentarian who brought cultures and cuisines from around the world into our homes through his unique perspective.",
        'creator': 'Ana Julia Bortolossi', 
    }
    return render(request, 'quotes/about.html', context)

