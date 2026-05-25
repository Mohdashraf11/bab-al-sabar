from django.db import models
from .validators import (
    validate_container_photo,
    validate_er_file
)

class Trip(models.Model):
    truck_number = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100, unique=True)

    container_photo = models.ImageField(
        upload_to='container_photos/',
        validators=[validate_container_photo]
    )
    er_file = models.FileField(
        upload_to='er_files/',
        validators=[validate_er_file]
    )

    status = models.CharField(max_length=50, default="Trip Started")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.trip_id