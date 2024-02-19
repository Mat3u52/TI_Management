from django import forms
from django.core.validators import RegexValidator
from .models import (
    MembersZZTI,
    MembersFile,
    CardStatus,
    GroupsMember,
    Notepad,
    Groups,
    GroupsNotepad,
    Cards,
    OrderedCardDocument,
    ToBePickedUpCardDocument,
    MemberFunction,
    MemberOccupation,
    GroupsFile
)
from django.utils import timezone
from django.forms.widgets import DateInput


class MemberForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$',
                                   message="Wprowadź włąściwy numer telefonu.")]
    )
    member_nr = forms.CharField(
        validators=[RegexValidator(r'^\d{0,10}$',
                                   message="To pole musi być liczbą.")]
    )
    pin = forms.IntegerField(
        required=True,
        validators=[RegexValidator(r'^\d{0,8}$',
                                   message="To pole musi być liczbą.")]
    )

    class Meta:
        model = MembersZZTI
        fields = ['forename', 'surname', 'role', 'occupation',
                  'member_nr', 'sex', 'birthday', 'birthplace', 'pin', 'phone_number',
                  'email', 'date_of_accession', 'date_of_abandonment', 'type_of_contract',
                  'date_of_contract', 'expiration_date_contract', 'group', 'card', 'image']

        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            # 'birthday': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_accession': forms.TextInput(attrs={'type': 'date'}),
            # 'date_of_accession': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_abandonment': forms.TextInput(attrs={'type': 'date'}),
            # 'date_of_abandonment': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_contract': forms.TextInput(attrs={'type': 'date'}),
            # 'date_of_contract': forms.TextInput(attrs={'type': 'datetime-local'}),
            'expiration_date_contract': forms.TextInput(attrs={'type': 'date'}),
            # 'expiration_date_contract': forms.TextInput(attrs={'type': 'datetime-local'}),

        }


class MemberEditForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$',
                                   message="Wprowadź włąściwy numer telefonu.")]
    )

    member_nr = forms.CharField(
        validators=[RegexValidator(r'^\d{0,10}$',
                                   message="To pole musi być liczbą.")]
    )
    pin = forms.IntegerField(
        required=True,
        validators=[RegexValidator(r'^\d{0,8}$',
                                   message="To pole musi być liczbą.")]
    )

    class Meta:
        model = MembersZZTI
        fields = ['forename', 'surname', 'role', 'occupation',
                      'member_nr', 'sex', 'birthday', 'birthplace', 'pin', 'phone_number',
                      'email', 'date_of_accession', 'date_of_abandonment', 'type_of_contract',
                      'date_of_contract', 'expiration_date_contract', 'group', 'card', 'image']

        widgets = {
                # 'birthday': forms.DateInput(attrs={'type': 'date'}),
                'birthday': forms.TextInput(attrs={'type': 'datetime-local'}),
                # 'date_of_accession': forms.TextInput(attrs={'type': 'date'}),
                'date_of_accession': forms.TextInput(attrs={'type': 'datetime-local'}),
                # 'date_of_abandonment': forms.TextInput(attrs={'type': 'date'}),
                'date_of_abandonment': forms.TextInput(attrs={'type': 'datetime-local'}),
                # 'date_of_contract': forms.TextInput(attrs={'type': 'date'}),
                'date_of_contract': forms.TextInput(attrs={'type': 'datetime-local'}),
                # 'expiration_date_contract': forms.TextInput(attrs={'type': 'date'}),
                'expiration_date_contract': forms.TextInput(attrs={'type': 'datetime-local'}),

        }


class MemberDeactivateForm(forms.ModelForm):

    class Meta:
        model = MembersZZTI
        fields = ['deactivate']


class MemberFunctionForm(forms.ModelForm):
    class Meta:
        model = MemberFunction
        fields = ['member_function',]


class MemberOccupationForm(forms.ModelForm):
    class Meta:
        model = MemberOccupation
        fields = ['member_occupation',]


class MemberFileForm(forms.ModelForm):
    class Meta:
        model = MembersFile
        fields = ['title', 'file']


class CardStatusForm(forms.ModelForm):

    card_start_pin = forms.CharField(
        validators=[
            RegexValidator(r'^\d{0,10}$',
                           message="To pole musi być liczbą.")],
        required=False)

    responsible = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = CardStatus
        fields = ['ordered_doc',
                  'to_be_picked_up_doc',
                  'card_start_pin',
                  'card_identity',
                  'card_status',
                  'date_of_action',
                  'file_name', 'file', 'file_date', 'file_name_a', 'file_a', 'file_a_date', 'responsible', 'confirmed']

        widgets = {
            'date_of_action': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_a_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class CardStatusEditForm(forms.ModelForm):

    card_start_pin = forms.CharField(
        validators=[
            RegexValidator(r'^\d{0,10}$',
                           message="To pole musi być liczbą.")],
        required=False)

    responsible = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = CardStatus
        fields = ['ordered_doc',
                  'to_be_picked_up_doc',
                  'card_start_pin',
                  'card_status',
                  'date_of_action',
                  'file_name', 'file', 'file_date', 'file_name_a', 'file_a', 'file_a_date', 'responsible', 'confirmed']

        widgets = {
            'date_of_action': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'file_a_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class CardStatusCardIDForm(forms.ModelForm):
    card_identity = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9]+$',
                message="To pole może składać się tylko z liczb i małych liter.")],
        required=False)

    responsible = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = CardStatus
        fields = ['card_identity', 'responsible']


class GroupsMemberForm(forms.ModelForm):
    class Meta:
        model = GroupsMember
        fields = ['member',]


class GroupNotepadForm(forms.ModelForm):
    class Meta:
        responsible = forms.CharField(widget=forms.HiddenInput())

        model = GroupsNotepad
        fields = [
            'title',
            'content',
            'published_date',
            'importance',
            'method',
            'status',
            'responsible'
        ]

        widgets = {
            'published_date': forms.TextInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'rows': 12,
                    'cols': 50
                }
            ),
        }


class NotepadMemberForm(forms.ModelForm):
    class Meta:
        responsible = forms.CharField(widget=forms.HiddenInput())

        model = Notepad
        fields = ['title', 'content', 'published_date', 'importance',
                  'method', 'status', 'responsible', 'file', 'confirmed']

        widgets = {
            'published_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'content': forms.Textarea(attrs={'rows': 12, 'cols': 50}),
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
    class Meta:
        model = GroupsMember
        fields = ['member', 'group']


class LoyaltyCardForm(forms.ModelForm):
    class Meta:

        model = Cards
        fields = ['card_name',]


class LoyaltyCardAddMemberForm(forms.ModelForm):

    card_identity = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9]+$',
                message="To pole może składać się tylko z liczb i małych liter.")],
        required=False
    )
    card_start_pin = forms.CharField(
        validators=[
            RegexValidator(r'^\d{0,10}$',
                           message="To pole musi być liczbą.")],
        required=False
    )

    responsible = forms.CharField(widget=forms.HiddenInput())

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


class LoyaltyCardsAddMemberFileOrderForm(forms.ModelForm):

    class Meta:
        model = CardStatus

        fields = ['ordered_doc', 'member', 'card', 'file_name', 'file', 'file_date']

        widgets = {
            'file_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class LoyaltyCardsAddMemberFileToBePickedUpForm(forms.ModelForm):

    class Meta:
        model = CardStatus

        fields = ['to_be_picked_up_doc', 'member', 'card', 'file_name_a', 'file_a', 'file_a_date']

        widgets = {
            'file_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class OrderedCardDocumentForm(forms.ModelForm):
    class Meta:
        model = OrderedCardDocument
        fields = ['card', 'title', 'file', 'responsible']


class ToBePickedUpCardDocumentForm(forms.ModelForm):
    class Meta:
        model = ToBePickedUpCardDocument
        fields = ['card', 'title', 'file', 'responsible']


class ExportDataToTXTForm(forms.Form):
    SEPARATOR_CHOICES = [
        (';', ';'),
        (',', ','),
        ('-', '-'),
        (':', ':'),
        ('/', '/'),
        ('#', '#'),
    ]

    DATA_CHOICES = [
        ('email', 'email'),
        ('phone_number', 'tel'),
        ('forename', 'imie'),
        ('surname', 'nazwisko'),
        ('member_nr', 'id członka'),
        ('card_identity', 'nr karty'),
    ]

    separator = forms.ChoiceField(
        choices=SEPARATOR_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-inline'
            }
        )
    )

    data = forms.MultipleChoiceField(
        choices=DATA_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    start_date = forms.DateField(
        label='Start Date',
        required=False,
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    end_date = forms.DateField(
        label='End Date',
        required=False,
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )


class GroupAddGenderForm(forms.Form):
    SEX_CHOICES = (
        ('---------', '---------'),
        ('female', 'Kobieta'),
        ('male', 'Mężczyzna'),
    )
    gender = forms.ChoiceField(
        choices=SEX_CHOICES
    )


class GroupAddRoleForm(forms.ModelForm):
    class Meta:
        model = MembersZZTI
        fields = [
            'role',
            'occupation',
        ]


class ExportDataSeparatorGroupForm(forms.Form):
    SEPARATOR_CHOICES = [
        (';', ';'),
        (',', ','),
        ('-', '-'),
    ]
    DATA_CHOICES = [
        ('email', 'email'),
        ('tel', 'tel'),
    ]

    # separator = forms.CharField()
    separator = forms.ChoiceField(
        choices=SEPARATOR_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-inline'
        })
    )
    data = forms.ChoiceField(
        choices=DATA_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-inline'
        })
    )


class GroupFileForm(forms.ModelForm):
    class Meta:
        model = GroupsFile
        fields = ['title', 'file']
