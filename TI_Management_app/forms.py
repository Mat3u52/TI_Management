from django import forms
from .models import MembersZZTI

class MemberForm(forms.ModelForm):
    class Meta:
        model = MembersZZTI
        fields = ['forename', 'surname', 'role',
                  'member_nr', 'sex', 'phone_number',
                  'email', 'date_of_accession', 'type_of_contract',
                  'date_of_contract', 'group', 'card_rfid',
                  'card_status', 'image']

        widgets = {
            'date_of_accession': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

