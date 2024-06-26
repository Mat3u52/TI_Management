import re
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
    GroupsFile,
    DocumentsDatabase,
    DocumentsDatabaseCategory,
    Relief,
    RelationRegisterRelief,
    RegisterRelief,
    FileRegisterRelief,
    SignatureRelief,
    AverageSalary,
    Scholarships,
    KindOfFinanceDocument,
    KindOfFinanceExpense,
    FileFinance,
    BankStatement
)
from django.utils import timezone
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from localflavor.pl.forms import PLPostalCodeField
from datetime import datetime, date, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from phone_field import PhoneField
from django_ckeditor_5.widgets import CKEditor5Widget


def validate_phone_number(value):
    phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
    if not phone_pattern.match(value):
        raise ValidationError('Wprowadź włąściwy numer telefonu.')

    
class MemberForm(forms.ModelForm):

    forename = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Imię',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Imię musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=100
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Nazwisko'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Nazwisko musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=100
    )

    birthplace = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Miejsce urodzenia'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Miejsce urodzenia musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=100
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '000 000 000',
                'class': 'phone-number'
            }
        ),
        label="Numer kontaktowy",
        help_text='Numer telefonu',
        required=False,
        validators=[validate_phone_number]
    )

    extension = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '+48',
                'class': 'ext-input',
                'disabled': 'disabled'
            }
        ),
        required=False,
        initial='+48'
    )

    member_nr = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Numer Członka'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=6,
                message="Numer Członka musi zawierać 6 znaków."
            ),
            RegexValidator(
                regex=r'^\d{0,10}$',
                message="To pole musi być liczbą."
            )
        ],
        max_length=100
    )

    pin = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'number',
                'aria-label': 'PIN'
            }
        ),
        validators=[
            MinValueValidator(
                limit_value=0,
                message="PIN musi być dodatni."
            ),
            MaxValueValidator(
                limit_value=9999,
                message="PIN max 9999."
            ),
            RegexValidator(
                r'^\d{0,8}$',
                message="To pole musi być liczbą."
            )
        ],
        required=True
    )

    image = forms.FileField(
        label='Select a jpeg file',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/jpeg,image/png'
            }
        ),
        required=False
    )

    recommendation = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control me-2',
                'style': 'min-width: 1%!important; min-height: 25px',
                'aria-label': 'rekomendacja',
                'id': 'recommendation',
            }
        ),
        required=False
    )

    recommended_member_nr = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'list': 'members',
                'aria-label': 'Nr Członka rekomendowanego',
                'name': 'recommended_member_nr',
            }
        ),
        required=False
    )

    member_function = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'placeholder': 'Funkcja',
                'aria-label': 'Funkcja Członka',
                'list': 'roles_database'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Funkcja Członka musi zawierać co najmniej 2 znaki."
            )
        ],
        required=True,
        max_length=150
    )

    member_occupation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'placeholder': 'Stanowisko',
                'aria-label': 'Stanowisko Członka',
                'list': 'occupation_database'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Stanowisko musi zawierać co najmniej 2 znaki."
            ),
        ],
        required=True,
        max_length=150
    )

    class Meta:
        model = MembersZZTI
        fields = [
            'forename',
            'surname',
            'member_function',
            'member_occupation',
            'member_nr',
            'sex',
            'birthday',
            'birthplace',
            'pin',
            'phone_number',
            'email',
            'date_of_accession',
            'date_of_abandonment',
            'type_of_contract',
            'date_of_contract',
            'expiration_date_contract',
            'group',
            'recommendation',
            'recommended_member_nr',
            'image'
        ]

        widgets = {
            'birthday': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            # 'birthday': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_accession': forms.TextInput(
                attrs={
                    'type': 'date'
                }
            ),
            # 'date_of_accession': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_abandonment': forms.TextInput(
                attrs={
                    'type': 'date'
                }
            ),
            # 'date_of_abandonment': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date_of_contract': forms.TextInput(
                attrs={
                    'type': 'date'
                }
            ),
            # 'date_of_contract': forms.TextInput(attrs={'type': 'datetime-local'}),
            'expiration_date_contract': forms.TextInput(
                attrs={
                    'type': 'date'
                }
            ),
            # 'expiration_date_contract': forms.TextInput(attrs={'type': 'datetime-local'}),
            'sex': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'type_of_contract': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'group': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

        self.fields['forename'].widget.attrs['placeholder'] = 'Imię'
        self.fields['surname'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['member_nr'].widget.attrs['placeholder'] = '6 znaków: 000000'
        eighteen_years_ago = date.today() - timedelta(days=18 * 365)
        eighteen_years_ago_str = eighteen_years_ago.strftime('%Y-%m-%d')
        self.fields['birthday'].initial = eighteen_years_ago_str
        self.fields['birthplace'].widget.attrs['placeholder'] = 'Miejsce urodzenia'
        self.fields['pin'].widget.attrs['placeholder'] = '4 znaki: 0000'
        self.fields['email'].widget.attrs['placeholder'] = 'user@user.com'
        current_data = date.today()
        current_data_str = current_data.strftime('%Y-%m-%d')
        self.fields['date_of_accession'].initial = current_data_str
        one_year_later = date.today().replace(year=date.today().year + 1)
        one_year_later_str = one_year_later.strftime('%Y-%m-%d')
        self.fields['date_of_abandonment'].initial = one_year_later_str
        today_str = date.today().strftime('%Y-%m-%d')
        self.fields['date_of_contract'].initial = today_str
        three_year_later = date.today().replace(year=date.today().year + 3)
        three_year_later_str = three_year_later.strftime('%Y-%m-%d')
        self.fields['expiration_date_contract'].initial = three_year_later_str
        self.fields['recommended_member_nr'].widget.attrs['placeholder'] = 'Nr Członka'
        self.fields['type_of_contract'].required = True

    def clean(self):
        cleaned_data = super().clean()
        date_of_accession = cleaned_data.get("date_of_accession")
        date_of_abandonment = cleaned_data.get("date_of_abandonment")
        date_of_contract = cleaned_data.get("date_of_contract")
        expiration_date_contract = cleaned_data.get("expiration_date_contract")

        if date_of_accession and date_of_abandonment:
            if date_of_accession >= date_of_abandonment:
                raise ValidationError("Data przystąpienia musi być wcześniejsza niż data rezygnacji.")

        if date_of_accession and date_of_contract:
            if date_of_accession < date_of_contract:
                raise ValidationError("Data przystąpienia musi być późniejsza niż data zatrudnienia.")

        if expiration_date_contract and date_of_contract:
            if expiration_date_contract < date_of_contract:
                raise ValidationError("Data rozwiązania umowy musi być późniejsza niż data zatrudnienia.")

        # phone_number = self.cleaned_data.get('phone_number')
        # PhoneField().clean(phone_number, None)

        return cleaned_data


class MemberCardEditForm(forms.ModelForm):

    card = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'autofocus': 'autofocus',
                'placeholder': 'Przyłóż kartę do czytnika'
            }
        ),
        required=False
    )

    class Meta:
        model = MembersZZTI
        fields = [
            'card'
        ]


class MemberEditForm(forms.ModelForm):

    forename = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Imię',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Imię musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=100
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Nazwisko'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Nazwisko musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=100
    )

    birthplace = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Miejsce urodzenia'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Miejsce urodzenia musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=100
    )

    member_nr = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Numer Członka'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=6,
                message="Numer Członka musi zawierać 6 znaków."
            ),
            RegexValidator(
                regex=r'^\d{0,10}$',
                message="To pole musi być liczbą."
            )
        ],
        max_length=100
    )

    pin = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'number',
                'aria-label': 'PIN'
            }
        ),
        validators=[
            MinValueValidator(
                limit_value=0,
                message="PIN musi być dodatni."
            ),
            MaxValueValidator(
                limit_value=9999,
                message="PIN max 9999."
            ),
            RegexValidator(
                r'^\d{0,8}$',
                message="To pole musi być liczbą."
            )
        ],
        required=True
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '000 000 000',
                'class': 'phone-number'
            }
        ),
        label="Numer kontaktowy",
        help_text='Numer telefonu',
        required=False,
        validators=[validate_phone_number]
    )

    extension = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '+48',
                'class': 'ext-input',
                'disabled': 'disabled'
            }
        ),
        required=False,
        initial='+48'
    )

    image = forms.FileField(
        label='Select a jpeg file',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/jpeg,image/png'
            }
        ),
        required=False
    )

    class Meta:
        model = MembersZZTI
        fields = [
            'forename',
            'surname',
            'role',
            'occupation',
            'member_nr',
            'sex',
            'birthday',
            'birthplace',
            'pin',
            'phone_number',
            'email',
            'date_of_accession',
            'date_of_abandonment',
            'type_of_contract',
            'date_of_contract',
            'expiration_date_contract',
            'group',
            # 'card',
            'image'
        ]

        widgets = {
            # 'birthday': forms.DateInput(attrs={'type': 'date'}),
            'birthday': forms.TextInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            # 'date_of_accession': forms.TextInput(attrs={'type': 'date'}),
            'date_of_accession': forms.TextInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            # 'date_of_abandonment': forms.TextInput(attrs={'type': 'date'}),
            'date_of_abandonment': forms.TextInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            # 'date_of_contract': forms.TextInput(attrs={'type': 'date'}),
            'date_of_contract': forms.TextInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            # 'expiration_date_contract': forms.TextInput(attrs={'type': 'date'}),
            'expiration_date_contract': forms.TextInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            'sex': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'type_of_contract': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'group': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'role': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'occupation': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super(MemberEditForm, self).__init__(*args, **kwargs)

        self.fields['forename'].widget.attrs['placeholder'] = 'Imię'
        self.fields['surname'].widget.attrs['placeholder'] = 'Nazwisko'
        self.fields['member_nr'].widget.attrs['placeholder'] = '6 znaków: 000000'
        eighteen_years_ago = date.today() - timedelta(days=18 * 365)
        eighteen_years_ago_str = eighteen_years_ago.strftime('%Y-%m-%d')
        self.fields['birthday'].initial = eighteen_years_ago_str
        self.fields['birthplace'].widget.attrs['placeholder'] = 'Miejsce urodzenia'
        self.fields['pin'].widget.attrs['placeholder'] = '4 znaki: 0000'
        self.fields['email'].widget.attrs['placeholder'] = 'user@user.com'
        current_data = date.today()
        current_data_str = current_data.strftime('%Y-%m-%d')
        self.fields['date_of_accession'].initial = current_data_str
        one_year_later = date.today().replace(year=date.today().year + 1)
        one_year_later_str = one_year_later.strftime('%Y-%m-%d')
        self.fields['date_of_abandonment'].initial = one_year_later_str
        today_str = date.today().strftime('%Y-%m-%d')
        self.fields['date_of_contract'].initial = today_str
        three_year_later = date.today().replace(year=date.today().year + 3)
        three_year_later_str = three_year_later.strftime('%Y-%m-%d')
        self.fields['expiration_date_contract'].initial = three_year_later_str
        self.fields['type_of_contract'].required = True

    def clean(self):
        cleaned_data = super().clean()
        date_of_accession = cleaned_data.get("date_of_accession")
        date_of_abandonment = cleaned_data.get("date_of_abandonment")
        date_of_contract = cleaned_data.get("date_of_contract")
        expiration_date_contract = cleaned_data.get("expiration_date_contract")
        pin = cleaned_data.get("pin")

        if date_of_accession and date_of_abandonment:
            if date_of_accession >= date_of_abandonment:
                raise ValidationError("Data przystąpienia musi być wcześniejsza niż data rezygnacji.")

        if date_of_accession and date_of_contract:
            if date_of_accession < date_of_contract:
                raise ValidationError("Data przystąpienia musi być późniejsza niż data zatrudnienia.")

        if expiration_date_contract and date_of_contract:
            if expiration_date_contract < date_of_contract:
                raise ValidationError("Data rozwiązania umowy musi być późniejsza niż data zatrudnienia.")


        # phone_number = self.cleaned_data.get('phone_number')
        # PhoneField().clean(phone_number, None)

        return cleaned_data


class MemberEditReliefForm(forms.ModelForm):
    postcode = PLPostalCodeField()

    class Meta:
        model = MembersZZTI
        fields = [
            'street',
            'city',
            'postcode',
            'house_number',
            'float_number'
        ]


class MemberDeactivateForm(forms.ModelForm):

    class Meta:
        model = MembersZZTI
        fields = ['deactivate']


class MemberFunctionForm(forms.ModelForm):

    member_function = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'placeholder': 'Funkcja',
                'aria-label': 'Funkcja Członka',
                'list': 'roles_database',
                'autofocus': 'autofocus'
            }
        ),
        required=True,
        max_length=250
    )

    class Meta:
        model = MemberFunction
        fields = ['member_function',]


class MemberOccupationForm(forms.ModelForm):

    member_occupation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'placeholder': 'Stanowisko',
                'aria-label': 'Stanowisko Członka',
                'list': 'occupation_database',
                'autofocus': 'autofocus',
            }
        ),
        required=True,
        max_length=250
    )

    class Meta:
        model = MemberOccupation
        fields = ['member_occupation',]


class MemberFileForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Nazwa dokumentu',
                'aria-label': 'Nazwa dokumentu',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Nazwa dokumentu musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=150,
        required=True
    )

    file = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    class Meta:
        model = MembersFile
        fields = [
            'title',
            'file'
        ]


class CardStatusForm(forms.ModelForm):

    card_start_pin = forms.CharField(
        validators=[
            RegexValidator(
                r'^\d{0,10}$',
                message="To pole musi być liczbą."
            )
        ],
        required=False
    )

    responsible = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = CardStatus
        fields = [
            'ordered_doc',
            'to_be_picked_up_doc',
            'card_start_pin',
            'card_identity',
            'card_status',
            'date_of_action',
            'file_name',
            'file',
            'file_date',
            'file_name_a',
            'file_a',
            'file_a_date',
            'responsible',
            'confirmed'
        ]

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
                  'file_name',
                  'file',
                  'file_date',
                  'file_name_a',
                  'file_a',
                  'file_a_date',
                  'responsible',
                  'confirmed']

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

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'aria-label': 'Tytuł',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Tytuł musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=100
    )
    responsible = forms.CharField(
        widget=forms.HiddenInput()
    )

    class Meta:
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
            'content': CKEditor5Widget(
                config_name='default'
            ),
            'published_date': forms.TextInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
            # 'content': forms.Textarea(
            #     attrs={
            #         'rows': 12,
            #         'cols': 50
            #     }
            # ),
            'importance': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'method': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            )
        }


class NotepadMemberForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Tytuł sprawy',
                'aria-label': 'Tytuł sprawy',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Tytuł sprawy musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=150,
        required=True
    )
    # confirmed = forms.BooleanField(
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             'id': 'id_confirmed',
    #             'class': 'my-checkbox-class'
    #         }
    #     )
    # )

    class Meta:
        responsible = forms.CharField(widget=forms.HiddenInput())

        model = Notepad
        fields = [
            'title',
            'content',
            'published_date',
            'importance',
            'method',
            'status',
            'responsible',
            'file',
            'confirmed'
        ]

        widgets = {
            'published_date': forms.TextInput(
                attrs={'type': 'datetime-local'}
            ),
            # 'content': forms.Textarea(attrs={'rows': 12, 'cols': 50}),
            'content': CKEditor5Widget(
                config_name='default'
            ),
            'importance': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'method': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            )
        }


class GroupsForm(forms.ModelForm):

    group_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Nazwa Grupy',
                'aria-label': 'Nazwa Grupy',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Nazwa grupy musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=150,
        required=True
    )

    class Meta:
        model = Groups
        fields = [
            'group_name'
        ]


class GroupsEditForm(forms.ModelForm):

    group_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Nazwa Grupy',
                'aria-label': 'Nazwa Grupy',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Nazwa grupy musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=150,
        required=True
    )

    class Meta:
        model = Groups
        fields = ['group_name']


class GroupAddMemberForm(forms.ModelForm):
    class Meta:
        model = GroupsMember
        fields = [
            'member',
            'group'
        ]


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
                message="To pole może składać się tylko z liczb i małych liter."
            )
        ],
        required=False
    )
    card_start_pin = forms.CharField(
        validators=[
            RegexValidator(r'^\d{0,10}$',
                           message="To pole musi być liczbą.")],
        required=False
    )

    responsible = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = CardStatus
        fields = [
            'member',
            'card',
            'card_identity',
            'card_start_pin',
            'card_status',
            'file_name',
            'file',
            'file_date',
            'file_name_a',
            'file_a',
            'file_a_date',
            'responsible',
            'confirmed'
        ]

        widgets = {
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
        choices=SEX_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control select'
            }
        )
    )


class GroupAddRoleForm(forms.ModelForm):
    class Meta:
        model = MembersZZTI
        fields = [
            'role',
            'occupation',
        ]

        widgets = {
            'role': forms.Select(attrs={'class': 'form-control select'}),
            'occupation': forms.Select(attrs={'class': 'form-control select'}),
        }


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

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Tytuł dokumentu',
                'aria-label': 'Tytuł dokumentu',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Tytuł dokumentu musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=150,
        required=True
    )

    file = forms.FileField(
        label='Select a PDF file or JPEG',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf,image/jpeg,image/png'
            }
        ),
        required=True
    )

    class Meta:
        model = GroupsFile
        fields = [
            'title',
            'file'
        ]


class DocumentsDatabaseForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Tytuł dokumentu',
                'aria-label': 'Tytuł dokumentu',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Tytuł dokumentu musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=150,
        required=True
    )
    file = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    class Meta:
        model = DocumentsDatabase
        fields = [
            'title',
            'category',
            'file',
            'responsible'
        ]
        widgets = {
            'category': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            )
        }


class DocumentsDatabaseCategoryForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'type': 'text',
                'placeholder': 'Nazwa kategorii',
                'aria-label': 'Nazwa kategorii',
                'autofocus': 'autofocus'
            }
        ),
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Nazwa kategorii musi zawierać co najmniej 2 znaki."
            )
        ],
        max_length=150,
        required=True
    )

    class Meta:
        model = DocumentsDatabaseCategory
        fields = [
            'title',
            'responsible'
        ]


class ReliefFigureForm(forms.ModelForm):
    title = forms.CharField(
        required=True
    )
    figure = forms.FloatField(
        required=True,
        widget=forms.NumberInput(
            attrs={'step': "0.01"}
        )
    )
    grace = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={'step': "1"}
        )
    )

    class Meta:
        model = Relief
        fields = [
            'title',
            'figure',
            'grace'
        ]


class RelationRegisterReliefForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        max_length=250,
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    class Meta:
        model = RelationRegisterRelief
        fields = [
            'title'
        ]


class RegisterReliefForm(forms.ModelForm):

    class Meta:
        model = RegisterRelief
        fields = [
            'relief',
            'relation',
            'associate_forename',
            'associate_surname',
            'account_number',
            'date_of_completing_the_application',
            'date_of_receipt_the_application',
            'date_of_accident',
            'reason'
        ]
        widgets = {
            'date_of_completing_the_application': forms.DateInput(attrs={'type': 'date'}),
            'date_of_receipt_the_application': forms.TextInput(attrs={'type': 'date'}),
            'date_of_accident': forms.TextInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        date_of_accident = cleaned_data.get('date_of_accident')

        if not date_of_accident:
            raise forms.ValidationError("Podaj datę zdarzenia.")

        relief = cleaned_data.get('relief')
        if relief:
            grace_period = relief.grace
            grace_period = grace_period*30
        else:
            raise forms.ValidationError("Nie można pobrać czasu karencji dla tej zapomogi.")

        waiting_period_end = date_of_accident + timezone.timedelta(days=grace_period)

        if timezone.now() < waiting_period_end:
            remaining_days = (waiting_period_end - timezone.now()).days
            raise forms.ValidationError(f"Czas karencji {relief.grace} nie minął. Pozostało {remaining_days} dni.")

        bank_account = cleaned_data.get('account_number')
        if bank_account:
            if not re.match(r'^\d{26}$', bank_account):
                raise forms.ValidationError("Nieprawidłowy numer konta bankowego.")

        return cleaned_data


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileRegisterReliefForm(forms.ModelForm):
    file = MultipleFileField(label='Select files', required=True)

    class Meta:
        model = FileRegisterRelief
        fields = ['file']


class CardRegisterReliefForm(forms.Form):
    card = forms.CharField(
        required=True,
        max_length=250,
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    class Meta:
        model = MembersZZTI
        fields = ['card']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(CardRegisterReliefForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['card'].initial = self.instance.card

    def clean(self):
        cleaned_data = super().clean()
        card = cleaned_data.get('card')

        instance = self.instance

        if instance and instance.card != card:
            raise forms.ValidationError("Niepoprawny podpis.")

        return cleaned_data


class SignatureReliefForm(forms.Form):
    card = forms.CharField(
        required=True,
        max_length=250,
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def __init__(self, relief_to_be_signed, *args, **kwargs):
        self.relief_to_be_signed = relief_to_be_signed
        super(SignatureReliefForm, self).__init__(*args, **kwargs)

    def clean_card(self):
        card = self.cleaned_data['card']
        if not MembersZZTI.objects.filter(card=card).exists():
            raise forms.ValidationError("Taki Członek nie istnieje!")
        if MembersZZTI.objects.filter(card=card).exists():
            member = MembersZZTI.objects.get(card=card)
            if User.objects.filter(username=member.member_nr).exists():
                existing_user = User.objects.filter(username=member.member_nr).first()
                if not existing_user.is_active:
                    raise forms.ValidationError(f"Członek nie jest aktywny!")

        existing_signature = self.relief_to_be_signed.registerReliefSignatureRelief.filter(member=member).exists()
        if existing_signature:
            raise forms.ValidationError("Podpis już istnieje.")

        return card


class PaymentConfirmationReliefForm(forms.Form):
    payment_confirmation = forms.BooleanField(initial=True)


class ConfirmedReliefTimeRangeForm(forms.Form):

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


class AverageSalaryForm(forms.ModelForm):

    class Meta:
        model = AverageSalary
        fields = [
            'title',
            'salary'
        ]


class ScholarshipsForm(forms.ModelForm):
    file_scholarship_application = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_scanned_confirmation_of_payment_for_studies = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_declaration_of_income = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_resolution_consenting = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_document_confirming_of_the_semester = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_university_regulations_of_the_grading_scale = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    class Meta:
        model = Scholarships
        fields = [
            'title',
            # 'member',
            'application_creation_date',
            'seminary_start_date',
            'seminary_end_date',
            'member_salary',
            'preferred_university',
            'average_grade',
            'grading_scale',
            'tuition_fee_amount',
            'file_scholarship_application',
            'file_scanned_confirmation_of_payment_for_studies',
            'file_declaration_of_income',
            'file_resolution_consenting',
            'file_document_confirming_of_the_semester',
            'file_university_regulations_of_the_grading_scale',
            'confirmation_of_student_id',
            'scholarship_rate'
        ]

        widgets = {
            'application_creation_date': forms.DateInput(attrs={'type': 'date'}),
            'seminary_start_date': forms.DateInput(attrs={'type': 'date'}),
            'seminary_end_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, member, *args, **kwargs):
        self.member = member
        super(ScholarshipsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        seminary_start_date = cleaned_data.get('seminary_start_date')
        seminary_end_date = cleaned_data.get('seminary_end_date')
        application_creation_date = cleaned_data.get('application_creation_date')
        confirmation_of_student_id = cleaned_data.get('confirmation_of_student_id')
        scholarship_rate = cleaned_data.get('scholarship_rate')

        if seminary_start_date and self.member:
            difference = seminary_start_date - self.member.date_of_accession
            if difference.days < 365:
                raise forms.ValidationError(f"Członek jest w związkach tylko przez: {difference.days} dni")

        if seminary_end_date and application_creation_date:
            difference = application_creation_date - seminary_end_date
            if difference.days > 30:
                raise forms.ValidationError(f"Okres na złożenie wniosku został przekroczony: {difference.days} dni")

        if confirmation_of_student_id is False:
            raise forms.ValidationError(f"Niepotwierdzona legitymacja studencka")

        if scholarship_rate == 0:
            raise forms.ValidationError(f"Stypendium nie przysługuje")

        return cleaned_data


class ScholarshipsEditForm(forms.ModelForm):
    file_scholarship_application = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_scanned_confirmation_of_payment_for_studies = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_declaration_of_income = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_resolution_consenting = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_document_confirming_of_the_semester = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    file_university_regulations_of_the_grading_scale = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf'
            }
        ),
        required=True
    )

    class Meta:
        model = Scholarships
        fields = [
            # 'title',
            # 'member',
            # 'application_creation_date',
            # 'seminary_start_date',
            # 'seminary_end_date',
            # 'member_salary',
            # 'preferred_university',
            # 'average_grade',
            # 'grading_scale',
            # 'tuition_fee_amount',
            'file_scholarship_application',
            'file_scanned_confirmation_of_payment_for_studies',
            'file_declaration_of_income',
            'file_resolution_consenting',
            'file_document_confirming_of_the_semester',
            'file_university_regulations_of_the_grading_scale',
            # 'confirmation_of_student_id',
            'scholarship_rate',
            'confirmation_of_scholarship'
        ]

        # widgets = {
        #     # 'application_creation_date': forms.DateInput(attrs={'type': 'date'}),
        #     # 'seminary_start_date': forms.DateInput(attrs={'type': 'date'}),
        #     # 'seminary_end_date': forms.DateInput(attrs={'type': 'date'})
        # }

    def __init__(self, *args, **kwargs):
        super(ScholarshipsEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        confirmation_of_scholarship = cleaned_data.get('confirmation_of_scholarship')
        scholarship_rate = cleaned_data.get('scholarship_rate')

        if confirmation_of_scholarship is False:
            raise forms.ValidationError(f"Proszę potwierdzić albo odrzucić wniosek")

        if scholarship_rate == 0:
            raise forms.ValidationError(f"Stypendium nie przysługuje")

        return cleaned_data


class KindOfFinanceDocumentForm(forms.ModelForm):

    title_doc = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'placeholder': 'Rodaj dokumentu',
                'aria-label': 'Rodaj dokumentu',
                'list': 'kind_of_finance_document',
                'autofocus': 'autofocus'
            }
        ),
        required=True,
        max_length=250
    )

    class Meta:
        model = KindOfFinanceDocument
        fields = ['title_doc']


class KindOfFinanceExpenseForm(forms.ModelForm):

    title_expense = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'placeholder': 'Nazwa wydatku',
                'aria-label': 'Nazwa wydatku',
                'list': 'expense_database'
            }
        ),
        required=True,
        max_length=250
    )

    class Meta:
        model = KindOfFinanceExpense
        fields = ['title_expense']


class FileFinanceForm(forms.ModelForm):

    figure = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control me-2',
                # 'style': 'max-width: 25%!important; min-height: 15px',
                'placeholder': '0.00 zł',
                'aria-label': 'Kwota',
                'min': '0',
                'step': '0.01',
                'required': 'required',
            }
        ),
        min_value=0,
        decimal_places=2,
        required=True,
        label='',
    )

    quantity = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control me-2',
                # 'style': 'max-width: 25%!important; min-height: 15px',
                'placeholder': '1',
                'value': '1',
                'aria-label': 'Pozycji na wyciągu',
                'min': '0',
                'step': '1',
                'required': 'required',
            }
        ),
        min_value=0,
        decimal_places=1,
        required=True,
        label='',
    )

    resolution_requirement = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control me-2',
                # 'style': 'min-width: 1%!important; min-height: 15px',
                'aria-label': 'Dokument bez uchwały',
                'id': 'documentRequirement'
            }
        ),
        label='',
        required=False
    )

    psychologist = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control me-2',
                # 'style': 'min-width: 1%!important; min-height: 15px',
                'aria-label': 'Pomoc psychologa',
                'id': 'PsychologistHelp'
            }
        ),
        label='',
        required=False
    )

    member_nr = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',
                'placeholder': 'Nr Członka',
                'aria-label': 'Nr Członka',
                'list': 'members'
            }
        ),
        required=False,
        max_length=250
    )

    file = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf,image/jpeg,image/png'
            }
        ),
        required=True
    )

    class Meta:
        model = FileFinance
        fields = [
            # 'title_doc',
            # 'title',
            'file',
            # 'type_of_document',
            'figure',
            'quantity',
            'payment_date',
            'resolution',
            'resolution_requirement',
            # 'expense_name',
            'psychologist',
            'member_nr',
            'description'
        ]
        widgets = {
            'payment_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'description': CKEditor5Widget(
                config_name='default'
            ),
            'resolution': forms.Select(
                attrs={
                    'class': 'form-control select'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(FileFinanceForm, self).__init__(*args, **kwargs)
        # self.fields['member'].queryset = MembersZZTI.objects.all().order_by('member_nr')
        self.fields['member_nr'].queryset = MembersZZTI.objects.filter(card__isnull=False, deactivate=False).order_by('member_nr')
        self.fields['resolution'].required = False

    def clean(self):
        cleaned_data = super().clean()
        psychologist = cleaned_data.get('psychologist')
        member_nr = cleaned_data.get('member_nr')
        quantity = cleaned_data.get('quantity')
        resolution_requirement = cleaned_data.get('resolution_requirement')
        if resolution_requirement is False:
            self.fields['resolution'].required = True

        if psychologist is True and not member_nr:
            self.add_error('member', "Proszę podać numer Członka")
        if psychologist is True and not MembersZZTI.objects.filter(member_nr=member_nr).exists():
            raise forms.ValidationError(f"Członek nie istnieje w bazie")

        if quantity < 0:
            raise forms.ValidationError(f"Tylko liczby dodatnie")

        return cleaned_data


class BankStatementForm(forms.ModelForm):

    file_bank_statement = forms.FileField(
        label='Select a PDF file',
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf,image/jpeg,image/png'
            }
        ),
        required=True
    )

    class Meta:
        model = BankStatement
        fields = [
            'year_bank_statement',
            'title_bank_statement',
            'file_bank_statement',
            'quantity_bank_statement',
            'starting_balance',
            'final_balance',
            'income_bank_statement'
        ]
