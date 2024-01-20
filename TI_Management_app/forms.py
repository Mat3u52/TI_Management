from django import forms
from django.core.validators import RegexValidator
from .models import MembersZZTI, MembersFile, CardStatus, GroupsMember, Notepad, Groups, Cards
from django.utils import timezone


class MemberForm(forms.ModelForm):
    phone_number = forms.CharField(required=False, validators=[RegexValidator(r'^\+?1?\d{9,15}$',
                                                                              message="Wprowadź włąściwy numer telefonu.")])
    member_nr = forms.CharField(validators=[RegexValidator(r'^\d{0,10}$',
                                                           message="To pole musi być liczbą.")])
    pin = forms.IntegerField(required=True, validators=[RegexValidator(r'^\d{0,8}$',
                                                                       message="To pole musi być liczbą.")])

    class Meta:
        model = MembersZZTI
        fields = ['forename', 'surname', 'role', 'occupation',
                  'member_nr', 'sex', 'birthday', 'birthplace', 'pin', 'phone_number',
                  'email', 'date_of_accession', 'date_of_abandonment', 'type_of_contract',
                  'date_of_contract', 'expiration_date_contract', 'group', 'card', 'image']

        widgets = {
            'date_of_accession': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_abandonment': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_contract': forms.TextInput(attrs={'type': 'datetime-local'}),
            'expiration_date_contract': forms.TextInput(attrs={'type': 'datetime-local'}),
            'birthday': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

    # def clean_pin(self, *args, **kwargs):
    #     pin = self.cleaned_data.get("pin")

        # if MembersZZTI.objects.filter(pin=pin).exists():
        #     raise forms.ValidationError("To pole musi być unikalne.")

        # if pin.is_integer() is False:
        # if type(pin) == float:
        #     raise forms.ValidationError('To pole musi być liczbą')

        # if len(str(pin)) != 8:
        #     raise forms.ValidationError('To pole musi sładać się z 8 znaków.')
        #
        # return pin

    # def clean_member_nr(self, *args, **kwargs):
    #     member_nr = self.cleaned_data.get("member_nr")
    #
    #     if MembersZZTI.objects.filter(member_nr=member_nr).exists():
    #         raise forms.ValidationError("To pole musi być unikalne.")
    #
    #     return member_nr


class MemberFileForm(forms.ModelForm):
    class Meta:
        model = MembersFile
        fields = ['title', 'file']


class CardStatusForm(forms.ModelForm):
    card_identity = forms.CharField(validators=[RegexValidator(r'^\d{0,10}$',
                                                               message="To pole musi być liczbą.")], required=False)
    card_start_pin = forms.CharField(validators=[RegexValidator(r'^\d{0,10}$',
                                                                message="To pole musi być liczbą.")], required=False)

    # responsible = forms.CharField(initial='admin')
    # responsible = forms.CharField(initial=user.username)
    # widget = forms.HiddenInput(),
    responsible = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = CardStatus
        fields = ['card', 'card_identity', 'card_start_pin', 'card_status', 'date_of_action',
                  'file_name', 'file', 'file_date', 'file_name_a', 'file_a', 'file_a_date', 'responsible', 'confirmed']

        widgets = {
            'date_of_action': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_a_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class GroupsMemberForm(forms.ModelForm):
    class Meta:
        model = GroupsMember
        fields = ['group',]


class NotepadMemberForm(forms.ModelForm):
    class Meta:
        responsible = forms.CharField(widget=forms.HiddenInput())

        model = Notepad
        fields = ['title', 'content', 'published_date', 'importance',
                  'method', 'status', 'responsible', 'file', 'confirmed']

        widgets = {
            'published_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class GroupsForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['group_name',]


class GroupsEditForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['group_name',]


class GroupAddMemberForm(forms.ModelForm):
    # group = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = GroupsMember
        fields = ['member', 'group']


class LoyaltyCardForm(forms.ModelForm):
    class Meta:
        # responsible = forms.CharField(widget=forms.HiddenInput())

        model = Cards
        fields = ['card_name',]


class LoyaltyCardAddMemberForm(forms.ModelForm):

    card_identity = forms.CharField(validators=[RegexValidator(r'^\d{0,10}$',
                                                               message="To pole musi być liczbą.")], required=False)
    card_start_pin = forms.CharField(validators=[RegexValidator(r'^\d{0,10}$',
                                                                message="To pole musi być liczbą.")], required=False)

    responsible = forms.CharField(widget=forms.HiddenInput())
    # card = forms.CharField(widget=forms.HiddenInput())
    card = forms.CharField(disabled=True)
    member = forms.CharField(disabled=True)

    date_of_action = forms.DateField(initial=timezone.now())

    class Meta:
        model = CardStatus
        fields = ['member', 'card', 'card_identity', 'card_start_pin', 'card_status', 'date_of_action',
                  'file_name', 'file', 'file_date', 'file_name_a', 'file_a', 'file_a_date', 'responsible', 'confirmed']

        widgets = {
            'date_of_action': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_a_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
