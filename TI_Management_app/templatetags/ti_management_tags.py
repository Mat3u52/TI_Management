from django import template
from ..models import MembersZZTI, BankStatement
from django.contrib.auth.models import User
from datetime import datetime
import os
import calendar

register = template.Library()


# @register.simple_tag
@register.filter(name='admin_exist')
def admin_exist(member_nr):
    return User.objects.filter(username=member_nr).first()


@register.filter(name='show_timestamp')
# def show_timestamp(timestamp):
def show_timestamp():
    current_time = datetime.utcnow()
    timestamp = int(current_time.timestamp())
    return timestamp


@register.filter(name='comma_to_period')
def comma_to_period(value):
    return str(value).replace(',', '.')


@register.filter(name='filename')
def filename(value):
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
