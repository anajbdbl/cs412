from django.contrib import admin

# Register your models here.
from .models import UserProfile, Movie, Review, Friend, Watchlist

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Friend)
admin.site.register(Watchlist)
