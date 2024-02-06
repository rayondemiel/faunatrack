from django.core.exceptions import ValidationError

def validate_latitude(value):
    if value <-90 or value > 90:
        raise ValidationError("La latitude doit être comprise entre -90 et 90")