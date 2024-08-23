import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_unique_number(value):
    """ Валидация поля на уникальный номер
      (цифра от 1000 до 9999 + случайная заглавная
     буква английского алфавита ставится автоматически"""

    if not re.match(r'^(?:[1-9][0-9]{3})$', value):
        raise ValidationError(
            _('Уникальный номер должен быть в формате: 4 цифры от 1000 до 9999'),
            params={'value': value},
        )
