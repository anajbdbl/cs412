"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include ## new import (include)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hw/", include("hw.urls")), ## new path
    path("quotes/", include("quotes.urls")), ## new path for assignment 3
    path("formdata/", include("formdata.urls")), ## new path for assignment 4 demo
    path("restaurant/", include("restaurant.urls")), ## new path for assignment 4 
    path("blog/", include("blog.urls")), ## new path for assignment 5 demo
    path('mini_fb/', include('mini_fb.urls')),  ## new path for assignment 5, 6, 7, 8, 9
    path('voter_analytics/', include('voter_analytics.urls')),  ## new path for assignment 10
    path('film_log/', include('film_log.urls')),  ## new path for FINAL PROJECT
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
