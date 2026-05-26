from django.shortcuts import render
from .forms import TripForm
from .models import Trip
from django.db import IntegrityError



def trip_form(request):

    error_message = None

    if request.method == 'POST':

        form = TripForm(request.POST, request.FILES)

        if form.is_valid():

            trip = form.save(commit=False)

            raw_trip_id = trip.trip_id.replace('TRP-', '').strip()

            trip.trip_id = f"TRP-{raw_trip_id}"

            try:

                trip.save()

                return render(
                    request,
                    'success.html',
                    {
                        'trip_id': trip.trip_id
                    }
                )

            except IntegrityError:

                error_message = (
                    "Trip ID already exists. "
                    "Please contact operations."
                )

    else:

        form = TripForm()

    return render(
        request,
        'index.html',
        {
            'form': form,
            'error_message': error_message
        }
    )