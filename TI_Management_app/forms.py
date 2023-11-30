from django import forms
from .models import MembersZZTI


class MemberForm(forms.ModelForm):
    class Meta:
        model = MembersZZTI
        fields = ['forename', 'surname', 'role',
                  'member_nr', 'sex', 'phone_number',
                  'email', 'date_of_accession', 'date_of_abandonment', 'type_of_contract',
                  'date_of_contract', 'group', 'card', 'image']

        widgets = {
            'date_of_accession': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_abandonment': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_contract': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

