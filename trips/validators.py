from django.core.exceptions import ValidationError
import os


def validate_container_photo(file):

    allowed_extensions = ['.jpg', '.jpeg', '.png']

    ext = os.path.splitext(file.name)[1].lower()

    if ext not in allowed_extensions:

        raise ValidationError(
            "Only JPG, JPEG and PNG files are allowed."
        )

    if file.size > 5 * 1024 * 1024:

        raise ValidationError(
            "Container photo must be smaller than 5MB."
        )


def validate_er_file(file):

    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']

    ext = os.path.splitext(file.name)[1].lower()

    if ext not in allowed_extensions:

        raise ValidationError(
            "Only JPG, JPEG, PNG and PDF files are allowed."
        )

    if file.size > 10 * 1024 * 1024:

        raise ValidationError(
            "ER file must be smaller than 10MB."
        )