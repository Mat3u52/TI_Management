from django import template
from ..models import MembersZZTI, BankStatement
from django.contrib.auth.models import User
from datetime import datetime
import os
import calendar
from django.forms import CheckboxInput
from django.utils import timezone
from django.db.models import Q

register = template.Library()


# @register.simple_tag
@register.filter(name='admin_exist')
def admin_exist(member_nr):
    return User.objects.filter(username=member_nr).first()


@register.filter(name='show_timestamp')
def show_timestamp(timestamp):
    current_time = datetime.utcnow()
    timestamp = int(current_time.timestamp())
    return timestamp


@register.filter(name='comma_to_period')
def comma_to_period(value):
    return str(value).replace(',', '.')


@register.filter(name='filename')
def filename(value):
    # return os.path.basename(value)
    if hasattr(value, 'path'):
        return os.path.basename(value.path)
    return os.path.basename(value)


@register.filter(name='month_name')
def month_name(month_number):
    return calendar.month_name[month_number]


@register.filter(name='to_int')
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


@register.simple_tag
def get_months_until_now(year=None):
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    months = [
        "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
        "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
    ]
    numeric_months = list(range(1, 13))

    if year is None or year >= current_year:
        months_until_now = [(months[i], numeric_months[i]) for i in range(current_month)]
    else:
        months_until_now = [(months[i], numeric_months[i]) for i in range(12)]

    return months_until_now


@register.filter(name='record_exist')
def record_exist(year, month):
    return BankStatement.objects.filter(year_bank_statement=year, month_bank_statement=month).first()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def add(*args):
    return sum(args)


@register.simple_tag
def subtract(value, *args):
    result = value
    for arg in args:
        result -= arg
    return result


@register.filter(name='phone_number')
def phone_number_format(value):
    """Formats a phone number to (XXX) XXX-XXXX format."""
    value = str(value)  # Ensure value is treated as a string
    if len(value) == 9:
        return f'(+48) {value[0:3]}-{value[3:6]}-{value[6:9]}'
    else:
        return value  # Return original value if not 10 characters (no formatting)


@register.filter(name='member_img_exist')
def member_img_exist(member_nr):
    try:
        member = MembersZZTI.objects.get(member_nr=member_nr)
        if member.image:
            return member.image
        else:
            return ''  # No image found, return an empty string or a default path if desired
    except MembersZZTI.DoesNotExist:
        return ''  # Member does not exist, return an empty string or a default path if desired


@register.filter(name='member_full_name_exist')
def member_full_name_exist(member_nr):
    try:
        member = MembersZZTI.objects.get(member_nr=member_nr)
        if member.forename and member.surname:
            return f"{member.forename} {member.surname}"
        else:
            return ''
    except MembersZZTI.DoesNotExist:
        return ''


@register.filter
def is_checkbox(field):
    """Returns True if the field's widget is a CheckboxInput."""
    return isinstance(field.field.widget, CheckboxInput)


@register.simple_tag
def member_notepad_history(member, title=""):
    # Filtering member's notepad history based on conditions
    history = member.notepad.filter(
        Q(published_date__lte=timezone.now()) &
        Q(title__contains=title)
    ).order_by('published_date').first()
    return history
