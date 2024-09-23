## quotes/views.py
## Description: logic that handles url requests 

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.

# Lists of quotes and images
QUOTES = [
    "Your body is not a temple, it's an amusement park. Enjoy the ride.",
    "Travel isn't always pretty. It isn't always comfortable. Sometimes it hurts, it even breaks your heart. But that's okay. The journey changes you.",
    "For me, the cooking life has been a long love affair, with moments both sublime and ridiculous.",
    "I'm a big believer in winging it. I'm a big believer that you're never going to find a perfect city travel experience or the perfect meal without a constant willingness to experience a bad one. Letting the happy accident happen is what a lot of vacation itineraries miss, I think, and I'm always trying to push people to allow those things to happen rather than stick to some rigid itinerary.",
    "Without experimentation, a willingness to ask questions and try new things, we shall surely become static, repetitive, and moribund.",
    "If I'm an advocate for anything, it's to move. As far as you can, as much as you can. Across the ocean, or simply across the river. Walk in someone else's shoes or at least eat their food. It's a plus for everybody."
]

IMAGES = [
    "bourdain_1.jpg",  
    "bourdain_2.jpg",
    "bourdain_3.jpg",
    "bourdain_4.jpg",
    "bourdain_5.jpg",
    "bourdain_6.jpg"
]


def quote(request):
    ''' View for the main page that shows one random quote and image '''
    random_index = random.randint(0, len(QUOTES) - 1)
    selected_quote = QUOTES[random_index]
    selected_image = IMAGES[random_index]
    context = {
        'quote': selected_quote,
        'image': selected_image
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    ''' View to show all quotes and images '''
    context = {
        'quotes': zip(QUOTES, IMAGES)
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    ''' View for the about page '''
    context = {
        'bio': "Anthony Bourdain was a chef, author, and travel documentarian who brought cultures and cuisines from around the world into our homes through his unique perspective.",
        'creator': 'Ana Julia Bortolossi', 
    }
    return render(request, 'quotes/about.html', context)

