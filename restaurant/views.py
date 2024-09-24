from django.shortcuts import render
import random
import time
from django.utils.timezone import now
from datetime import timedelta

# Create your views here.

def main(request):
    ''' Returns main page of the restaurant '''
    return render(request, 'restaurant/main.html')

def order(request):
    ''' Produces the order page for the form to work '''
    menu = [
        {'name': 'Tacos', 'price': 10},
        {'name': 'Empanadas', 'price': 8},
        {'name': 'Churros', 'price': 5},
        {'name': 'Arepas', 'price': 9}
    ]
    
    daily_specials = [
        {'name': 'Tamales', 'price': 7},
        {'name': 'Ceviche', 'price': 12},
        {'name': 'Pupusas', 'price': 6},
        {'name': 'Carne Asada', 'price': 15}
    ]
    daily_special = random.choice(daily_specials)

    context = {
        'daily_special': daily_special['name'],
        'menu': menu
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    ''' Produces the order confirmation page '''
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        customer_email = request.POST.get('email')
        customer_phone = request.POST.get('phone')
        special_instructions = request.POST.get('instructions')

        ordered_items = []
        total_price = 0
        
        menu_prices = {
            'Tacos': 10,
            'Empanadas': 8,
            'Churros': 5,
            'Arepas': 9
        }

        daily_special_prices = {
            'Tamales': 7,
            'Ceviche': 12,
            'Pupusas': 6,
            'Carne Asada': 15
        }

        items = request.POST.getlist('items')
        for item in items:
            if item in menu_prices:
                ordered_items.append({'name': item, 'price': menu_prices[item]})
                total_price += menu_prices[item]
            elif item in daily_special_prices:
                ordered_items.append({'name': item, 'price': daily_special_prices[item]})
                total_price += daily_special_prices[item]

        ready_time = now() + timedelta(minutes=random.randint(30, 60))

        context = {
            'name': customer_name,
            'email': customer_email,
            'phone': customer_phone,
            'items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%H:%M'),
            'instructions': special_instructions,
        }
        return render(request, 'restaurant/confirmation.html', context)

    return render(request, 'restaurant/order.html')