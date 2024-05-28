from django import template
from ..models import MembersZZTI
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
def show_timestamp(timestamp):
    current_time = datetime.utcnow()
    timestamp = int(current_time.timestamp())
    return timestamp


@register.filter(name='comma_to_period')
def comma_to_period(value):
    return str(value).replace(',', '.')


@register.filter
def filename(value):
    return os.path.basename(value)


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
