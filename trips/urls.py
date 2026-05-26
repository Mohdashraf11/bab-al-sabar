from django.urls import path
from . import views
from .views import trip_form

urlpatterns = [
    path('', trip_form, name='trip_form'),
]