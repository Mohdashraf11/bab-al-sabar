from django.contrib import admin
from .models import Trip

import csv
from django.http import HttpResponse

import openpyxl

from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors

from django.utils.html import format_html


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        'trip_id',
        'truck_number',
        'status',
        'container_photo_link',
        'second_container_photo_link',
        'er_file_link',
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

    date_hierarchy = 'created_at'

    ordering = ('-created_at',)

    list_per_page = 50

    actions = ['export_as_csv', 'export_as_excel', 'export_as_pdf',]


    def container_photo_link(self, obj):

        if obj.container_photo:

            return format_html(
                '<a href="{}" target="_blank">View Image</a>',
                obj.container_photo.url
            )

        return "No Image"


    container_photo_link.short_description = (
        "Container 1"
    )

    def second_container_photo_link(self, obj):

        if obj.second_container_photo:

            return format_html(
                '<a href="{}" target="_blank">View Image</a>',
                obj.second_container_photo.url
            )

        return "No Image"


    second_container_photo_link.short_description = (
        "Container 2"
    )

    def er_file_link(self, obj):

        if obj.er_file:

            return format_html(
                '<a href="{}" target="_blank">View File</a>',
                obj.er_file.url
            )

        return "No File"


    er_file_link.short_description = (
        "ER File"
    )

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = (
            'attachment; filename=trips.csv'
        )

        writer = csv.writer(response)

        writer.writerow([
            'Trip ID',
            'Truck Number',
            'Status',
            'Container Photo',
            'Second Container Photo',
            'ER File',
            'Created At',
        ])

        for trip in queryset:

            writer.writerow([
                trip.trip_id,
                trip.truck_number,
                trip.status,
                trip.container_photo.url if trip.container_photo else '',
                trip.second_container_photo.url if trip.second_container_photo else '',
                trip.er_file.url if trip.er_file else '',
                trip.created_at,
            ])

        return response


    export_as_csv.short_description = (
        "Export selected trips as CSV"
    )


    def export_as_excel(self, request, queryset):

        workbook = openpyxl.Workbook()

        sheet = workbook.active

        sheet.title = 'Trips'


        headers = [
            'Trip ID',
            'Truck Number',
            'Status',
            'Container Photo',
            'Second Container Photo',
            'ER File',
            'Created At',
        ]

        sheet.append(headers)


        for trip in queryset:

            sheet.append([
                trip.trip_id,
                trip.truck_number,
                trip.status,
                trip.container_photo.url if trip.container_photo else '',
                trip.second_container_photo.url if trip.second_container_photo else '',
                trip.er_file.url if trip.er_file else '',
                str(trip.created_at),
            ])


        response = HttpResponse(
            content_type=(
                'application/vnd.openxmlformats-'
                'officedocument.spreadsheetml.sheet'
            )
        )

        response['Content-Disposition'] = (
            'attachment; filename=trips.xlsx'
        )

        workbook.save(response)

        return response


    export_as_excel.short_description = (
        "Export selected trips as Excel"
    )

    def export_as_pdf(self, request, queryset):

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = (
            'attachment; filename=trips.pdf'
        )

        document = SimpleDocTemplate(response)

        data = [[
            'Trip ID',
            'Truck Number',
            'Status',
            'Container 1',
            'Container 2',
            'ER File',
            'Created At',
        ]]

        for trip in queryset:

            data.append([
                trip.trip_id,
                trip.truck_number,
                trip.status,
                trip.container_photo.url if trip.container_photo else '',
                trip.second_container_photo.url if trip.second_container_photo else '',
                trip.er_file.url if trip.er_file else '',
                str(trip.created_at),
            ])

        table = Table(data)

        table.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),

            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        ]))

        elements = [table]

        document.build(elements)

        return response


    export_as_pdf.short_description = (
        "Export selected trips as PDF"
    )