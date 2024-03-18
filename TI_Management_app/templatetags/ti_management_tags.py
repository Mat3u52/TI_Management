from django import template
from ..models import MembersZZTI
from django.contrib.auth.models import User

register = template.Library()


# @register.simple_tag
@register.filter(name='admin_exist')
def admin_exist(member_nr):
    return User.objects.filter(username=member_nr).first()
