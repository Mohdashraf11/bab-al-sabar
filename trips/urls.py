from django.urls import path
from .views import trip_form, export_excel

urlpatterns = [
    path('', trip_form, name='trip_form'),
    path('export/excel/', export_excel, name='export_excel'),
]