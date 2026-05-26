from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'truck_number',
            'trip_id',
            'container_photo',
            'second_container_photo',
            'er_file'
        ]