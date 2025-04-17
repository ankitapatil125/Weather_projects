# weather_project/urls.py
from django.contrib import admin
from django.urls import path, include  # make sure to import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),  # Include your app's urls
]
