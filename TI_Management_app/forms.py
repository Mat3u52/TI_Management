from django import forms
from .models import MembersZZTI


class MemberForm(forms.ModelForm):
    class Meta:
        model = MembersZZTI
        fields = ['image']
