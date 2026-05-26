from django.shortcuts import render
from .forms import TripForm
from .models import Trip
from django.db import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponse
import openpyxl

from django.contrib.auth.models import User




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


@staff_member_required
def export_excel(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = 'Trips'

    headers = [
        'Trip ID',
        'Truck Number',
        'Status',
        'Container Photo',
        'ER File',
        'Created At',
    ]

    sheet.append(headers)

    trips = Trip.objects.all()

    for trip in trips:

        sheet.append([
            trip.trip_id,
            trip.truck_number,
            trip.status,
            trip.container_photo.url if trip.container_photo else '',
            trip.er_file.url if trip.er_file else '',
            str(trip.created_at),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=trips.xlsx'

    workbook.save(response)

    return response

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        'admin',
        'mohdashraf09458@gmail.com',
        'admin@111'
    )