# Django convention to have this in a seperate file
# might be usefull for form as well
from django.core.exceptions import ValidationError


def validate_name(value):  # name can't contain numbers, ect
    for v in value:
        if not (v == " " or v == "-" or v.isalpha()):
            raise ValidationError("Ugyldig navn")
    return value
