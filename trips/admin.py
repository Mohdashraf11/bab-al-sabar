from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        'trip_id',
        'truck_number',
        'status',
        'created_at',
    )

    search_fields = (
        'trip_id',
        'truck_number',
    )

    list_filter = (
        'status',
        'created_at',
    )

    ordering = (
        '-created_at',
    )