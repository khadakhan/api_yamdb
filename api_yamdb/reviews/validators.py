from datetime import datetime

from django.contrib.auth.models import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def lte_current_year_validator(year):
    if year > datetime.now().year:
        raise ValidationError('Year must be less then or equal current one')


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Никнейм "me" недопустим.')
    validator = UnicodeUsernameValidator()
    try:
        validator(value)
    except ValidationError as error:
        raise ValidationError(
            f"Никнейм содержит недопустимые символы: {error}")
