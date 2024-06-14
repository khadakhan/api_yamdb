from datetime import datetime

from django.core.exceptions import ValidationError


def lte_current_year_validator(year):
    if year > datetime.now().year:
        raise ValidationError('Year must be less then or equal current one')


def validate_username_me(username):
    if username.lower() == 'me':
        raise ValidationError('Никнейм "me" недопустим.')
