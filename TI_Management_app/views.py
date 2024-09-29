from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import (
    MembersZZTI,
    MembersFile,
    CardStatus,
    GroupsMember,
    Notepad,
    Groups,
    Cards,
    OrderedCardDocument,
    ToBePickedUpCardDocument,
    MemberFunction,
    MemberOccupation,
    GroupsFile,
    GroupsNotepad,
    DocumentsDatabase,
    DocumentsDatabaseCategory,
    Relief,
    RelationRegisterRelief,
    RegisterRelief,
    FileRegisterRelief,
    SignatureRelief,
    Scholarships,
    AverageSalary,
    KindOfFinanceDocument,
    FileFinance,
    KindOfFinanceExpense,
    BankStatement,
    Vote,
    Choice,
    Poll,
    VotingSessionKickOff,
    VotingSessionKickOffSignature,
    VotingSessionSignature,
    VotingResponses
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import (
    MemberForm,
    MemberEditForm,
    MemberDeactivateForm,
    MemberFileForm,
    CardStatusForm,
    CardStatusEditForm,
    CardStatusCardIDForm,
    GroupsMemberForm,
    NotepadMemberForm,
    GroupsForm,
    GroupNotepadForm,
    GroupsEditForm,
    GroupAddMemberForm,
    LoyaltyCardForm,
    LoyaltyCardAddMemberForm,
    LoyaltyCardsAddMemberFileOrderForm,
    LoyaltyCardsAddMemberFileToBePickedUpForm,
    OrderedCardDocumentForm,
    ToBePickedUpCardDocumentForm,
    ExportDataToTXTForm,
    GroupAddGenderForm,
    ExportDataSeparatorGroupForm,
    MemberFunctionForm,
    MemberOccupationForm,
    GroupAddRoleForm,
    GroupFileForm,
    DocumentsDatabaseForm,
    DocumentsDatabaseCategoryForm,
    ReliefFigureForm,
    RelationRegisterReliefForm,
    MemberEditReliefForm,
    RegisterReliefForm,
    FileRegisterReliefForm,
    CardRegisterReliefForm,
    SignatureReliefForm,
    PaymentConfirmationReliefForm,
    ConfirmedReliefTimeRangeForm,
    AverageSalaryForm,
    ScholarshipsForm,
    ScholarshipsEditForm,
    KindOfFinanceDocumentForm,
    KindOfFinanceExpenseForm,
    FileFinanceForm,
    BankStatementForm,
    MemberCardEditForm,
    VotingAddForm,
    VotingAddPollForm,
    VotingAddChoiceForm,
    VotingAddRecapForm,
    VotingSessionKickOffForm,
    VotingSessionKickOffSignatureForm,
    VotingSessionSignatureForm,
    ChoiceForm,
    VotingSessionCloseForm
)
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse  # txt file
from django.http import FileResponse  # pdf file
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import pdfmetrics, TTFont
from textwrap import wrap
from django.contrib import messages
import csv
from django.conf import settings

from django.http import JsonResponse

from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from datetime import datetime
from collections import defaultdict
import pytz
from decimal import Decimal
from django.db.models import Sum, Case, When, DecimalField, OuterRef, Subquery, Max
from .common.decorators import ajax_required
from django.db.models import Count
import bleach

from django.template.loader import render_to_string
import weasyprint
# import logging
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import redis

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    'p', 'br', 'div', 'span', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figure', 'table', 'tbody', 'tr', 'td'
]

ALLOWED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    'img': ['src', 'alt'],
    'a': ['href', 'title'],
    'span': ['style'],
    'div': ['style'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan']
}


@login_required
def members_list(request):
    members_obj = MembersZZTI.objects.all().order_by('-created_date')

    """
        It is temporary piece of code for verification whether user is not deactivate.
    """
    for member in members_obj:
        if member.date_of_abandonment:
            if member.date_of_abandonment < timezone.now():
                member.deactivate = True
                member.save()

    paginator = Paginator(members_obj, 50)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/members/members_list.html',
        {
            'page': page,
            'members': members
        }
    )


@login_required
def members_table_list(request):
    order_by = request.GET.get('order_by', '-forename')
    members_obj = MembersZZTI.objects.all().order_by(order_by)

    paginator = Paginator(members_obj, 50)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/members/members_table_list.html',
        {
            'page': page,
            'members': members
        }
    )


def member_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            'Imie',
            'Nazwisko',
            'Funkcja',
            'Zawód',
            'Numer',
            'Płeć',
            'Data urodzenia',
            'Miejsce urodzenia',
            'PPID',
            'Numer telefonu',
            'Email',
            'Data przystąpienia',
            'Data wystąpienia',
            'Rodzaj umowy',
            'Data zatrudnienia',
            'Data rozwiązania umowy',
            'Dezaktywacja'
        ]
    )

    members = MembersZZTI.objects.all().values_list(
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
        'deactivate'
    )

    for member in members:
        writer.writerow(member)

    return response


@login_required
def member_detail(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    accessible = Cards.objects.all()
    accessible_ids = accessible.values_list('id', flat=True)
    user_cards = CardStatus.objects.filter(member_id=pk, card__isnull=False)
    card_names = user_cards.values_list('card', flat=True).distinct()
    different_elements = set(accessible_ids).difference(set(card_names))

    accessible_group = Groups.objects.all()
    accessible_group_ids = accessible_group.values_list('id', flat=True)
    user_group = GroupsMember.objects.filter(member_id=pk, group__isnull=False)
    group_names = user_group.values_list('group', flat=True).distinct()
    different_elements_group = set(accessible_group_ids).difference(set(group_names))

    all_card_history_entries = member.history.filter(card__isnull=False)
    card_history_entries = []
    seen_cards = set()

    for entry in all_card_history_entries:
        if entry.card not in seen_cards:
            card_history_entries.append(entry)
            seen_cards.add(entry.card)

    all_note_entries = member.notepad.filter(title__isnull=False).order_by('-published_date')
    note_entries = []
    seen_note = set()

    for entry in all_note_entries:
        if entry.title not in seen_note:
            note_entries.append(entry)
            seen_note.add(entry.title)

    total_views = r.incr(f'member:{member.id}:views')

    return render(
        request,
        'TI_Management_app/members/member_detail.html',
        {
            'member': member,
            'accessible_ids': accessible_ids,
            'card_names': card_names,
            'different_elements': different_elements,
            'accessible': accessible,
            'accessible_group': accessible_group,
            'different_elements_group': different_elements_group,
            'card_history_entries': card_history_entries,
            'seen_cards': seen_cards,
            'note_entries': note_entries,
            'seen_note': seen_note,
            'total_views': total_views
        }
    )


@cache_page(60*15)
@login_required
def member_deactivate(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_loyalty_cards = CardStatus.objects.filter(member=member)
    member_groups = GroupsMember.objects.filter(member=member)

    if request.method == "POST":
        form = MemberDeactivateForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            if form.cleaned_data['deactivate'] is True:
                for card_status in member_loyalty_cards:
                    card_status.author = request.user
                    card_status.card_status = 'deactivated'
                    card_status.date_of_action = timezone.now()
                    card_status.save()
                member_groups.delete()

            member = form.save(commit=False)
            member.author = request.user
            member.date_of_abandonment = timezone.now()
            member.save()
            messages.success(request, "Członek został zdezaktywowany!")

            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberDeactivateForm(instance=member)
    return render(
        request,
        'TI_Management_app/members/member_deactivate.html',
        {
            'form': form,
            'member': member,
            'member_loyalty_cards': member_loyalty_cards,
            'member_groups': member_groups
        }
    )


def error_404_view(request, exception):
    data = {"name": "TI_Management"}
    return render(request, 'TI_Management_app/404.html', data)



@login_required
def member_new(request):
    roles = MemberFunction.objects.all()
    occupations = MemberOccupation.objects.all()
    members = MembersZZTI.objects.all().order_by('member_nr')

    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        # form_role = MemberFunctionForm(request.POST)
        # form_occupation = MemberOccupationForm(request.POST)

        # if form.is_valid() and form_role.is_valid() and form_occupation.is_valid():
        if form.is_valid():

            # role = form_role.cleaned_data['member_function']
            role = form.cleaned_data['member_function']
            if role:
                if not MemberFunction.objects.filter(member_function=role).exists():
                    # role_insert = form_role.save(commit=False)
                    # role_insert = form.save(commit=False)
                    # role_insert.author = request.user
                    # role_insert.save()
                    member_function = MemberFunction.objects.create(
                        author=request.user,
                        member_function=role
                    )
                    member_function.save()


            # occupation = form_occupation.cleaned_data['member_occupation']
            occupation = form.cleaned_data['member_occupation']

            if occupation:
                if not MemberOccupation.objects.filter(member_occupation=occupation).exists():
                    # occupation_insert = form_occupation.save(commit=False)
                    # occupation_insert = form.save(commit=False)
                    # occupation_insert.author = request.user
                    # occupation_insert.save()
                    member_occupation = MemberOccupation.objects.create(
                        author=request.user,
                        member_occupation=occupation
                    )
                    member_occupation.save()

            forename = form.cleaned_data['forename']
            surname = form.cleaned_data['surname']
            birthplace = form.cleaned_data['birthplace']

            member = form.save(commit=False)
            member.author = request.user
            member.forename = forename.title()
            member.surname = surname.title()
            if birthplace:
                member.birthplace = birthplace.title()
            if role:
                member.role = MemberFunction.objects.filter(member_function=role).latest('id')
            if occupation:
                member.occupation = MemberOccupation.objects.filter(member_occupation=occupation).latest('id')

            card = form.cleaned_data.get('card')
            if card:
                member.card = make_password(card)

            recommended_member_nr = form.cleaned_data.get('recommended_member_nr')
            if recommended_member_nr:
                member.recommended_by = recommended_member_nr

            type_of_contract = form.cleaned_data.get('type_of_contract')
            if type_of_contract == 'indefinite_period_of_time':
                member.expiration_date_contract = None

            member.save()
            messages.success(request, f"Gratulacje! {member.forename} jest naszym nowym Członkiem.")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberForm()
        # form_role = MemberFunctionForm()
        # form_occupation = MemberOccupationForm()

    return render(
        request,
        'TI_Management_app/members/member_new.html',
        {
            'form': form,
            # 'form_role': form_role,
            # 'form_occupation': form_occupation,
            'roles': roles,
            'occupations': occupations,
            'members': members
        }
    )


@login_required
def member_edit(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberEditForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            # member.save(update_fields=['forename'])
            member.save()
            messages.success(request, "Zaktualizowano!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberEditForm(instance=member)

    return render(
        request,
        'TI_Management_app/members/member_edit.html',
        {
            'form': form,
            'member': member
        }
    )


@login_required
def member_function_add(request):
    all_functions = MemberFunction.objects.all()
    if request.method == "POST":
        form = MemberFunctionForm(request.POST)
        if form.is_valid():
            function = form.save(commit=False)
            function.author = request.user
            function.save()
            messages.success(request, f"Dodano nową funkcję {function.member_function}!")
            return redirect('TI_Management_app:member_function_add')
    else:
        form = MemberFunctionForm()
    return render(
        request,
        'TI_Management_app/members/member_function_add.html',
        {
            'form': form,
            'all_functions': all_functions
        }
    )


@login_required
def member_function_edit(request, pk):
    all_functions = MemberFunction.objects.all()
    function = get_object_or_404(MemberFunction, pk=pk)
    if request.method == "POST":
        form = MemberFunctionForm(request.POST, instance=function)
        if form.is_valid():
            one_function = form.save(commit=False)
            one_function.author = request.user
            one_function.save()
            messages.success(request, "Zaktualizowano funkcję!")
            return redirect('TI_Management_app:member_function_add')
    else:
        form = MemberFunctionForm(instance=function)
    return render(
        request,
        'TI_Management_app/members/member_function_edit.html',
        {
            'form': form,
            'all_functions': all_functions,
            'function': function
        }
    )


@login_required
def member_occupation_add(request):
    all_occupation = MemberOccupation.objects.all()
    if request.method == "POST":
        form = MemberOccupationForm(request.POST)
        if form.is_valid():
            occupation = form.save(commit=False)
            occupation.author = request.user
            occupation.save()
            messages.success(request, f"Dodano nowe stanowisko {occupation.member_occupation}!")
            return redirect('TI_Management_app:member_occupation_add')
    else:
        form = MemberOccupationForm()
    return render(
        request,
        'TI_Management_app/members/member_occupation_add.html',
        {
            'form': form,
            'all_occupation': all_occupation
        }
    )


@login_required
def member_occupation_edit(request, pk):
    all_occupation = MemberOccupation.objects.all()
    occupation = get_object_or_404(MemberOccupation, pk=pk)
    if request.method == "POST":
        form = MemberOccupationForm(request.POST, instance=occupation)
        if form.is_valid():
            one_occupation = form.save(commit=False)
            one_occupation.author = request.user
            one_occupation.save()
            messages.success(request, f"Zaktualizowano stanowisko {occupation.member_occupation}!")
            return redirect('TI_Management_app:member_occupation_add')
    else:
        form = MemberOccupationForm(instance=occupation)
    return render(
        request,
        'TI_Management_app/members/member_occupation_edit.html',
        {
            'form': form,
            'all_occupation': all_occupation,
            'occupation': occupation
        }
    )


@cache_page(60*15)
@login_required
def member_card_edit(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberCardEditForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            card = form.cleaned_data.get('card')
            if card:
                member.card = make_password(card)
            member.save()
            messages.success(request, "Zaktualizowano!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberCardEditForm(instance=member)
    return render(
        request,
        'TI_Management_app/members/member_card_edit.html',
        {
            'form': form,
            'member': member
        }
    )


@login_required
def member_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        members = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
                                             Q(surname__contains=searched.capitalize()) |
                                             Q(member_nr__contains=searched) |
                                             Q(phone_number__contains=searched))
        return render(
            request,
            'TI_Management_app/members/member_search.html',
            {
                'searched': searched,
                'members': members
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/members/member_search.html',
            {}
        )


@login_required
def member_file_edit(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberFileForm(request.POST, request.FILES)  # , instance = member
        if form.is_valid():
            member_file = form.save(commit=False)
            member_file.author = request.user
            member_file.member = member
            member_file.save()
            messages.success(request, f"Dodano dokument {member_file.title}!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberFileForm()
    return render(
        request,
        'TI_Management_app/members/member_file_edit.html',
        {
            'form': form,
            'member': member
        }
    )


@login_required
def member_file_delete(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_file = get_object_or_404(MembersFile, pk=pk1)

    member.author = request.user
    member_file.file.delete()
    member_file.delete()
    return redirect('TI_Management_app:member_detail', pk=member.pk)


@login_required
def loyalty_card_list(request):
    loyalty_card_obj = Cards.objects.annotate(member_count=Count('loyaltyCardStatus')).order_by('-created_date')
    # loyalty_card_obj = Cards.objects.all()

    paginator = Paginator(loyalty_card_obj, 5)
    page = request.GET.get('page')
    try:
        loyalty_card = paginator.page(page)
    except PageNotAnInteger:
        loyalty_card = paginator.page(1)
    except EmptyPage:
        loyalty_card = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/loyalty_card/loyalty_card_list.html',
        {
            'page': page,
            'loyalty_card': loyalty_card
        }
    )


@login_required
def loyalty_card_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        loyalty_card = Cards.objects.filter(Q(card_name__icontains=searched))
        return render(
            request,
            'TI_Management_app/loyalty_card/loyalty_card_search.html',
            {
                'searched': searched,
                'loyalty_card': loyalty_card
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/loyalty_card/loyalty_card_search.html',
            {}
        )


@login_required
def loyalty_card_member_search(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    loyalty_card_validator = CardStatus.objects.all()
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        loyalty_card_member = MembersZZTI.objects.filter(
            Q(forename__contains=searched.capitalize()) |
            Q(surname__contains=searched.capitalize()) |
            Q(member_nr__contains=searched) |
            Q(phone_number__contains=searched),
            deactivate=False
        )
        members_in_validator = []
        for member in loyalty_card_member:
            exists_in_validator = loyalty_card_validator.filter(
                Q(member_id=member.id) &
                Q(card_id=loyalty_card.id)
            ).exists()
            if not exists_in_validator:
                members_in_validator.append(member)

        return render(
            request,
            'TI_Management_app/loyalty_card/loyalty_card_member_search.html',
            {
                'searched': searched,
                'loyalty_card_member': loyalty_card_member,
                'loyalty_card': loyalty_card,
                'loyalty_card_validator': loyalty_card_validator,
                'members_in_validator': members_in_validator,
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/loyalty_card/loyalty_card_member_search.html',
            {}
        )


@login_required
def loyalty_card_detail(request, pk, category):
    category = category
    loyalty_card = get_object_or_404(Cards, pk=pk)
    status_card_file = CardStatus.objects.order_by('-file_date')
    status_card_file_a = CardStatus.objects.order_by('-file_a_date')
    ordered_card_file = OrderedCardDocument.objects.all()
    to_be_picked_up_doc_card_file = ToBePickedUpCardDocument.objects.all()

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=Kary_Lojalnosciowe_{loyalty_card}_{timezone.now()}.txt'

    if request.method == 'POST' and category == 'active':
        form = ExportDataToTXTForm(request.POST)
        if form.is_valid():
            separator = form.cleaned_data['separator']
            data = form.cleaned_data['data']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            lines = []

            if start_date and end_date:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.filter(
                        date_of_action__range=(start_date, end_date)
                ):
                    if loyalty_card_all_user.card_status == 'active':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")
            else:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.all():
                    if loyalty_card_all_user.card_status == 'active':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")

            response.writelines(lines)

            return response

    if request.method == 'POST' and category == 'toBePickedUp':
        form = ExportDataToTXTForm(request.POST)
        if form.is_valid():
            separator = form.cleaned_data['separator']
            data = form.cleaned_data['data']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            lines = []

            if start_date and end_date:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.filter(
                        date_of_action__range=(start_date, end_date)
                ):
                    if loyalty_card_all_user.card_status == 'toBePickedUp':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")
            else:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.all():
                    if loyalty_card_all_user.card_status == 'toBePickedUp':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")

            response.writelines(lines)

            return response

    if request.method == 'POST' and category == 'ordered':
        form = ExportDataToTXTForm(request.POST)
        if form.is_valid():
            separator = form.cleaned_data['separator']
            data = form.cleaned_data['data']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            lines = []

            if start_date and end_date:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.filter(
                        date_of_action__range=(start_date, end_date)
                ):
                    if loyalty_card_all_user.card_status == 'ordered':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")
            else:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.all():
                    if loyalty_card_all_user.card_status == 'ordered':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")

            response.writelines(lines)

            return response

    if request.method == 'POST' and category == 'toOrder':
        form = ExportDataToTXTForm(request.POST)
        if form.is_valid():
            separator = form.cleaned_data['separator']
            data = form.cleaned_data['data']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            lines = []

            if start_date and end_date:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.filter(
                        date_of_action__range=(start_date, end_date)
                ):
                    if loyalty_card_all_user.card_status == 'toOrder':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")
            else:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.all():
                    if loyalty_card_all_user.card_status == 'toOrder':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")

            response.writelines(lines)

            return response
    # else:
    #     form = ExportDataToTXTForm()

    if request.method == 'POST' and category == 'deactivated':
        form = ExportDataToTXTForm(request.POST)
        if form.is_valid():
            separator = form.cleaned_data['separator']
            data = form.cleaned_data['data']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            lines = []

            if start_date and end_date:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.filter(
                        date_of_action__range=(start_date, end_date)
                ):
                    if loyalty_card_all_user.card_status == 'deactivated':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")
            else:
                for loyalty_card_all_user in loyalty_card.loyaltyCardStatus.all():
                    if loyalty_card_all_user.card_status == 'deactivated':
                        if 'email' in data:
                            lines.append(f"{loyalty_card_all_user.member.email}{separator}")
                        if 'phone_number' in data:
                            lines.append(f"{loyalty_card_all_user.member.phone_number}{separator}")
                        if 'forename' in data:
                            lines.append(f"{loyalty_card_all_user.member.forename}{separator}")
                        if 'surname' in data:
                            lines.append(f"{loyalty_card_all_user.member.surname}{separator}")
                        if 'member_nr' in data:
                            lines.append(f"{loyalty_card_all_user.member.member_nr}{separator}")
                        if 'card_identity' in data:
                            lines.append(f"{loyalty_card_all_user.card_identity}{separator}")
                        lines.append(f"\n")

            response.writelines(lines)

            return response
    else:
        form = ExportDataToTXTForm()

    return render(
        request,
        'TI_Management_app/loyalty_card/loyalty_card_detail.html',
        {
            'loyalty_card': loyalty_card,
            'status_card_file': status_card_file,
            'status_card_file_a': status_card_file_a,
            'ordered_card_file': ordered_card_file,
            'to_be_picked_up_doc_card_file': to_be_picked_up_doc_card_file,
            'form': form
        }
    )


@login_required
def loyalty_card_add(request):
    if request.method == "POST":
        form = LoyaltyCardForm(request.POST)
        if form.is_valid():
            loyalty_card = form.save(commit=False)
            loyalty_card.author = request.user
            loyalty_card.save()
            messages.success(request, f"Dodano nową kartę lojalnościową {loyalty_card.card_name}!")
            return redirect('TI_Management_app:loyalty_card_list')
    else:
        form = LoyaltyCardForm()
    return render(
        request,
        'TI_Management_app/loyalty_card/loyalty_card_add.html',
        {
            'form': form
        }
    )


@login_required
def loyalty_card_edit(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    if request.method == "POST":
        form = LoyaltyCardForm(request.POST, instance=loyalty_card)
        if form.is_valid():
            loyalty_card = form.save(commit=False)
            loyalty_card.author = request.user
            loyalty_card.save()
            messages.success(request, f"Zaktualizowano {loyalty_card.card_name}!")
            return redirect('TI_Management_app:loyalty_card_detail', pk=loyalty_card.pk, category='none')
    else:
        form = LoyaltyCardForm(instance=loyalty_card)
    return render(
        request,
        'TI_Management_app/loyalty_card/loyalty_card_edit.html',
        {
            'form': form,
            'loyalty_card': loyalty_card
        }
    )


@login_required
def loyalty_card_add_member(request, pk, pk1):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    loyalty_card_member_add = get_object_or_404(MembersZZTI, pk=pk1)
    loyalty_card_validator = CardStatus.objects.all()
    if request.method == "POST":
        form = LoyaltyCardAddMemberForm(request.POST)
        if form.is_valid():
            confirmed_hid = form.cleaned_data['confirmed_hid']
            loyalty_card_member = form.save(commit=False)
            loyalty_card_member.author = request.user
            loyalty_card_member.card = loyalty_card
            loyalty_card_member.member = loyalty_card_member_add
            loyalty_card_member.date_of_action = timezone.now()
            if confirmed_hid:
                loyalty_card_member.confirmed = True
            loyalty_card_member.save()
            messages.success(request, "Dodano nowego Uczestnika!")
            return redirect('TI_Management_app:loyalty_card_detail', pk=loyalty_card.pk, category='none')
    else:
        username = request.user.username
        form = LoyaltyCardAddMemberForm(
            initial={
                'card': loyalty_card,
                'member': loyalty_card_member_add,
                'responsible': username
            }
        )
    return render(
        request,
        'TI_Management_app/loyalty_card/loyalty_card_add_member.html',
        {
            'form': form,
            'loyalty_card': loyalty_card,
            'loyalty_card_member_add': loyalty_card_member_add,
            'loyalty_card_validator': loyalty_card_validator
        }
    )


@login_required
def loyalty_cards_add_file_order(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    if request.method == "POST":
        form = OrderedCardDocumentForm(request.POST, request.FILES)  # , instance = member
        if form.is_valid():
            order_file = form.save(commit=False)
            order_file.author = request.user
            order_file.card = loyalty_card
            order_file.save()
            messages.success(request, f"Dodano dokument {order_file.title}!")
            return redirect('TI_Management_app:loyalty_card_detail', pk=loyalty_card.pk, category='none')
    else:
        username = request.user.username
        form = OrderedCardDocumentForm(
            initial={
                'card': loyalty_card,
                'responsible': username
            }
        )
    return render(
        request,
        'TI_Management_app/loyalty_card/loyalty_cards_add_file_order.html',
        {
            'form': form,
            'loyalty_card': loyalty_card
        }
    )


@login_required
def loyalty_cards_add_file_to_be_picked_up(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    if request.method == "POST":
        form = ToBePickedUpCardDocumentForm(request.POST, request.FILES)  # , instance = member
        if form.is_valid():
            order_file = form.save(commit=False)
            order_file.author = request.user
            order_file.card = loyalty_card
            order_file.save()
            messages.success(request, f"Dodano dokument {order_file.title}!")
            return redirect('TI_Management_app:loyalty_card_detail', pk=loyalty_card.pk, category='none')
    else:
        username = request.user.username
        form = ToBePickedUpCardDocumentForm(
            initial={
                'card': loyalty_card,
                'responsible': username
            }
        )
    return render(
        request,
        'TI_Management_app/loyalty_card/loyalty_cards_add_file_to_be_picked_up.html',
        {
            'form': form,
            'loyalty_card': loyalty_card
        }
    )


# @login_required
# def loyalty_cards_add_member_file_order(request, pk):
#     loyalty_card = get_object_or_404(CardStatus, pk=pk)
#     if request.method == "POST":
#         form = LoyaltyCardsAddMemberFileOrderForm(request.POST, request.FILES, instance=loyalty_card)
#         if form.is_valid():
#             loyalty_card_member = form.save(commit=False)
#             loyalty_card_member.author = request.user
#             loyalty_card_member.file_date = timezone.now()
#             loyalty_card_member.save()
#             messages.success(request, f"Dodano dokument!")
#             return redirect('TI_Management_app:loyalty_card_list')
#     else:
#         form = LoyaltyCardsAddMemberFileOrderForm(instance=loyalty_card)
#     return render(request, 'TI_Management_app/loyalty_cards_add_member_file_order.html',
#                   {'form': form,
#                    'loyalty_card': loyalty_card})


# @login_required
# def loyalty_card_member_file_order_search(request, pk):
#     loyalty_card = get_object_or_404(Cards, pk=pk)
#     loyalty_card_validator = CardStatus.objects.all()
#     if request.method == "POST":
#         searched = request.POST.get('searched', False)
#         loyalty_card_member = MembersZZTI.objects.filter(
#             Q(forename__contains=searched.capitalize()) |
#             Q(surname__contains=searched.capitalize()) |
#             Q(member_nr__contains=searched) |
#             Q(phone_number__contains=searched)
#         )
#         return render(request,
#                       'TI_Management_app/loyalty_card_member_file_order_search.html',
#                       {'searched': searched,
#                        'loyalty_card_member': loyalty_card_member,
#                        'loyalty_card': loyalty_card,
#                        'loyalty_card_validator': loyalty_card_validator})
#     else:
#         return render(request,
#                       'TI_Management_app/loyalty_card_member_file_order_search.html',
#                       {})


# @login_required
# def loyalty_cards_add_member_file_to_be_picked_up(request, pk):
#     loyalty_card = get_object_or_404(CardStatus, pk=pk)
#     if request.method == "POST":
#         form = LoyaltyCardsAddMemberFileToBePickedUpForm(request.POST, request.FILES, instance=loyalty_card)
#         if form.is_valid():
#             loyalty_card_member = form.save(commit=False)
#             loyalty_card_member.author = request.user
#             loyalty_card_member.file_a_date = timezone.now()
#             loyalty_card_member.save()
#             messages.success(request, "Dodano dokument!")
#             return redirect('TI_Management_app:loyalty_card_list')
#     else:
#         form = LoyaltyCardsAddMemberFileToBePickedUpForm(instance=loyalty_card)
#     return render(request, 'TI_Management_app/loyalty_cards_add_member_file_to_be_picked_up.html',
#                   {'form': form,
#                    'loyalty_card': loyalty_card})


# @login_required
# def loyalty_card_member_file_to_be_picked_up_search(request, pk):
#     loyalty_card = get_object_or_404(Cards, pk=pk)
#     loyalty_card_validator = CardStatus.objects.all()
#     if request.method == "POST":
#         searched = request.POST.get('searched', False)
#         loyalty_card_member = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
#                                                          Q(surname__contains=searched.capitalize()) |
#                                                          Q(member_nr__contains=searched) |
#                                                          Q(phone_number__contains=searched))
#         return render(request,
#                       'TI_Management_app/loyalty_card_member_file_to_be_picked_up_search.html',
#                       {'searched': searched,
#                        'loyalty_card_member': loyalty_card_member,
#                        'loyalty_card': loyalty_card,
#                        'loyalty_card_validator': loyalty_card_validator})
#     else:
#         return render(request,
#                       'TI_Management_app/loyalty_card_member_file_to_be_picked_up_search.html',
#                       {})


@login_required
def loyalty_card_delete_member(request, pk, pk1):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    member_loyalty_card = get_object_or_404(CardStatus, pk=pk1)
    loyalty_card.author = request.user
    member_loyalty_card.delete()
    return redirect('TI_Management_app:loyalty_card_detail', pk=loyalty_card.pk, category='none')


# @login_required
# def loyalty_card_delete_all(request, pk):
#     loyalty_card = get_object_or_404(Cards, pk=pk)
#     loyalty_card.author = request.user
#
#     loyalty_card.delete()
#
#     return redirect('TI_Management_app:loyalty_card_detail')


@login_required
def member_loyalty_card_edit(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_loyalty_card = get_object_or_404(CardStatus, pk=pk1)
    # loyalty_card = get_object_or_404(Cards, pk=pk)
    ordered_card_file = OrderedCardDocument.objects.all()
    if request.method == "POST":

        form = CardStatusEditForm(request.POST, request.FILES, instance=member_loyalty_card)
        # form.fields['member'].initial = member
        if form.is_valid():
            confirmed_hid = form.cleaned_data['confirmed_hid']
            member_loyalty_card = form.save(commit=False)
            member_loyalty_card.author = request.user
            member_loyalty_card.member = member
            member_loyalty_card.date_of_action = timezone.now()
            if confirmed_hid:
                member_loyalty_card.confirmed = True
            member_loyalty_card.save()

            messages.success(request, f"Zaktualizowano Kartę Lojalnościową!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = CardStatusEditForm(instance=member_loyalty_card)
        # form.fields['member'].initial = member
    return render(
        request,
        'TI_Management_app/members/member_loyalty_card_edit.html',
        {
            'form': form,
            'member': member,
            'member_loyalty_card': member_loyalty_card,
            'ordered_card_file': ordered_card_file
        }
    )


@login_required
def member_loyalty_card_id_edit(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_loyalty_card = get_object_or_404(CardStatus, pk=pk1)

    if request.method == "POST":
        form = CardStatusCardIDForm(request.POST, instance=member_loyalty_card)
        if form.is_valid():
            member_loyalty_card = form.save(commit=False)
            member_loyalty_card.author = request.user
            member_loyalty_card.member = member
            member_loyalty_card.save()
            messages.success(request, "Zaktualizowano!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = CardStatusCardIDForm(instance=member_loyalty_card)
    return render(
        request, 'TI_Management_app/members/member_loyalty_card_id_edit.html',
        {
            'form': form,
            'member': member,
            'member_loyalty_card': member_loyalty_card
        }
    )


@login_required
def member_loyalty_card_add(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    card_add = get_object_or_404(Cards, pk=pk1)
    if request.method == "POST":
        form = CardStatusForm(request.POST, request.FILES)
        if form.is_valid():
            confirmed_hid = form.cleaned_data['confirmed_hid']
            loyalty_card = form.save(commit=False)
            loyalty_card.author = request.user
            loyalty_card.member = member
            loyalty_card.card = card_add
            loyalty_card.date_of_action = timezone.now()
            if confirmed_hid:
                loyalty_card.confirmed = True

            loyalty_card.save()
            messages.success(request, "Dodano kartę lojalnościową!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        username = request.user.username
        form = CardStatusForm(
            initial={
                'responsible': username,
                'member': member
            }
        )
    return render(
        request,
        'TI_Management_app/members/member_loyalty_card_add.html',
        {
            'form': form,
            'member': member,
            'card_add': card_add
        }
    )


@login_required
def member_loyalty_card_delete(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_loyalty_card = get_object_or_404(CardStatus, pk=pk1)
    member.author = request.user
    # member_loyalty_card.file.delete()
    # member_loyalty_card.card.delete()
    # member_loyalty_card.file_a.delete()
    member_loyalty_card.delete()
    return redirect('TI_Management_app:member_detail', pk=member.pk)


@login_required
def groups_list(request):
    # groups_obj = Groups.objects.all()
    groups_obj = Groups.objects.annotate(member_count=Count('groupsGroup')).order_by('-created_date')

    paginator = Paginator(groups_obj, 5)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/groups/groups_list.html',
        {
            'page': page,
            'groups': groups
        }
    )


@login_required
def group_member_search(request, pk):
    group_available = get_object_or_404(Groups, pk=pk)
    group_validator = GroupsMember.objects.all()
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        group_members = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
                                                   Q(surname__contains=searched.capitalize()) |
                                                   Q(member_nr__contains=searched) |
                                                   Q(phone_number__contains=searched), deactivate=False)

        # members_without_group = MembersZZTI.objects.filter(groupsMember__isnull=True)
        members_without_group = group_members.exclude(groupsMember__group__pk=pk)

        return render(
            request,
            'TI_Management_app/groups/group_member_search.html',
            {
                'searched': searched,
                'group_members': group_members,
                'group_available': group_available,
                'group_validator': group_validator,
                'members_without_group': members_without_group
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/groups/group_member_search.html',
            {}
        )


@login_required
def groups_add(request):
    if request.method == "POST":
        form = GroupsForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.author = request.user
            group.save()
            messages.success(request, f"Dodano nową grupę: {group.group_name}!")
            return redirect('TI_Management_app:groups_list')
    else:
        form = GroupsForm()
    return render(
        request,
        'TI_Management_app/groups/groups_add.html',
        {
            'form': form
        }
    )


@login_required
def groups_edit(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    if request.method == "POST":
        form = GroupsEditForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.author = request.user
            group.save()
            messages.success(request, f"Zaktualizowano grupę {group.group_name}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form = GroupsEditForm(instance=group)
    return render(
        request,
        'TI_Management_app/groups/groups_edit.html',
        {
            'form': form,
            'group': group
        }
    )


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Groups, pk=pk)

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={group}.txt'

    if request.method == "POST":
        form_gender = GroupAddGenderForm(request.POST)

        if form_gender.is_valid():
            gender = form_gender.cleaned_data['gender']
            all_members_ids = MembersZZTI.objects.filter(sex=gender).values_list('id', flat=True)

            group_instance = get_object_or_404(Groups, pk=pk)

            group_members_instances = []
            for member_id in all_members_ids:
                if not GroupsMember.objects.filter(group=group_instance, member_id=member_id).exists():
                    group_members_instance = GroupsMember.objects.create(group=group_instance, member_id=member_id)
                    group_members_instances.append(group_members_instance)

            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form_gender = GroupAddGenderForm()

    if request.method == "POST":
        form_role = GroupAddRoleForm(request.POST)

        if form_role.is_valid():
            role = form_role.cleaned_data['role']
            occupation = form_role.cleaned_data['occupation']
            if role:
                all_members_ids = MembersZZTI.objects.filter(role=role).values_list('id', flat=True)

                group_instance = get_object_or_404(Groups, pk=pk)

                group_members_instances = []
                for member_id in all_members_ids:
                    if not GroupsMember.objects.filter(group=group_instance, member_id=member_id).exists():
                        group_members_instance = GroupsMember.objects.create(group=group_instance, member_id=member_id)
                        group_members_instances.append(group_members_instance)

                return redirect('TI_Management_app:group_detail', pk=group.pk)
            elif occupation:
                all_members_ids = MembersZZTI.objects.filter(occupation=occupation).values_list('id', flat=True)

                group_instance = get_object_or_404(Groups, pk=pk)

                group_members_instances = []
                for member_id in all_members_ids:
                    if not GroupsMember.objects.filter(group=group_instance, member_id=member_id).exists():
                        group_members_instance = GroupsMember.objects.create(group=group_instance, member_id=member_id)
                        group_members_instances.append(group_members_instance)

                return redirect('TI_Management_app:group_detail', pk=group.pk)

    else:
        form_role = GroupAddRoleForm()

    if request.method == 'POST':
        form_export = ExportDataSeparatorGroupForm(request.POST)
        if form_export.is_valid():
            separator = form_export.cleaned_data['separator']
            data = form_export.cleaned_data['data']
            lines = []
            if data == 'email':
                for details in group.groupsGroup.all():
                    lines.append(f"{details.member.email}{separator}")
                response.writelines(lines)
            else:
                for details in group.groupsGroup.all():
                    lines.append(f"{details.member.phone_number}{separator}")
                response.writelines(lines)

            return response
    else:
        form_export = ExportDataSeparatorGroupForm()

    return render(
        request,
        'TI_Management_app/groups/group_detail.html',
        {
            'group': group,
            'form_gender': form_gender,
            'form_role': form_role,
            'form_export': form_export
        }
    )


@login_required
def group_file_edit(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    if request.method == "POST":
        form = GroupFileForm(request.POST, request.FILES)
        if form.is_valid():
            group_file = form.save(commit=False)
            group_file.author = request.user
            group_file.group = group
            group_file.save()
            messages.success(request, f"Dodano plik do grupy {group_file.group}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form = GroupFileForm()
    return render(
        request,
        'TI_Management_app/groups/group_file_edit.html',
        {
            'form': form,
            'group': group
        }
    )


@login_required
def group_file_delete(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    group_file = get_object_or_404(GroupsFile, pk=pk1)

    group.author = request.user
    group_file.file.delete()
    group_file.delete()
    return redirect('TI_Management_app:group_detail', pk=group.pk)


@login_required
def group_notepad_add(request, pk):
    group = get_object_or_404(Groups, pk=pk)

    if request.method == "POST":
        form = GroupNotepadForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sanitized_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            group_notepad = form.save(commit=False)
            group_notepad.author = request.user
            group_notepad.content = sanitized_content
            group_notepad.group = group
            group_notepad.published_date = timezone.now()
            group_notepad.save()
            messages.success(request, f"Dodano notatkę do grupy {group_notepad.group}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        username = request.user.username
        form = GroupNotepadForm(initial={'responsible': username})
    return render(
        request,
        'TI_Management_app/groups/group_notepad_add.html',
        {
            'form': form,
            'group': group
        }
    )


@login_required
def group_notepad_edit(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    notepad = get_object_or_404(GroupsNotepad, pk=pk1)

    if request.method == "POST":
        form = GroupNotepadForm(request.POST, instance=notepad)
        if form.is_valid():
            content = form.cleaned_data['content']
            sanitized_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            group_notepad = form.save(commit=False)
            group_notepad.author = request.user
            group_notepad.content = sanitized_content
            group_notepad.group = group
            group_notepad.published_date = timezone.now()
            group_notepad.save()
            messages.success(request, f"Zaktualizowano notatkę grupy {group_notepad.group}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form = GroupNotepadForm(instance=notepad)
    return render(
        request,
        'TI_Management_app/groups/group_notepad_edit.html',
        {
            'form': form,
            'group': group,
            'notepad': notepad
        }
    )


@login_required
def group_notepad_history(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    notepad = get_object_or_404(GroupsNotepad, pk=pk1)
    group_notepad_history_obj = notepad.history.order_by('-published_date')

    return render(
        request,
        'TI_Management_app/groups/group_notepad_history.html',
        {
            'group': group,
            'group_notepad_history_obj': group_notepad_history_obj,
            'notepad': notepad
        }
    )


@login_required
def group_notepad_history_pdf_advance(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    notepad = get_object_or_404(GroupsNotepad, pk=pk1)
    group_notepad_history_obj = notepad.history.order_by('-published_date')

    html = render_to_string(
        'TI_Management_app/groups/group_notepad_history_pdf_advance.html',
        {
            'group_notepad_history_obj': group_notepad_history_obj,
            'group': group,
            'notepad': notepad
        }
    )
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="notepad_{}.pdf"'.format(group_notepad_history_obj.id)
    response['Content-Disposition'] = f'filename="notepad_{pk1}.pdf"'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/TI_Management_app.css')]
    )
    return response


@login_required
def group_notepad_history_pdf_one_advance(request, pk, pk1, pk2):
    group = get_object_or_404(Groups, pk=pk)
    notepad = get_object_or_404(GroupsNotepad, pk=pk1)
    group_notepad_history_obj = get_object_or_404(notepad.history, pk=pk2)

    html = render_to_string(
        'TI_Management_app/groups/group_notepad_history_pdf_one_advance.html',
        {
            'group_notepad_history_obj': group_notepad_history_obj,
            'group': group,
            'notepad': notepad
        }
    )
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="notepad_{}.pdf"'.format(group_notepad_history_obj.id)
    response['Content-Disposition'] = f'filename="notepad_{pk1}.pdf"'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/TI_Management_app.css')]
    )
    return response


@login_required
def group_notepad_history_pdf(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    notepad = get_object_or_404(GroupsNotepad, pk=pk1)
    group_notepad_history_obj = notepad.history.order_by('-published_date')

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    pdfmetrics.registerFont(
        TTFont(
            'Verdana',
            'TI_Management_app/static/font/verdana.ttf'
        )
    )

    lines = []

    for history in group_notepad_history_obj:
        lines.append(f"Tytuł: {history.title}")
        lines.append(" ")
        lines.append("Opis:")
        lines.append(" ")
        description = wrap(history.content, 65)
        for i in description:
            lines.append(f"{i}")
            lines.append(" ")
        lines.append(f"Data: {history.published_date.isoformat()}")
        lines.append(" ")
        lines.append(f"Ważność: {history.importance}")
        lines.append(" ")
        lines.append(f"Sposób zgłoszenia: {history.method}")
        lines.append(" ")
        lines.append(f"Nadano status: {history.status}")
        lines.append(" ")
        lines.append(f"Prowadzący: {history.responsible}")
        lines.append(" ")
        # if history.file:
        #     lines.append("Plik")
        # lines.append(" ")

        # if history.confirmed:
        #     confirm = "Podpisano: Tak"
        # else:
        #     confirm = "Podpisano: Nie"
        # lines.append(confirm)
        lines.append("--------------------------------------------------------------------")
        lines.append(" ")

    y = 10

    for line in lines:
        c.beginText()
        c.setFont("Verdana", 14)

        y += 10
        c.drawString(10, y, line)
        c.getPageNumber()
        # c.showPage()
        if "-------" in line:
            c.showPage()
            y = 0

    c.save()
    buf.seek(0)

    return FileResponse(
        buf,
        as_attachment=True,
        filename=f"HistoriaKomunikacjiGrupy-{group.group_name}.pdf"
    )


@login_required
def group_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        groups = Groups.objects.filter(Q(group_name__contains=searched.capitalize()))
        return render(
            request,
            'TI_Management_app/groups/group_search.html',
            {
                'searched': searched,
                'groups': groups
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/groups/group_search.html',
            {}
        )


@login_required
def member_group_add(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    group = get_object_or_404(Groups, pk=pk1)
    if request.method == "POST":
        form = GroupsMemberForm(request.POST)
        if form.is_valid():
            group_member = form.save(commit=False)
            group_member.author = request.user
            group_member.member = member
            group_member.group = group
            group_member.save()
            messages.success(request, f"Dodano nowego uczestnika do grupy {group.group_name}!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = GroupsMemberForm()
    return render(
        request,
        'TI_Management_app/members/member_group_add.html',
        {
            'form': form,
            'member': member,
            'group': group
        }
    )


@login_required
def group_add_member(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    member = get_object_or_404(MembersZZTI, pk=pk1)
    if request.method == "POST":
        form = GroupAddMemberForm(request.POST)
        if form.is_valid():
            group_member = form.save(commit=False)
            group_member.author = request.user
            group_member.group = group
            group_member.member = member
            group_member.save()
            messages.success(request, f"Dodano nowego uczestnika do grupy {group.group_name}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form = GroupAddMemberForm(initial={'group': group})
    return render(
        request,
        'TI_Management_app/groups/group_add_member.html',
        {
            'form': form,
            'group': group,
            'member': member
        }
    )


@login_required
def member_group_delete(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_group = get_object_or_404(GroupsMember, pk=pk1)
    member.author = request.user
    member_group.delete()
    return redirect('TI_Management_app:member_detail', pk=member.pk)


@login_required
def group_delete_member(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    member_group = get_object_or_404(GroupsMember, pk=pk1)
    group.author = request.user
    member_group.delete()
    return redirect('TI_Management_app:group_detail', pk=group.pk)


@login_required
def group_delete_all(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    group.author = request.user
    group.delete()
    return redirect('TI_Management_app:groups_list')


@login_required
def member_notepad_add(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = NotepadMemberForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data['content']
            sanitized_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            notepad = form.save(commit=False)
            notepad.author = request.user
            notepad.content = sanitized_content
            notepad.member = member
            notepad.published_date = timezone.now()
            notepad.save()
            messages.success(request, f"Dodano notatkę {notepad.title}!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        username = request.user.username
        form = NotepadMemberForm(initial={'responsible': username})
    return render(
        request,
        'TI_Management_app/members/member_notepad_add.html',
        {
            'form': form,
            'member': member
        }
    )


@login_required
def member_notepad_edit(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    notepad = get_object_or_404(Notepad, pk=pk1)
    if request.method == "POST":
        form = NotepadMemberForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data['content']
            sanitized_content = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            notepad = form.save(commit=False)
            notepad.author = request.user
            notepad.content = sanitized_content
            notepad.member = member
            notepad.published_date = timezone.now()
            notepad.save()
            messages.success(request, f"Zaktualizowano notatkę {notepad.title}!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = NotepadMemberForm(instance=notepad)
    return render(
        request,
        'TI_Management_app/members/member_notepad_edit.html',
        {
            'form': form,
            'member': member,
            'notepad': notepad
        }
    )


@login_required
def member_notepad_history(request, pk, title):
    member = MembersZZTI.objects.get(id=pk)
    member_notepad_history_obj = (member.notepad.filter(
        Q(published_date__lte=timezone.now()) &
        Q(title__contains=title)
    ).order_by('-published_date'))

    return render(
        request,
        'TI_Management_app/members/member_notepad_history.html',
        {
            'member': member,
            'member_notepad_history_obj': member_notepad_history_obj,
            'title': title
        }
    )


@login_required
def member_notepad_history_pdf_advance(request, pk, title):
    member = MembersZZTI.objects.get(id=pk)
    member_notepad_history_obj = member.notepad.filter(
        Q(published_date__lte=timezone.now()) &
        Q(title__contains=title)
    ).order_by('-published_date')

    html = render_to_string(
        'TI_Management_app/members/member_notepad_history_pdf_advance.html',
        {
            'member_notepad_history_obj': member_notepad_history_obj,
            'member': member,
            # 'notepad': notepad
        }
    )
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="notepad_{}.pdf"'.format(group_notepad_history_obj.id)
    response['Content-Disposition'] = f'filename="member_notepad_{pk}.pdf"'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/TI_Management_app.css')]
    )
    return response


@login_required
def member_notepad_history_pdf(request, pk, title):
    member = MembersZZTI.objects.get(id=pk)
    member_notepad_history_obj = member.notepad.filter(
        Q(published_date__lte=timezone.now()) &
        Q(title__contains=title)
    ).order_by('-published_date')

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # c.beginText()
    # c.setFont("Verdana", 14)
    # textob = c.beginText()
    # textob.setTextOrigin(inch, inch)
    pdfmetrics.registerFont(TTFont('Verdana', 'TI_Management_app/static/font/verdana.ttf'))
    # textob.setFont("Verdana", 14)


    # lines = [
    #     "this is line 1",
    #     "this is line 2",
    #     "this is line 3",
    # ]
    lines = []

    for history in member_notepad_history_obj:
        lines.append(f"Tytuł: {history.title}")
        lines.append(" ")
        lines.append("Opis:")
        lines.append(" ")
        description = wrap(history.content, 65)
        for i in description:
            lines.append(f"{i}")
            lines.append(" ")
        lines.append(f"Data: {history.published_date.isoformat()}")
        lines.append(" ")
        lines.append(f"Ważność: {history.importance}")
        lines.append(" ")
        lines.append(f"Sposób zgłoszenia: {history.method}")
        lines.append(" ")
        lines.append(f"Nadano status: {history.status}")
        lines.append(" ")
        lines.append(f"Prowadzący: {history.responsible}")
        lines.append(" ")
        if history.file:
            lines.append("Plik")
        lines.append(" ")

        # lines.append(history.file)
        # lines.append(" ")
        if history.confirmed:
            confirm = "Podpisano: Tak"
        else:
            confirm = "Podpisano: Nie"
        lines.append(confirm)
        lines.append("--------------------------------------------------------------------")
        lines.append(" ")

    y = 10

    for line in lines:
        c.beginText()
        c.setFont("Verdana", 14)

        y += 10
        c.drawString(10, y, line)
        c.getPageNumber()
        # c.showPage()
        if "-------" in line:
            c.showPage()
            y = 0

    c.save()
    buf.seek(0)

    return FileResponse(
        buf,
        as_attachment=True,
        filename=f"HistoriaKomunikacji-{member.forename} {member.surname}.pdf"
    )


@login_required
def member_notepad_delete_all(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member.author = request.user

    notepad_obj = MembersZZTI.objects.get(id=pk)
    # todo  notepad_obj.notepad.file.delete()

    notepad_obj.notepad.all().delete()

    return redirect('TI_Management_app:member_detail', pk=member.pk)


@login_required
def documents_database_category(request):
    categories = DocumentsDatabaseCategory.objects.all()
    if request.method == "POST":
        form = DocumentsDatabaseCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            messages.success(request, f"Dodano nową kategorie {category.title}!")
            return redirect('TI_Management_app:documents_database_category')
    else:
        username = request.user.username
        form = DocumentsDatabaseCategoryForm(
            initial={
                'responsible': username
            }
        )
    return render(
        request,
        'TI_Management_app/documents/documents_database_category.html',
        {
            'form': form,
            'categories': categories
        }
    )


@login_required
def documents_database_category_edit(request, pk):
    category = get_object_or_404(DocumentsDatabaseCategory, pk=pk)

    if request.method == "POST":
        form = DocumentsDatabaseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_form = form.save(commit=False)
            category_form.author = request.user
            category_form.save()
            messages.success(request, f"Zaktualizowano kategorie {category.title}!")
            return redirect('TI_Management_app:documents_database_category')
    else:
        username = request.user.username
        form = DocumentsDatabaseCategoryForm(
            instance=category,
            initial={
                'responsible': username
            }
        )
    return render(
        request,
        'TI_Management_app/documents/documents_database_category_edit.html',
        {
            'form': form,
            'category': category
        }
    )


@login_required
def documents_database_category_delete(request, pk):
    category = get_object_or_404(DocumentsDatabaseCategory, pk=pk)
    category.author = request.user
    # category.documentsDatabaseCategory.file.delete()
    documents = DocumentsDatabase.objects.filter(category=category)

    for document in documents:
        for file_path in document.history.values_list('file', flat=True):
            absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(absolute_file_path):
                os.remove(absolute_file_path)
        # document.file.delete()

    category.delete()
    return redirect('TI_Management_app:documents_database_category')


@login_required
def documents_database(request):
    documents = DocumentsDatabase.objects.all()

    if request.method == "POST":
        form = DocumentsDatabaseForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.author = request.user
            doc.save()
            messages.success(request, f"Dodano nowy dokument {doc.title}!")
            return redirect('TI_Management_app:documents_database')
    else:
        username = request.user.username
        form = DocumentsDatabaseForm(
            initial={
                'responsible': username
            }
        )
    return render(
        request,
        'TI_Management_app/documents/documents_database.html',
        {
            'form': form,
            'documents': documents
        }
    )


@login_required
def documents_database_edit(request, pk):
    document = get_object_or_404(DocumentsDatabase, pk=pk)

    if request.method == "POST":
        form = DocumentsDatabaseForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.author = request.user
            doc.save()
            messages.success(request, f"Zaktualizowano dokument {document.title}!")
            return redirect('TI_Management_app:documents_database')
    else:
        username = request.user.username
        form = DocumentsDatabaseForm(
            instance=document,
            initial={
                'responsible': username
            }
        )
    return render(
        request,
        'TI_Management_app/documents/documents_database_edit.html',
        {
            'form': form,
            'document': document
        }
    )


@login_required
def documents_database_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        documents = DocumentsDatabase.objects.filter(
            Q(title__contains=searched.capitalize()) |
            Q(file__contains=searched.capitalize()) |
            Q(category__title__contains=searched.capitalize())
        )
        return render(
            request,
            'TI_Management_app/documents/documents_database_search.html',
            {
                'searched': searched,
                'documents': documents
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/documents/documents_database_search.html',
            {}
        )


@login_required
def documents_database_delete(request, pk):
    documents = get_object_or_404(DocumentsDatabase, pk=pk)
    documents.author = request.user

    for file_path in documents.history.values_list('file', flat=True):
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if os.path.exists(absolute_file_path):
            os.remove(absolute_file_path)

    # documents.file.delete()
    documents.delete()

    return redirect('TI_Management_app:documents_database')


@login_required
def relief_figure_add(request):
    all_relief = Relief.objects.all().order_by('-created_date')
    if request.method == "POST":
        form = ReliefFigureForm(request.POST)
        if form.is_valid():
            figure = form.cleaned_data['figure']
            grace = form.cleaned_data['grace']
            figure = round(float(figure), 2)
            grace = int(grace)
            relief = form.save(commit=False)
            relief.author = request.user
            relief.figure = figure
            relief.grace = grace
            relief.save()
            messages.success(request, f"Dodano zapomogę {relief.title}!")
            return redirect('TI_Management_app:relief_figure_add')
    else:
        form = ReliefFigureForm()
    return render(
        request,
        'TI_Management_app/finance/relief_figure_add.html',
        {
            'form': form,
            'all_relief': all_relief
        }
    )


@login_required
def relief_figure_edit(request, pk):
    one_relief = get_object_or_404(Relief, pk=pk)
    if request.method == "POST":
        form = ReliefFigureForm(request.POST, instance=one_relief)
        if form.is_valid():
            figure = form.cleaned_data['figure']
            grace = form.cleaned_data['grace']
            figure = round(float(figure), 2)
            grace = int(grace)
            relief = form.save(commit=False)
            relief.author = request.user
            relief.figure = figure
            relief.grace = grace
            relief.save()
            messages.success(request, f"Zaktualizowano zapomogę {relief.title}!")
            return redirect('TI_Management_app:relief_figure_add')
    else:
        form = ReliefFigureForm(instance=one_relief)
    return render(
        request,
        'TI_Management_app/finance/relief_figure_edit.html',
        {
            'form': form,
            'one_relief': one_relief
        }
    )


@login_required
def relief_figure_delete(request, pk):
    one_relief = get_object_or_404(Relief, pk=pk)
    one_relief.author = request.user
    one_relief.delete()
    # one_relief.history.delete()
    return redirect('TI_Management_app:relief_figure_add')


@login_required
def relation_register_relief_add(request):
    all_relation_register_relief = RelationRegisterRelief.objects.all().order_by('-created_date')
    if request.method == "POST":
        form = RelationRegisterReliefForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.author = request.user
            relation.save()
            messages.success(request, f"Dodano nową relacje {relation.title}!")
            return redirect('TI_Management_app:relation_register_relief_add')
    else:
        form = RelationRegisterReliefForm()
    return render(
        request,
        'TI_Management_app/finance/relation_register_relief_add.html',
        {
            'form': form,
            'all_relation_register_relief': all_relation_register_relief
        }
    )


@login_required
def relation_register_relief_edit(request, pk):
    one_relation_register_relief = get_object_or_404(RelationRegisterRelief, pk=pk)
    if request.method == "POST":
        form = RelationRegisterReliefForm(request.POST, instance=one_relation_register_relief)
        if form.is_valid():
            one_relation = form.save(commit=False)
            one_relation.author = request.user
            one_relation.save()
            messages.success(request, f"Zaktualizowano relacje {one_relation.title}!")
            return redirect('TI_Management_app:relation_register_relief_add')
    else:
        form = RelationRegisterReliefForm(instance=one_relation_register_relief)
    return render(
        request,
        'TI_Management_app/finance/relation_register_relief_edit.html',
        {
            'form': form,
            'one_relation_register_relief': one_relation_register_relief
        }
    )


@login_required
def relation_register_relief_delete(request, pk):
    one_relation = get_object_or_404(RelationRegisterRelief, pk=pk)
    one_relation.author = request.user
    one_relation.delete()
    # one_relation.history.delete()
    return redirect('TI_Management_app:relation_register_relief_add')


@login_required
def register_relief_step_one(request):
    relief_process_ongoing = RegisterRelief.objects.filter(complete=False).order_by('-created_date')

    return render(
        request,
        'TI_Management_app/finance/register_relief_step_one.html',
        {
            'relief_process_ongoing': relief_process_ongoing
        }
    )


@login_required
def register_relief_step_one_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        members = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
                                             Q(surname__contains=searched.capitalize()) |
                                             Q(member_nr__contains=searched) |
                                             Q(phone_number__contains=searched),
                                             card__isnull=False,
                                             deactivate=False)
        return render(
            request,
            'TI_Management_app/finance/register_relief_step_one_search.html',
            {'searched': searched,
             'members': members}
        )
    else:
        return render(
            request,
            'TI_Management_app/finance/register_relief_step_one_search.html',
            {}
        )


@login_required
def register_relief_step_two(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberEditReliefForm(request.POST, instance=member)
        if form.is_valid():
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']

            address_member = form.save(commit=False)
            address_member.author = request.user
            address_member.city = city.title()
            address_member.street = street.title()
            address_member.save()
            messages.success(
                request,
                f"1/4 - Zaktualizowano adres {member.forename} {member.surname}!"
            )
            return redirect('TI_Management_app:register_relief_step_three', pk=member.pk)
    else:
        form = MemberEditReliefForm(instance=member)
    return render(
        request,
        'TI_Management_app/finance/register_relief_step_two.html',
        {
            'form': form,
            'member': member
        }
    )


@login_required
def get_relief_details(request):
    relief_id = request.GET.get('relief_id')
    if relief_id:
        try:
            relief = Relief.objects.get(pk=relief_id)
            author_name = relief.author.username if relief.author else "Unknown"
            author_email = relief.author.email if relief.author else "Unknown"
            figure = relief.figure if relief.figure else "Unknown"
            grace = relief.grace if relief.grace else "Unknown"
            data = {
                'author_name': author_name,
                'author_email': author_email,
                'figure': figure,
                'grace': grace
            }
            return JsonResponse(data)
        except Relief.DoesNotExist:
            pass
    return JsonResponse({'error': 'Relief not found'}, status=400)


@login_required
def register_relief_step_three(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    all_relief = Relief.objects.all().order_by('-created_date')
    all_relation = RelationRegisterRelief.objects.all().order_by('-created_date')

    if request.method == "POST":
        form = RegisterReliefForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']

            sanitized_description = bleach.clean(reason, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
            register_relife = form.save(commit=False)
            register_relife.author = request.user
            register_relife.reason = sanitized_description
            register_relife.member = member
            register_relife.save()
            messages.success(request, "2/4 - Walidacja karencji przebiegła pomyślnie!")
            return redirect('TI_Management_app:register_relief_step_four', pk=register_relife.pk)
    else:
        form = RegisterReliefForm()
    return render(
        request,
        'TI_Management_app/finance/register_relief_step_three.html',
        {
            'form': form,
            'member': member,
            'all_relief': all_relief,
            'all_relation': all_relation
        }
    )


@login_required
def register_relief_step_four(request, pk):
    one_registered_relife = get_object_or_404(RegisterRelief, pk=pk)

    if request.method == "POST":
        form = FileRegisterReliefForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_files = request.FILES.getlist('file')
            for uploaded_file in uploaded_files:
                FileRegisterRelief.objects.create(
                    author=request.user,
                    register_relief=one_registered_relife,
                    title=uploaded_file.name,
                    file=uploaded_file
                )

            messages.success(request, "3/4 - Dodano domumenty do zapomogi!")
            return redirect('TI_Management_app:register_relief_step_five', pk=one_registered_relife.pk)
    else:
        form = FileRegisterReliefForm()
    return render(
        request,
        'TI_Management_app/finance/register_relief_step_four.html',
        {
            'form': form,
            # 'member': member,
            'one_registered_relife': one_registered_relife
        }
    )


# @login_required
# def register_relief_step_five(request, pk):
#     one_registered_relife = get_object_or_404(RegisterRelief, pk=pk)
#     member = one_registered_relife.member
#
#     if request.method == "POST":
#         form = CardRegisterReliefForm(request.POST, instance=member)
#         # form = CardRegisterReliefForm(request.POST)
#
#         if form.is_valid():
#             # if member.card is form.cleaned_data['card']:
#             if RegisterRelief.objects.filter(member__card=form.cleaned_data['card']).exists():
#
#                 member_card = str(member.card)
#
#                 is_correct = check_password(form.cleaned_data['card'], member_card)
#
#                 # if form.cleaned_data['card'] == one_registered_relife.member.card:
#                 if is_correct:
#                     one_registered_relife.complete = True
#                     one_registered_relife.date_of_signed_by_the_applicant = timezone.now()
#                     one_registered_relife.save()
#
#                     messages.success(request, "4/4 - Podpisano!")
#                     return redirect('TI_Management_app:register_relief_valid', pk=one_registered_relife.pk)
#     else:
#         # form = CardRegisterReliefForm(instance=member)
#         form = CardRegisterReliefForm()
#     return render(
#         request,
#         'TI_Management_app/finance/register_relief_step_five.html',
#         {
#             'form': form,
#             'one_registered_relife': one_registered_relife
#         }
#     )
@login_required
def register_relief_step_five(request, pk):
    one_registered_relife = get_object_or_404(RegisterRelief, pk=pk)
    member = one_registered_relife.member

    if request.method == "POST":
        form = CardRegisterReliefForm(request.POST, instance=member)

        if form.is_valid():
            # Verify if the card is already registered to a member
            # if RegisterRelief.objects.filter(member__card=form.cleaned_data['card']).exists():
            member_card = str(member.card)

            # Check if the provided card matches the stored card
            is_correct = check_password(form.cleaned_data['card'], member_card)

            if is_correct:
                one_registered_relife.complete = True
                one_registered_relife.date_of_signed_by_the_applicant = timezone.now()
                one_registered_relife.save()

                messages.success(request, "4/4 - Podpisano!")
                return redirect('TI_Management_app:register_relief_valid', pk=one_registered_relife.pk)
            # else:
            #     form.add_error('card', 'Karta nie jest zarejestrowana dla żadnego członka.')
    else:
        form = CardRegisterReliefForm()

    return render(
        request,
        'TI_Management_app/finance/register_relief_step_five.html',
        {
            'form': form,
            'one_registered_relife': one_registered_relife
        }
    )


@login_required
def register_relief_valid(request, pk):
    validation_register_relief = get_object_or_404(RegisterRelief, pk=pk)

    return render(
        request,
        'TI_Management_app/finance/register_relief_valid.html',
        {
            'validation_register_relief': validation_register_relief
        }
    )


@login_required
def relief_status_list(request):
    relief_list = RegisterRelief.objects.filter(complete=True).order_by('-created_date')
    active_admin = User.objects.filter(is_active=True)

    paginator = Paginator(relief_list, 50)
    page = request.GET.get('page')
    try:
        relief = paginator.page(page)
    except PageNotAnInteger:
        relief = paginator.page(1)
    except EmptyPage:
        relief = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/finance/relief_status_list.html',
        {
            'page': page,
            'relief': relief,
            'active_admin': active_admin
        }
    )


@login_required
def relief_status_list_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        members = RegisterRelief.objects.filter(
            Q(member__forename__contains=searched.capitalize()) |
            Q(member__surname__contains=searched.capitalize()) |
            Q(member__member_nr__contains=searched) |
            Q(member__phone_number__contains=searched),
            member__card__isnull=False,
            member__deactivate=False,
            complete=True
        )
        return render(
            request,
            'TI_Management_app/finance/relief_status_list_search.html',
            {
                'searched': searched,
                'members': members
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/finance/relief_status_list_search.html',
            {}
        )


# @login_required
# def relief_status_to_be_signed(request, pk):
#     relief_to_be_signed = get_object_or_404(RegisterRelief, pk=pk)
#
#     if request.method == "POST":
#         form = SignatureReliefForm(relief_to_be_signed, request.POST)
#         form_confirmation = PaymentConfirmationReliefForm(request.POST)
#         if form.is_valid():
#             card = form.cleaned_data['card']
#             member = MembersZZTI.objects.filter(card=card).first()
#             if member and User.objects.filter(username=member.member_nr, is_active=True).exists():
#                 existing_signature = relief_to_be_signed.registerReliefSignatureRelief.filter(member=member).exists()
#
#                 if not existing_signature:
#
#                     signature = SignatureRelief.objects.create(
#                         author=request.user,
#                         member=member,
#                         register_relief=relief_to_be_signed,
#                         signature=True
#                     )
#                     signature.save()
#
#                     messages.success(
#                         request,
#                         f"Dodano podpis {member.forename} {member.surname} {member.member_nr}!"
#                     )
#                     return redirect('TI_Management_app:relief_status_to_be_signed', pk=relief_to_be_signed.pk)
#
#         if form_confirmation.is_valid():
#             confirmation = form_confirmation.cleaned_data['payment_confirmation']
#             if confirmation is True:
#
#                 relief_to_be_signed.agreement = True
#                 relief_to_be_signed.payment_confirmation = True
#                 relief_to_be_signed.date_of_payment_confirmation = timezone.now()
#                 relief_to_be_signed.save()
#
#                 messages.success(
#                     request,
#                     f"Potwierdzenie wypłaty"
#                 )
#                 return redirect('TI_Management_app:relief_status_to_be_signed', pk=relief_to_be_signed.pk)
#             else:
#                 messages.error(
#                     request,
#                     "Error!"
#                 )
#
#     else:
#         form = SignatureReliefForm(relief_to_be_signed)
#         form_confirmation = PaymentConfirmationReliefForm()
#
#     return render(
#         request,
#         'TI_Management_app/finance/relief_status_to_be_signed.html',
#         {
#             'form': form,
#             'form_confirmation': form_confirmation,
#             'relief_to_be_signed': relief_to_be_signed
#         }
#     )
@login_required
def relief_status_to_be_signed(request, pk):
    relief_to_be_signed = get_object_or_404(RegisterRelief, pk=pk)

    if request.method == "POST":
        form = SignatureReliefForm(relief_to_be_signed, request.POST)
        form_confirmation = PaymentConfirmationReliefForm(request.POST)
        if form.is_valid():
            card = form.cleaned_data['card']
            member = None
            for potential_member in MembersZZTI.objects.all():
                if check_password(card, potential_member.card):
                    member = potential_member
                    break

            if member and User.objects.filter(username=member.member_nr, is_active=True).exists():
                existing_signature = relief_to_be_signed.registerReliefSignatureRelief.filter(member=member).exists()

                if not existing_signature:
                    signature = SignatureRelief.objects.create(
                        author=request.user,
                        member=member,
                        register_relief=relief_to_be_signed,
                        signature=True
                    )
                    signature.save()

                    messages.success(
                        request,
                        f"Dodano podpis {member.forename} {member.surname} {member.member_nr}!"
                    )
                    return redirect('TI_Management_app:relief_status_to_be_signed', pk=relief_to_be_signed.pk)

        if form_confirmation.is_valid():
            confirmation = form_confirmation.cleaned_data['payment_confirmation']
            if confirmation is True:
                relief_to_be_signed.agreement = True
                relief_to_be_signed.payment_confirmation = True
                relief_to_be_signed.date_of_payment_confirmation = timezone.now()
                relief_to_be_signed.save()

                messages.success(
                    request,
                    f"Potwierdzenie wypłaty"
                )
                return redirect('TI_Management_app:relief_status_to_be_signed', pk=relief_to_be_signed.pk)
            else:
                messages.error(
                    request,
                    "Error!"
                )

    else:
        form = SignatureReliefForm(relief_to_be_signed)
        form_confirmation = PaymentConfirmationReliefForm()

    return render(
        request,
        'TI_Management_app/finance/relief_status_to_be_signed.html',
        {
            'form': form,
            'form_confirmation': form_confirmation,
            'relief_to_be_signed': relief_to_be_signed
        }
    )


@login_required
def relief_status_to_be_signed_pdf_advance(request, pk):
    relief_to_be_signed = get_object_or_404(RegisterRelief, pk=pk)

    html = render_to_string(
        'TI_Management_app/finance/relief_status_to_be_signed_pdf_advance.html',
        {
            'relief_to_be_signed': relief_to_be_signed,
        }
    )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="relief_{pk}.pdf"'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/TI_Management_app.css')]
    )
    return response


@login_required
def relief_confirmed_list(request):
    relief_list = RegisterRelief.objects.filter(payment_confirmation=True).order_by('-created_date')

    if request.method == "POST":
        form = ConfirmedReliefTimeRangeForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            relief_list = RegisterRelief.objects.filter(
                payment_confirmation=True,
                date_of_payment_confirmation__range=(start_date, end_date)
            ).order_by('-created_date')

            messages.success(request, f"Wybrano zakres {start_date} - {end_date}")
            # return redirect('TI_Management_app:relief_confirmed_list')
    else:
        form = ConfirmedReliefTimeRangeForm()

    paginator = Paginator(relief_list, 50)
    page = request.GET.get('page')
    try:
        relief = paginator.page(page)
    except PageNotAnInteger:
        relief = paginator.page(1)
    except EmptyPage:
        relief = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/finance/relief_confirmed_list.html',
        {
            'page': page,
            'relief': relief,
            'form': form
        }
    )


@login_required
def relief_confirmed_list_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        members = RegisterRelief.objects.filter(
            Q(member__forename__contains=searched.capitalize()) |
            Q(member__surname__contains=searched.capitalize()) |
            Q(member__member_nr__contains=searched) |
            Q(member__phone_number__contains=searched),
            member__card__isnull=False,
            complete=True,
            payment_confirmation=True
        )
        return render(
            request,
            'TI_Management_app/finance/relief_confirmed_list_search.html',
            {
                'searched': searched,
                'members': members
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/finance/relief_confirmed_list_search.html',
            {}
        )


@login_required
def scholarships_list(request):
    scholarships_all = Scholarships.objects.order_by('-created_date')

    paginator = Paginator(scholarships_all, 50)
    page = request.GET.get('page')
    try:
        scholarships = paginator.page(page)
    except PageNotAnInteger:
        scholarships = paginator.page(1)
    except EmptyPage:
        scholarships = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/finance/scholarships_list.html',
        {
            'page': page,
            'scholarships': scholarships
        }
    )


@login_required
def scholarships_list_search(request):

    if request.method == "POST":
        searched = request.POST.get('searched', False)
        members = Scholarships.objects.filter(
            Q(member__forename__contains=searched.capitalize()) |
            Q(member__surname__contains=searched.capitalize()) |
            Q(member__member_nr__contains=searched) |
            Q(member__phone_number__contains=searched)
        )
        return render(
            request,
            'TI_Management_app/finance/scholarships_list_search.html',
            {
                'searched': searched,
                'members': members
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/finance/scholarships_list_search.html',
            {}
        )


@login_required
# @require_POST #  I have to start before using the slug
def scholarships_average_salary_add(request):
    scholarships_average_salary_list = AverageSalary.objects.order_by('-created_date')

    if request.method == "POST":
        form = AverageSalaryForm(request.POST)
        if form.is_valid():
            salary = form.save(commit=False)
            salary.author = request.user
            salary.save()

            messages.success(request, f"Dodano przeciętne wynagrodzenie {salary.title}!")
            return redirect('TI_Management_app:scholarships_average_salary_add')
    else:
        form = AverageSalaryForm()

    paginator = Paginator(scholarships_average_salary_list, 50)
    page = request.GET.get('page')
    try:
        average_salary = paginator.page(page)
    except PageNotAnInteger:
        average_salary = paginator.page(1)
    except EmptyPage:
        average_salary = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/finance/scholarships_average_salary_add.html',
        {
            'form': form,
            'page': page,
            'average_salary': average_salary
        }
    )


@login_required
# @require_POST
def scholarships_add(request, pk):

    # scholarship_rate = models.FloatField(null=False, blank=False)
    # confirmation_of_scholarship = models.BooleanField(default=False)

    member = get_object_or_404(MembersZZTI, pk=pk)
    scholarships_average_salary_list = AverageSalary.objects.latest('id')

    if request.method == "POST":
        form = ScholarshipsForm(member, request.POST, request.FILES)

        # scholarship_rate_calculation =

        if form.is_valid():
            scholarship = form.save(commit=False)
            scholarship.author = request.user
            scholarship.member = member
            scholarship.average_salary = scholarships_average_salary_list
            # scholarship.scholarship_rate = scholarship_rate_calculation
            scholarship.save()
            messages.success(request, f"Dodano stypendium \"{scholarship.title}\"")
            return redirect('TI_Management_app:scholarships_list')
    else:
        form = ScholarshipsForm(member)
    return render(
        request,
        'TI_Management_app/finance/scholarships_add.html',
        {
            'form': form,
            'scholarships_average_salary_list': scholarships_average_salary_list,
            'member': member
        }
    )


@login_required
def scholarships_add_search(request):
    # verification whether the record is added in AvaregeSalary
    try:
        scholarships_average_salary_list = AverageSalary.objects.latest('id')
        flag = True
    except ObjectDoesNotExist:
        scholarships_average_salary_list = 0.00
        flag = False

    if request.method == "POST":
        searched = request.POST.get('searched', False)
        members = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
                                             Q(surname__contains=searched.capitalize()) |
                                             Q(member_nr__contains=searched) |
                                             Q(phone_number__contains=searched),
                                             card__isnull=False,
                                             deactivate=False)

        return render(
            request,
            'TI_Management_app/finance/scholarships_add_search.html',
            {
                'searched': searched,
                'flag': flag,
                'members': members
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/finance/scholarships_add_search.html',
            {
                'flag': flag,
                'scholarships_average_salary_list': scholarships_average_salary_list
            }
        )


@login_required
# @require_POST
def scholarships_edit(request, pk):
    one_scholarship = get_object_or_404(Scholarships, pk=pk)

    # formatted_date = one_scholarship.seminary_start_date.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S")
    formatted_seminary_start_date = one_scholarship.seminary_start_date.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d")
    formatted_seminary_end_date = one_scholarship.seminary_end_date.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d")

    member_earnings_pct = (one_scholarship.member_salary / one_scholarship.average_salary.salary) * 100

    if request.method == "POST":
        form = ScholarshipsEditForm(request.POST, request.FILES, instance=one_scholarship)
        if form.is_valid():
            one_scholarship_update = form.save(commit=False)
            one_scholarship_update.author = request.user
            one_scholarship_update.member = one_scholarship.member
            one_scholarship_update.confirmation_date = timezone.now()
            one_scholarship_update.save()
            messages.success(request, f"Potwierdzono  {one_scholarship_update.title}!")
            return redirect('TI_Management_app:scholarships_list')
    else:
        form = ScholarshipsEditForm(instance=one_scholarship)
    return render(
        request,
        'TI_Management_app/finance/scholarships_edit.html',
        {
            'form': form,
            'one_scholarship': one_scholarship,
            'formatted_seminary_start_date': formatted_seminary_start_date,
            'formatted_seminary_end_date': formatted_seminary_end_date,
            'member_earnings_pct': member_earnings_pct
        }
    )


@login_required
# @require_POST
def scholarships_delete(request, pk):
    scholarship = get_object_or_404(Scholarships, pk=pk)
    scholarship.author = request.user
    scholarship.file_scholarship_application.delete()
    scholarship.file_scanned_confirmation_of_payment_for_studies.delete()
    scholarship.file_declaration_of_income.delete()
    scholarship.file_resolution_consenting.delete()
    scholarship.file_document_confirming_of_the_semester.delete()
    scholarship.file_university_regulations_of_the_grading_scale.delete()
    scholarship.delete()

    return redirect('TI_Management_app:scholarships_list')


@ajax_required
@login_required
def get_member_details(request, member_nr):
    try:
        member = get_object_or_404(MembersZZTI, member_nr=member_nr, card__isnull=False, deactivate=False)
        member_details = {
            'first_name': member.forename,
            # 'last_name': member.surname,
            # 'email': member.email,
            # Add more fields as needed
        }
        return JsonResponse(member_details)
    except MembersZZTI.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
# @require_POST
def finance_file_add(request):
    kind_of_finance_document = KindOfFinanceDocument.objects.all()
    doc_database = DocumentsDatabase.objects.filter(Q(category__title__icontains='Uchwały'))
    expense_names = KindOfFinanceExpense.objects.all()
    members = MembersZZTI.objects.all().order_by('member_nr')

    if request.method == "POST":
        form_kind_of_document = KindOfFinanceDocumentForm(request.POST)
        form_file_finance = FileFinanceForm(request.POST, request.FILES)
        form_kind_of_expense = KindOfFinanceExpenseForm(request.POST)

        if all([form_kind_of_document.is_valid(), form_file_finance.is_valid(), form_kind_of_expense.is_valid()]):
            document_title = form_kind_of_document.cleaned_data['title_doc']
            expense_title = form_kind_of_expense.cleaned_data['title_expense']
            member_nr = form_file_finance.cleaned_data['member_nr']
            psychologist = form_file_finance.cleaned_data['psychologist']
            title = f"{document_title} - {expense_title}"
            description = form_file_finance.cleaned_data['description']
            sanitized_description = bleach.clean(description, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

            if not KindOfFinanceDocument.objects.filter(title_doc=document_title).exists():
                finance_document_kind = form_kind_of_document.save(commit=False)
                finance_document_kind.title = document_title
                finance_document_kind.author = request.user
                finance_document_kind.save()

            if not KindOfFinanceExpense.objects.filter(title_expense=expense_title).exists():
                kind_of_expense = form_kind_of_expense.save(commit=False)
                kind_of_expense.title = expense_title
                kind_of_expense.author = request.user
                kind_of_expense.save()

            finance_file = form_file_finance.save(commit=False)
            finance_file.author = request.user
            finance_file.title = title
            finance_file.description = sanitized_description
            # finance_file.type_of_document = KindOfFinanceDocument.objects.get(title_doc=document_title)
            finance_file.type_of_document = KindOfFinanceDocument.objects.filter(title_doc=document_title).latest('id')
            # finance_file.expense_name = KindOfFinanceExpense.objects.get(title_expense=expense_title)
            finance_file.expense_name = KindOfFinanceExpense.objects.filter(title_expense=expense_title).latest('id')
            # finance_file.member = MembersZZTI.objects.get(member_nr=member_nr)
            if psychologist is True and MembersZZTI.objects.filter(member_nr=member_nr).exists():
                finance_file.member = MembersZZTI.objects.filter(member_nr=member_nr).latest('id')
            finance_file.save()

            messages.success(request, f"Dodano dokument księgowy - {title}")
            return redirect('TI_Management_app:finance_list')
    else:
        form_kind_of_document = KindOfFinanceDocumentForm()
        form_file_finance = FileFinanceForm()
        form_kind_of_expense = KindOfFinanceExpenseForm()
    return render(
        request,
        'TI_Management_app/finance/finance_file_add.html',
        {
            'form_kind_of_document': form_kind_of_document,
            'form_file_finance': form_file_finance,
            'form_kind_of_expense': form_kind_of_expense,
            'kind_of_finance_document': kind_of_finance_document,
            'doc_database': doc_database,
            'expense_names': expense_names,
            'members': members
        }
    )


@login_required
def finance_list(request):
    finance_obj = FileFinance.objects.all().order_by('-payment_date')
    register_relief_obj = RegisterRelief.objects.filter(payment_confirmation=True).order_by('-date_of_payment_confirmation')
    scholarships_obj = Scholarships.objects.filter(confirmation_of_scholarship=True).order_by('-confirmation_date')

    combined_list = sorted(
        chain(finance_obj, register_relief_obj, scholarships_obj),
        key=lambda obj: obj.payment_date if hasattr(obj, 'payment_date') else obj.date_of_payment_confirmation if hasattr(obj, 'date_of_payment_confirmation') else obj.confirmation_date,
        reverse=True
    )

    grouped_by_year = defaultdict(list)
    for obj in combined_list:
        date_field = obj.payment_date if hasattr(obj, 'payment_date') else obj.date_of_payment_confirmation if hasattr(obj, 'date_of_payment_confirmation') else obj.confirmation_date
        year = date_field.year
        grouped_by_year[year].append(obj)

    summarized_data = []

    for year, entries in grouped_by_year.items():
        finance_figure = sum(Decimal(getattr(entry, 'figure', 0)) for entry in entries if isinstance(entry, FileFinance))
        finance_quantity = sum(getattr(entry, 'quantity', 0) for entry in entries if isinstance(entry, FileFinance))
        scholarship_figure = sum(Decimal(getattr(entry, 'scholarship_rate', 0)) for entry in entries if isinstance(entry, Scholarships))
        relief_figure = sum(Decimal(getattr(entry, 'figure', 0)) for entry in entries if isinstance(entry, RegisterRelief))

        total_expense = finance_figure + scholarship_figure + relief_figure

        summarized_data.append((year, entries, finance_figure, scholarship_figure, relief_figure, total_expense, finance_quantity))

    sorted_years = sorted(summarized_data, key=lambda x: x[0], reverse=True)

    years_list = [year for year, _, _, _, _, _, _ in sorted_years]

    bank_statements_by_year = BankStatement.objects.filter(year_bank_statement__in=years_list).values('year_bank_statement').annotate(total_income=Sum('income_bank_statement')).order_by('-year_bank_statement')

    bank_income_by_year = {entry['year_bank_statement']: entry['total_income'] for entry in bank_statements_by_year}

    sorted_years_with_income = []
    for year, entries, finance_figure, scholarship_figure, relief_figure, total_expense, finance_quantity in sorted_years:
        total_income = bank_income_by_year.get(year, Decimal(0))
        sorted_years_with_income.append((year, entries, finance_figure, scholarship_figure, relief_figure, total_expense, total_income, finance_quantity))

    paginator = Paginator(sorted_years_with_income, 1)  # One year per page
    page = request.GET.get('page')
    try:
        years = paginator.page(page)
    except PageNotAnInteger:
        years = paginator.page(1)
    except EmptyPage:
        years = paginator.page(paginator.num_pages)

    latest_ids_subquery = BankStatement.objects.filter(
        year_bank_statement=OuterRef('year_bank_statement')
    ).values('year_bank_statement').annotate(
        max_id=Max('id')
    ).values('max_id')

    bank_statements = BankStatement.objects.filter(
        id__in=Subquery(latest_ids_subquery)
    ).filter(year_bank_statement__in=years_list).order_by('-year_bank_statement')

    latest_bank_statements = BankStatement.objects.filter(
        id__in=Subquery(latest_ids_subquery)
    ).values('year_bank_statement', 'income_bank_statement')
    latest_income_by_year = {entry['year_bank_statement']: entry['income_bank_statement'] for entry in
                             latest_bank_statements}

    all_years = [entry[0] for entry in sorted_years]

    return render(
        request,
        'TI_Management_app/finance/finance_list.html',
        {
            'years': years,
            'page': page,
            'bank_statements': bank_statements,
            'latest_income': latest_income_by_year,
            'all_years': all_years
        }
    )

# @login_required
# def finance_list(request):
#     finance_obj = FileFinance.objects.all().order_by('-payment_date')
#
#     register_relief_obj = RegisterRelief.objects.filter(payment_confirmation=True).order_by('-date_of_payment_confirmation')
#
#     scholarships_obj = Scholarships.objects.filter(confirmation_of_scholarship=True).order_by('-confirmation_date')
#
#     combined_list = sorted(
#         chain(finance_obj, register_relief_obj, scholarships_obj),
#         key=lambda obj: obj.payment_date if hasattr(obj, 'payment_date') else obj.date_of_payment_confirmation if hasattr(obj, 'date_of_payment_confirmation') else obj.confirmation_date,
#         reverse=True
#     )
#
#     grouped_by_year = defaultdict(list)
#     for obj in combined_list:
#         date_field = obj.payment_date if hasattr(obj, 'payment_date') else obj.date_of_payment_confirmation if hasattr(obj, 'date_of_payment_confirmation') else obj.confirmation_date
#         year = date_field.year
#         grouped_by_year[year].append(obj)
#
#     summarized_data = []
#
#     for year, entries in grouped_by_year.items():
#         finance_figure = sum(Decimal(getattr(entry, 'figure', 0)) for entry in entries if isinstance(entry, FileFinance))
#         scholarship_figure = sum(Decimal(getattr(entry, 'scholarship_rate', 0)) for entry in entries if isinstance(entry, Scholarships))
#         relief_figure = sum(Decimal(getattr(entry, 'figure', 0)) for entry in entries if isinstance(entry, RegisterRelief))
#
#         total_expense = finance_figure + scholarship_figure + relief_figure
#
#         summarized_data.append((year, entries, finance_figure, scholarship_figure, relief_figure, total_expense))
#
#     sorted_years = sorted(summarized_data, key=lambda x: x[0], reverse=True)
#
#     years_list = [year for year, _, _, _, _, _ in sorted_years]
#
#     bank_statements_by_year = BankStatement.objects.filter(year_bank_statement__in=years_list).values('year_bank_statement').annotate(total_income=Sum('income_bank_statement')).order_by('-year_bank_statement')
#
#     bank_income_by_year = {entry['year_bank_statement']: entry['total_income'] for entry in bank_statements_by_year}
#
#     sorted_years_with_income = []
#     for year, entries, finance_figure, scholarship_figure, relief_figure, total_expense in sorted_years:
#         total_income = bank_income_by_year.get(year, Decimal(0))
#         sorted_years_with_income.append((year, entries, finance_figure, scholarship_figure, relief_figure, total_expense, total_income))
#
#     paginator = Paginator(sorted_years_with_income, 1)  # One year per page
#     page = request.GET.get('page')
#     try:
#         years = paginator.page(page)
#     except PageNotAnInteger:
#         years = paginator.page(1)
#     except EmptyPage:
#         years = paginator.page(paginator.num_pages)
#
#     latest_ids_subquery = BankStatement.objects.filter(
#         year_bank_statement=OuterRef('year_bank_statement')
#     ).values('year_bank_statement').annotate(
#         max_id=Max('id')
#     ).values('max_id')
#
#     bank_statements = BankStatement.objects.filter(
#         id__in=Subquery(latest_ids_subquery)
#     ).filter(year_bank_statement__in=years_list).order_by('-year_bank_statement')
#
#     latest_bank_statements = BankStatement.objects.filter(
#         id__in=Subquery(latest_ids_subquery)
#     ).values('year_bank_statement', 'income_bank_statement')
#     latest_income_by_year = {entry['year_bank_statement']: entry['income_bank_statement'] for entry in
#                              latest_bank_statements}
#
#     all_years = [entry[0] for entry in sorted_years]
#
#     return render(
#         request,
#         'TI_Management_app/finance/finance_list.html',
#         {
#             'years': years,
#             'page': page,
#             'bank_statements': bank_statements,
#             'latest_income': latest_income_by_year,
#             'all_years': all_years
#         }
#     )


@login_required
def finance_reporting_doc(request):
    current_date = datetime.now()
    current_year = current_date.year
    previous_year = current_year-1
    month = 0

    if request.method == "POST":
        form = BankStatementForm(request.POST, request.FILES)
        if form.is_valid():
            bank_statement = form.save(commit=False)
            bank_statement.author = request.user
            bank_statement.month_bank_statement = month
            bank_statement.save()
            messages.success(request, f"Dodano dokument sprawozdawczy {bank_statement.title_bank_statement}!")
            return redirect('TI_Management_app:finance_list')
    else:
        form = BankStatementForm()

    return render(
        request,
        'TI_Management_app/finance/finance_reporting_doc.html',
        {
            'form': form,
            'current_year': current_year,
            'previous_year': previous_year
        }
    )


@login_required
def finance_detail(request, year, month):

    tz = pytz.timezone('Europe/Warsaw')

    start_date = timezone.make_aware(datetime(year, month, 1), tz)
    end_date = timezone.make_aware(datetime(year, month + 1, 1), tz) if month < 12 else timezone.make_aware(
        datetime(year + 1, 1, 1), tz)

    finances = FileFinance.objects.filter(
        payment_date__gte=start_date,
        payment_date__lt=end_date
    ).exclude(payment_date__isnull=True).order_by('-payment_date')

    total_figure = finances.aggregate(Sum('figure'))['figure__sum']
    total_figure = total_figure if total_figure is not None else 0

    reliefs = RegisterRelief.objects.filter(
        payment_confirmation=True,
        date_of_payment_confirmation__gte=start_date,
        date_of_payment_confirmation__lt=end_date
    ).exclude(date_of_payment_confirmation__isnull=True).order_by('-date_of_payment_confirmation')

    total_reliefs = RegisterRelief.objects.aggregate(
        total=Sum(
            Case(
                When(payment_confirmation=True, then='relief__figure'),
                default=0,
                output_field=DecimalField()
            )
        )
    )['total']
    total_reliefs = total_reliefs if total_reliefs is not None else 0

    scholarships = Scholarships.objects.filter(
        confirmation_of_scholarship=True,
        confirmation_date__gte=start_date,
        confirmation_date__lt=end_date
    ).exclude(confirmation_date__isnull=True).order_by('-confirmation_date')

    total_scholarships = scholarships.aggregate(
        total=Sum(
            Case(
                When(confirmation_of_scholarship=True, then='scholarship_rate'),
                default=0,
                output_field=DecimalField()
            )
        )
    )['total']
    total_scholarships = total_scholarships if total_scholarships is not None else 0

    total_expenses = total_figure + total_reliefs + total_scholarships

    bank_statements = BankStatement.objects.filter(year_bank_statement=year, month_bank_statement=month).order_by('-month_bank_statement')
    total_income_bank_statements = BankStatement.objects.filter(year_bank_statement=year, month_bank_statement=month).aggregate(total_income_bank_statements=Sum('income_bank_statement'))
    total_income = total_income_bank_statements['total_income_bank_statements'] if total_income_bank_statements['total_income_bank_statements'] is not None else 0

    months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
    month_name = months[month-1]

    if request.method == "POST":
        form = BankStatementForm(request.POST, request.FILES)
        if form.is_valid():
            bank_statement = form.save(commit=False)
            bank_statement.author = request.user
            bank_statement.year_bank_statement = year
            bank_statement.month_bank_statement = month
            bank_statement.save()
            messages.success(request, f"Dodano dokument sprawozdawczy {bank_statement.title_bank_statement}!")
            return redirect('TI_Management_app:finance_list')
    else:
        form = BankStatementForm()

    return render(
        request,
        'TI_Management_app/finance/finance_detail.html',
        {
            'finances': finances,
            'reliefs': reliefs,
            'scholarships': scholarships,
            'year': year,
            'month': month,
            'month_name': month_name,
            'form': form,
            'total_figure': total_figure,
            'total_scholarships': total_scholarships,
            'total_reliefs': total_reliefs,
            'total_expenses': total_expenses,
            'bank_statements': bank_statements,
            'total_income': total_income
        }
    )


@login_required
def finance_file_detail(request, pk):
    finance_file_details = get_object_or_404(FileFinance, pk=pk)

    return render(
        request,
        'TI_Management_app/finance/finance_file_detail.html',
        {
            'finance_file_details': finance_file_details,
        }
    )


@login_required
def finance_file_edit(request, pk):
    finance_file_details = get_object_or_404(FileFinance, pk=pk)
    kind_of_finance_document = KindOfFinanceDocument.objects.all()
    doc_database = DocumentsDatabase.objects.filter(Q(category__title__icontains='Uchwały'))
    expense_names = KindOfFinanceExpense.objects.all()
    members = MembersZZTI.objects.all().order_by('member_nr')
    formatted_payment_date = finance_file_details.payment_date.astimezone(
        timezone.get_current_timezone()).strftime("%Y-%m-%d")

    if request.method == "POST":
        form_kind_of_document = KindOfFinanceDocumentForm(request.POST, instance=finance_file_details.type_of_document)
        form_file_finance = FileFinanceForm(request.POST, request.FILES, instance=finance_file_details)
        form_kind_of_expense = KindOfFinanceExpenseForm(request.POST, instance=finance_file_details.expense_name)

        if all([form_kind_of_document.is_valid(), form_file_finance.is_valid(), form_kind_of_expense.is_valid()]):
            document_title = form_kind_of_document.cleaned_data['title_doc']
            expense_title = form_kind_of_expense.cleaned_data['title_expense']
            member_nr = form_file_finance.cleaned_data['member_nr']
            psychologist = form_file_finance.cleaned_data['psychologist']
            title = f"{document_title} - {expense_title}"

            if not KindOfFinanceDocument.objects.filter(title_doc=document_title).exists():
                finance_document_kind = form_kind_of_document.save(commit=False)
                finance_document_kind.title = document_title
                finance_document_kind.author = request.user
                finance_document_kind.save()

            if not KindOfFinanceExpense.objects.filter(title_expense=expense_title).exists():
                kind_of_expense = form_kind_of_expense.save(commit=False)
                kind_of_expense.title = expense_title
                kind_of_expense.author = request.user
                kind_of_expense.save()

            finance_file = form_file_finance.save(commit=False)
            finance_file.author = request.user
            finance_file.title = title
            # finance_file.type_of_document = KindOfFinanceDocument.objects.get(title_doc=document_title)
            finance_file.type_of_document = KindOfFinanceDocument.objects.filter(title_doc=document_title).latest('id')
            # finance_file.expense_name = KindOfFinanceExpense.objects.get(title_expense=expense_title)
            finance_file.expense_name = KindOfFinanceExpense.objects.filter(title_expense=expense_title).latest('id')
            # finance_file.member = MembersZZTI.objects.get(member_nr=member_nr)
            if psychologist is True and MembersZZTI.objects.filter(member_nr=member_nr).exists():
                finance_file.member = MembersZZTI.objects.filter(member_nr=member_nr).latest('id')
            finance_file.save()

            messages.success(request, "Zaktualizowano!")
            return redirect('TI_Management_app:finance_file_edit', pk=finance_file_details.pk)
    else:
        form_kind_of_document = KindOfFinanceDocumentForm(instance=finance_file_details.type_of_document)
        form_file_finance = FileFinanceForm(instance=finance_file_details)
        form_kind_of_expense = KindOfFinanceExpenseForm(instance=finance_file_details.expense_name)
    return render(
        request,
        'TI_Management_app/finance/finance_file_edit.html',
        {
            'form_kind_of_document': form_kind_of_document,
            'form_file_finance': form_file_finance,
            'form_kind_of_expense': form_kind_of_expense,
            'finance_file_details': finance_file_details,
            'kind_of_finance_document': kind_of_finance_document,
            'doc_database': doc_database,
            'expense_names': expense_names,
            'members': members,
            'formatted_payment_date': formatted_payment_date
        }
    )


# @cache_page(60*15)
@login_required
def voting_add(request):
    # members = MembersZZTI.objects.filter(card__isnull=False, deactivate=False)
    members = MembersZZTI.objects.filter(card__isnull=False).exclude(card='').filter(deactivate=False)

    if request.method == "POST":
        form = VotingAddForm(request.POST or None)
        if form.is_valid():

            description = form.cleaned_data['description']
            sanitized_description = bleach.clean(description, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

            participants_all = form.cleaned_data['participants_all']
            # vote_method_online = form.cleaned_data['vote_method_online']
            # vote_method_offline = form.cleaned_data['vote_method_offline']
            participants_group = form.cleaned_data['participants_group']
            participants = request.POST.getlist('participants')
            commission = request.POST.getlist('commission')

            period = form.cleaned_data['period']
            date_accede = form.cleaned_data['date_accede']
            # print(f"Received period views: {period}")

            voting = form.save(commit=False)
            voting.author = request.user
            voting.description = sanitized_description
            voting.vote_method_offline = True
            voting.save()

            commission_set = set()
            for commission_one in commission:
                try:
                    commission_member = MembersZZTI.objects.get(member_nr=commission_one)
                    commission_set.add(commission_member)
                except MembersZZTI.DoesNotExist:
                    print(f"Commission with member_nr {commission_one} does not exist")

            # print(commission_set)

            # for member_commission in commission_set:
            #     voting.election_commission.add(member_commission)
            #
            # voting.save()
            voting.election_commission.set(commission_set)

            if participants_all:
                members_to_add = set()
                if period and date_accede:
                    if isinstance(date_accede, datetime):
                        date_accede = date_accede.date()

                    if period == 'from':
                        members_to_add = members.filter(date_of_accession__gt=date_accede)
                    elif period == 'to':
                        members_to_add = members.filter(date_of_accession__lt=date_accede)
                    else:
                        members_to_add = members.filter(date_of_accession=date_accede)
                else:
                    members_to_add = members

                voting.members.set(members_to_add)
                voting.save()

            else:
                members_set = set()

                if participants_group:

                    if period and date_accede:
                        if isinstance(date_accede, datetime):
                            date_accede = date_accede.date()

                        if period == 'from':
                            for group in participants_group:
                                group_members = GroupsMember.objects.filter(group=group, member__date_of_accession__gt=date_accede)
                                for group_member in group_members:
                                    members_set.add(group_member.member)

                        elif period == 'to':
                            for group in participants_group:
                                group_members = GroupsMember.objects.filter(group=group, member__date_of_accession__lt=date_accede)
                                for group_member in group_members:
                                    members_set.add(group_member.member)
                        else:
                            for group in participants_group:
                                group_members = GroupsMember.objects.filter(group=group, member__date_of_accession=date_accede)
                                for group_member in group_members:
                                    members_set.add(group_member.member)
                                 
                    else:

                        for group in participants_group:
                            # print(group)
                            group_members = GroupsMember.objects.filter(group=group)
                            for group_member in group_members:
                                members_set.add(group_member.member)

                for participant in participants:
                    try:
                        participant_member = MembersZZTI.objects.get(member_nr=participant)
                        members_set.add(participant_member)
                    except MembersZZTI.DoesNotExist:
                        print(f"Participant with member_nr {participant} does not exist")

                for member_set in members_set:
                    voting.members.add(member_set)

            voting.save()

            messages.success(request, f"Dodano głosowanie - {voting.title}!")
            return redirect('TI_Management_app:voting_add_poll', pk=voting.pk)
    else:
        form = VotingAddForm()
    return render(
        request,
        'TI_Management_app/voting/voting_add.html',
        {
            'form': form,
            'members': members
        }
    )


@login_required
def voting_add_poll(request, pk):
    voting = get_object_or_404(Vote, pk=pk)
    poll_exist = voting.votePoll.exists()
    members = MembersZZTI.objects.filter(card__isnull=False).exclude(card='').filter(deactivate=False)

    current_date = timezone.now()
    voting_date_start = voting.date_start
    if voting_date_start:
        if voting_date_start > current_date:
            voting_status: bool = True
        else:
            voting_status: bool = False
    else:
        voting_status: bool = True


    if request.method == "POST":
        form = VotingAddPollForm(request.POST)
        form_choice = VotingAddChoiceForm(request.POST)
        if all([form.is_valid(), form_choice.is_valid()]):
            question = form.cleaned_data['question']
            finish = form.cleaned_data['finish']
            description = form.cleaned_data['description']
            sanitized_description = bleach.clean(description, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

            poll = form.save(commit=False)
            poll.author = request.user
            poll.vote = voting
            poll.question = question.title()
            poll.description = sanitized_description
            poll.save()

            # open_ended_answer
            open_ended_answer = form_choice.cleaned_data['open_ended_answer']
            print(open_ended_answer)

            answers = []
            correct_choices = []
            for key in request.POST:
                if key.startswith('answer_'):
                    answer_index = key.split('_')[1]
                    answers.append(request.POST[key])
                    correct_choices.append(request.POST.get(f'correct_{answer_index}') == 'on')

            if open_ended_answer or not answers:
                choice = Choice(author=request.user, poll=poll, open_ended_answer=True)
                choice.save()
            else:
                for answer, is_correct in set(zip(answers, correct_choices)):
                    choice = Choice(author=request.user, poll=poll, answer=answer, correct=is_correct, open_ended_answer=False)
                    choice.save()

            if finish:
                messages.success(request, "Podsumowanie")
                return redirect('TI_Management_app:voting_add_recap', pk=voting.pk)
            else:
                messages.success(request, f"Dodano pytanie / polecenie {poll.question}")
                return redirect('TI_Management_app:voting_add_poll', pk=voting.pk)
    else:
        form = VotingAddPollForm()
        form_choice = VotingAddChoiceForm()
    return render(
        request,
        'TI_Management_app/voting/voting_add_poll.html',
        {
            'form': form,
            'form_choice': form_choice,
            'voting': voting,
            'poll_exist': poll_exist,
            'members': members,
            'voting_status': voting_status
        }
    )


# @cache_page(60*15)
@login_required
def voting_add_recap(request, pk):
    voting = get_object_or_404(Vote, pk=pk)

    current_date = timezone.now()
    voting_date_start = voting.date_start
    if voting_date_start:
        if voting_date_start > current_date:
            voting_status: bool = True
        else:
            voting_status: bool = False
    else:
        voting_status: bool = True

    if request.method == "POST":
        form = VotingAddRecapForm(request.POST, instance=voting)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.author = request.user
            # poll.vote = voting
            poll.save()

            messages.success(request, f"Głosowanie dodane i rozpocznie się {poll.date_start}")
            return redirect('TI_Management_app:voting_list')
    else:
        form = VotingAddRecapForm()
    return render(
        request,
        'TI_Management_app/voting/voting_add_recap.html',
        {
            'form': form,
            'voting': voting,
            'voting_status': voting_status
        }
    )


@login_required
def voting_list(request):
    # vote_obj = Vote.objects.all().order_by('-created_date')
    vote_obj = Vote.objects.filter(date_start__gte=timezone.now()).order_by('-created_date')
    votes_without_date_start = Vote.objects.filter(date_start__isnull=True)
    votes_with_date_start = Vote.objects.filter(date_start__gte=timezone.now(), date_start__isnull=False)

    paginator = Paginator(vote_obj, 50)
    page = request.GET.get('page')
    try:
        voting = paginator.page(page)
    except PageNotAnInteger:
        voting = paginator.page(1)
    except EmptyPage:
        voting = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/voting/voting_list.html',
        {
            'page': page,
            'voting': voting,
            'votes_without_date_start': votes_without_date_start,
            'votes_with_date_start': votes_with_date_start
        }
    )


@login_required
def voting_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        voting = Vote.objects.filter(
            Q(title__icontains=searched) &
            Q(date_start__gte=timezone.now())
        )
        return render(
            request,
            'TI_Management_app/voting/voting_search.html',
            {
                'searched': searched,
                'voting': voting
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/voting/voting_search.html',
            {}
        )


@login_required
def voting_detail(request, pk):
    voting = get_object_or_404(Vote, pk=pk)

    return render(
        request,
        'TI_Management_app/voting/voting_detail.html',
        {
            'voting': voting
        }
    )


@login_required
def voting_edit(request, pk):
    voting = get_object_or_404(Vote, pk=pk)
    # members = MembersZZTI.objects.filter(card__isnull=False, deactivate=False)
    members = MembersZZTI.objects.filter(card__isnull=False).exclude(card='').filter(deactivate=False)

    current_date = timezone.now()
    voting_date_start = voting.date_start
    if voting_date_start > current_date:
        voting_status: bool = True
    else:
        voting_status: bool = False

    if request.method == "POST":
        form = VotingAddForm(request.POST, instance=voting)
        form_duration = VotingAddRecapForm(request.POST, instance=voting)
        if all([form.is_valid(), form_duration.is_valid()]):

            description = form.cleaned_data['description']
            sanitized_description = bleach.clean(description, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

            participants_all = form.cleaned_data['participants_all']
            participants_group = form.cleaned_data['participants_group']
            participants = request.POST.getlist('participants')
            commission = request.POST.getlist('commission')

            voting = form.save(commit=False)
            voting.author = request.user
            voting.description = sanitized_description
            voting.save()

            commission_set = set()
            for commission_one in commission:
                try:
                    commission_member = MembersZZTI.objects.get(member_nr=commission_one)
                    commission_set.add(commission_member)
                except MembersZZTI.DoesNotExist:
                    print(f"Commission with member_nr {commission_one} does not exist")

            # voting.election_commission.set(commission_set)
            for member_set in commission_set:
                voting.election_commission.add(member_set)
            voting.save()

            if participants_all:
                for member in set(members):
                    voting.members.add(member)
                voting.save()
            else:
                members_set = set()

                if participants_group:
                    for group in participants_group:
                        group_members = GroupsMember.objects.filter(group=group)
                        for group_member in group_members:
                            members_set.add(group_member.member)

                for participant in participants:
                    try:
                        participant_member = MembersZZTI.objects.get(member_nr=participant)
                        members_set.add(participant_member)
                    except MembersZZTI.DoesNotExist:
                        print(f"Participant with member_nr {participant} does not exist")

                for member_set in members_set:
                    voting.members.add(member_set)

                voting.save()

                duration = form_duration.save(commit=False)
                duration.save()

            messages.success(request, f"Zaktualizowano głosowanie! - {voting.title}")
            return redirect('TI_Management_app:voting_detail', pk=voting.pk)
    else:
        form = VotingAddForm(instance=voting)
        form_duration = VotingAddRecapForm(instance=voting)
    return render(
        request,
        'TI_Management_app/voting/voting_edit.html',
        {
            'form': form,
            'form_duration': form_duration,
            'members': members,
            'voting': voting,
            'voting_status': voting_status
        }
    )


@login_required
def remove_member_from_vote(request, vote_pk, member_pk):
    vote_instance = get_object_or_404(Vote, pk=vote_pk)
    member_instance = get_object_or_404(MembersZZTI, pk=member_pk)

    vote_instance.members.remove(member_instance)

    return redirect('TI_Management_app:voting_edit', pk=vote_pk)


@login_required
def remove_election_commission_from_vote(request, vote_pk, member_pk):
    vote_instance = get_object_or_404(Vote, pk=vote_pk)
    election_commission_instance = get_object_or_404(MembersZZTI, pk=member_pk)

    vote_instance.election_commission.remove(election_commission_instance)

    return redirect('TI_Management_app:voting_edit', pk=vote_pk)


@login_required
def voting_edit_poll_remove(request, vote_pk, poll_pk):
    # vote_instance = get_object_or_404(Vote, pk=vote_pk)
    poll_instance = get_object_or_404(Poll, pk=poll_pk)

    poll_instance.delete()

    return redirect('TI_Management_app:voting_detail', pk=vote_pk)


@login_required
def voting_edit_poll(request, pk, poll_pk):
    voting = get_object_or_404(Vote, pk=pk)
    poll = get_object_or_404(Poll, pk=poll_pk)
    poll_exist = voting.votePoll.exists()
    members = MembersZZTI.objects.filter(card__isnull=False).exclude(card='').filter(deactivate=False)
    # choice = Choice.objects.filter(poll=poll_pk)
    choices = poll.pollChoice.all()

    current_date = timezone.now()
    voting_date_start = voting.date_start
    if voting_date_start > current_date:
        voting_status: bool = True
    else:
        voting_status: bool = False

    for choice in choices:
        if choice.open_ended_answer is True:
            open_answer: bool = True
        else:
            open_answer: bool = False

    if request.method == "POST":
        form = VotingAddPollForm(request.POST, instance=poll)
        form_choice = VotingAddChoiceForm(request.POST)
        if all([form.is_valid(), form_choice.is_valid()]):
            finish = form.cleaned_data['finish']
            description = form.cleaned_data['description']
            sanitized_description = bleach.clean(description, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

            poll = form.save(commit=False)
            poll.author = request.user
            poll.vote = voting
            poll.description = sanitized_description
            poll.save()

            answers = []
            correct_choices = []
            for key in request.POST:
                if key.startswith('answer_'):
                    answer_index = key.split('_')[1]
                    answers.append(request.POST[key])
                    correct_choices.append(request.POST.get(f'correct_{answer_index}') == 'on')

            # print(answers)
            # print(correct_choices)

            for answer, is_correct in zip(answers, correct_choices):
                choice = Choice(author=request.user, poll=poll, answer=answer, correct=is_correct)
                choice.save()

            messages.success(request, "Podsumowanie")
            return redirect('TI_Management_app:voting_add_recap', pk=voting.pk)
    else:
        form = VotingAddPollForm(instance=poll)
        form_choice = VotingAddChoiceForm()
    return render(
        request,
        'TI_Management_app/voting/voting_edit_poll.html',
        {
            'form': form,
            'form_choice': form_choice,
            'voting': voting,
            'poll_exist': poll_exist,
            'poll': poll,
            'members': members,
            'voting_status': voting_status,
            'open_answer': open_answer
        }
    )


@login_required
def remove_choice_from_poll(request, pk, vote_pk, poll_pk):
    choice = get_object_or_404(Choice, pk=pk)
    choice.delete()
    return redirect('TI_Management_app:voting_edit_poll', pk=vote_pk, poll_pk=poll_pk)


@login_required
def voting_active_session_list(request):
    vote_obj = Vote.objects.filter(
        date_start__lte=timezone.now(),
        date_end__gte=timezone.now()
    ).order_by('-created_date')

    active_session = VotingSessionKickOff.objects.order_by('-created_date').first()
    current_date = timezone.now()
    if active_session is not None and active_session.session_end:
        session_end = active_session.session_end
        if session_end > current_date:
            session_status = True
        else:
            session_status = False
    else:
        session_status = False

    paginator = Paginator(vote_obj, 50)
    page = request.GET.get('page')
    try:
        voting = paginator.page(page)
    except PageNotAnInteger:
        voting = paginator.page(1)
    except EmptyPage:
        voting = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/voting/voting_active_session_list.html',
        {
            'page': page,
            'voting': voting,
            'session_status': session_status
        }
    )


@login_required
def voting_active_session_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        voting = Vote.objects.filter(
            Q(title__icontains=searched) &
            Q(date_start__lte=timezone.now()) &
            Q(date_end__gte=timezone.now())
        )
        return render(
            request,
            'TI_Management_app/voting/voting_active_session_search.html',
            {
                'searched': searched,
                'voting': voting
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/voting/voting_active_session_search.html',
            {}
        )


@login_required
def voting_active_session_detail(request, pk):
    voting = get_object_or_404(Vote, pk=pk)
    sessions = VotingSessionKickOff.objects.filter(vote=voting)
    member_already_participated = VotingSessionSignature.objects.filter(vote=voting)

    # Show only ended sessions
    sessions_status = sessions.filter(
        Q(session_end__lte=timezone.now()) |
        Q(session_closed=True)
    )

    return render(
        request,
        'TI_Management_app/voting/voting_active_session_detail.html',
        {
            'voting': voting,
            'sessions': sessions,
            'sessions_status': sessions_status,
            'member_already_participated': member_already_participated
        }
    )


class VotingActiveSessionMemberDetail(LoginRequiredMixin, DetailView):
    model = MembersZZTI
    template_name = 'TI_Management_app/voting/voting_active_session_member_detail.html'
    context_object_name = 'member'


@login_required
def voting_active_session_kick_off(request, pk):
    voting = get_object_or_404(Vote, pk=pk)
    now = timezone.now()

    if request.method == "POST":
        form = VotingSessionKickOffForm(request.POST, initial={'title': f"sesja#{now.timestamp()}#{voting.title}"})
        if form.is_valid():
            session_kick_off = form.save(commit=False)
            session_kick_off.author = request.user
            session_kick_off.vote = voting
            session_kick_off.session_start = timezone.now()
            session_kick_off.save()

            messages.success(request, f"Rozpoczęcie sesji głosowania")
            return redirect('TI_Management_app:voting_active_session_kick_off_edit', pk_vote=pk, pk_kick_off=session_kick_off.id)
    else:
        form = VotingSessionKickOffForm(initial={'title': f"sesja#{now.timestamp()}#{voting.title}"})
    return render(
        request,
        'TI_Management_app/voting/voting_active_session_kick_off.html',
        {
            'form': form,
            'voting': voting
        }
    )


@login_required
def voting_active_session_close(request, pk_vote, pk_kick_off):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)

    if request.method == "POST":
        form = VotingSessionCloseForm(request.POST, instance=session_kick_off)
        if form.is_valid():
            session_close = form.save(commit=False)
            session_close.author = request.user
            session_close.session_closed = True
            session_close.session_end = timezone.now()
            session_close.save()

            messages.success(request, f"Sesja głosowania '{session_kick_off.title}' została zakończona")
            return redirect('TI_Management_app:voting_active_session_detail', pk=pk_vote)
    else:
        form = VotingSessionCloseForm(instance=session_kick_off)
    return render(
        request,
        'TI_Management_app/voting/voting_active_session_close.html',
        {
            'form': form,
            'voting': voting,
            'session_kick_off': session_kick_off
        }
    )


@login_required
def voting_active_session_kick_off_edit(request, pk_vote, pk_kick_off):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off_edit = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
    voting_session_kick_off_signature = VotingSessionKickOffSignature.objects.filter(voting_session_kick_off=session_kick_off_edit)

    if request.method == "POST":
        form_signature = VotingSessionKickOffSignatureForm(request.POST, voting_session_kick_off=session_kick_off_edit)

        if form_signature.is_valid():
            commission_signature = form_signature.cleaned_data['commission_signature']
            vote = session_kick_off_edit.vote

            for member in vote.election_commission.all():
                if check_password(commission_signature, member.card):
                    member_id = member

            if member_id:
                session_kick_off_signature = form_signature.save(commit=False)
                session_kick_off_signature.author = request.user
                session_kick_off_signature.voting_session_kick_off = session_kick_off_edit
                session_kick_off_signature.member = member_id
                session_kick_off_signature.signature = True
                session_kick_off_signature.save()

                # messages.success(request, "Dodano podpis Członka komisji")
                if int(voting.min_amount_commission) > len(voting_session_kick_off_signature):
                    return redirect(
                        'TI_Management_app:voting_active_session_kick_off_edit',
                        pk_vote=voting.id,
                        pk_kick_off=session_kick_off_edit.id
                    )
                else:
                    session_kick_off_edit = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
                    session_kick_off_edit.commission_confirmed = True
                    session_kick_off_edit.save()

                    return render(
                        request,
                        'TI_Management_app/voting/new_window_redirect.html',
                        {
                            'redirect_url': reverse(
                                'TI_Management_app:voting_active_session',
                                args=[voting.id, session_kick_off_edit.id]
                            ),
                            'safe_redirect_url': reverse(
                                'TI_Management_app:voting_active_session_kick_off_validation',
                                args=[voting.id, session_kick_off_edit.id]
                            )
                        }
                    )
    else:
        form_signature = VotingSessionKickOffSignatureForm(voting_session_kick_off=session_kick_off_edit)

    return render(
        request,
        'TI_Management_app/voting/voting_active_session_kick_off_edit.html',
        {
            'form_signature': form_signature,
            'voting': voting,
            'voting_session_kick_off_signature': voting_session_kick_off_signature
        }
    )


@login_required
def voting_active_session(request, pk_vote, pk_kick_off):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
    session_signature = VotingSessionSignature.objects.filter(vote=voting)

    if session_kick_off.session_end <= timezone.now() or session_kick_off.session_closed is True:
        sessions_status = False
        print("you can not give the vote")
    else:
        sessions_status = True
        print("you can give vote")

    if sessions_status:
        if request.method == "POST":
            # form = VotingSessionSignatureForm(request.POST, vote=voting, session_signature=session_signature)
            form = VotingSessionSignatureForm(request.POST, vote=voting)

            if form.is_valid():
                member_signature = form.cleaned_data['member_signature']

                # vote = session_signature.vote

                member_checked = None
                for member in voting.members.all():
                    if check_password(member_signature, member.card):
                        member_checked = member
                        break

                if member_checked:
                    session_kick_off_signature = form.save(commit=False)
                    session_kick_off_signature.author = request.user
                    session_kick_off_signature.vote = voting
                    session_kick_off_signature.voting_session_kick_off = session_kick_off
                    session_kick_off_signature.member = member_checked
                    session_kick_off_signature.signature = True
                    session_kick_off_signature.save()

                    return redirect(
                        'TI_Management_app:voting_active_session_validation',
                        pk_vote=voting.id,
                        pk_kick_off=session_kick_off.id,
                        pk_member=session_kick_off_signature.id
                    )
        else:
            form = VotingSessionSignatureForm(vote=voting)

        return render(
            request,
            'TI_Management_app/voting/voting_active_session.html',
            {
                'form': form,
                'voting': voting,
                'session_kick_off': session_kick_off,
                'session_signature': session_signature
            }
        )


@login_required
def check_session_status(request, pk_kick_off):
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)

    if session_kick_off.session_end <= timezone.now() or session_kick_off.session_closed:
        return JsonResponse({'session_status': False})
    else:
        return JsonResponse({'session_status': True})


@login_required
def voting_active_session_validation(request, pk_vote, pk_kick_off, pk_member):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
    member = get_object_or_404(VotingSessionSignature, pk=pk_member)
    polls = Poll.objects.filter(vote=voting)

    if session_kick_off.session_end <= timezone.now() or session_kick_off.session_closed:
        sessions_status = False
    else:
        sessions_status = True

    if sessions_status:

        if request.method == 'POST':
            forms = []
            form_is_valid = True
            voting_responses = []

            for poll in polls:
                form = ChoiceForm(request.POST, poll=poll)
                forms.append(form)

                if form.is_valid():
                    selected_answers = [key for key, value in form.cleaned_data.items() if value]

                    # print(selected_answers)

                    for selected_answer in selected_answers:

                        choice_id = selected_answer.split('_')[1]

                        # print(choice_id)
                        # print(poll.id)

                        choice = get_object_or_404(Choice, pk=choice_id, poll=poll)

                        voting_response = VotingResponses(
                            author=request.user,
                            vote=voting,
                            voting_session_kick_off=session_kick_off,
                            poll=poll,
                            choice=choice
                        )
                        voting_responses.append(voting_response)

                else:
                    form_is_valid = False

            if form_is_valid:
                for response in voting_responses:
                    response.save()

                return redirect(
                    'TI_Management_app:voting_active_session_successful',
                    pk_vote=voting.id,
                    pk_kick_off=session_kick_off.id,
                    pk_member=member.id
                )

            return render(
                request,
                'TI_Management_app/voting/voting_active_session_validation.html',
                {
                    'forms': forms,
                    'voting': voting,
                    'session_kick_off': session_kick_off,
                    'member': member,
                    'polls': polls,
                }
            )

        else:
            forms = [ChoiceForm(poll=poll) for poll in polls]

        return render(
            request,
            'TI_Management_app/voting/voting_active_session_validation.html',
            {
                'forms': forms,
                'voting': voting,
                'session_kick_off': session_kick_off,
                'member': member,
                'polls': polls
            }
        )


@login_required
def voting_active_session_kick_off_validation(request, pk_vote, pk_kick_off):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
    session_signatures = VotingSessionSignature.objects.filter(vote=voting)

    return render(
        request,
        'TI_Management_app/voting/voting_active_session_kick_off_validation.html',
        {
            'voting': voting,
            'session_kick_off': session_kick_off,
            'session_signatures': session_signatures
        }
    )


@login_required
def voting_active_session_approve(request, pk_vote, pk_kick_off, pk_member):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
    member = get_object_or_404(VotingSessionSignature, pk=pk_member)
    session_signatures = VotingSessionSignature.objects.filter(vote=voting)

    member.confirmation = True
    member.reject = False
    member.save()

    return render(
        request,
        'TI_Management_app/voting/voting_active_session_kick_off_validation.html',
        {
            'voting': voting,
            'session_kick_off': session_kick_off,
            'session_signatures': session_signatures
        }
    )


@login_required
def voting_active_session_disapprove(request, pk_vote, pk_kick_off, pk_member):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
    member = get_object_or_404(VotingSessionSignature, pk=pk_member)
    session_signatures = VotingSessionSignature.objects.filter(vote=voting)

    member.confirmation = True
    member.reject = True
    member.save()

    return render(
        request,
        'TI_Management_app/voting/voting_active_session_kick_off_validation.html',
        {
            'voting': voting,
            'session_kick_off': session_kick_off,
            'session_signatures': session_signatures
        }
    )


@login_required
def voting_active_session_successful(request, pk_vote, pk_kick_off, pk_member):
    voting = get_object_or_404(Vote, pk=pk_vote)
    session_kick_off = get_object_or_404(VotingSessionKickOff, pk=pk_kick_off)
    member = get_object_or_404(VotingSessionSignature, pk=pk_member)

    return render(
        request,
        'TI_Management_app/voting/voting_active_session_successful.html',
        {
            'voting': voting,
            'session_kick_off': session_kick_off,
            'member': member
        }
    )


@login_required
def voting_history_and_reports_list(request):

    voting_obj = Vote.objects.filter(Q(date_end__lte=timezone.now()))

    paginator = Paginator(voting_obj, 50)
    page = request.GET.get('page')
    try:
        voting = paginator.page(page)
    except PageNotAnInteger:
        voting = paginator.page(1)
    except EmptyPage:
        voting = paginator.page(paginator.num_pages)

    return render(
        request,
        'TI_Management_app/voting/voting_history_and_reports_list.html',
        {
            'page': page,
            'voting': voting
        }
    )


@login_required
def voting_history_and_reports_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        voting = Vote.objects.filter(
            Q(title__icontains=searched) &
            Q(date_end__lte=timezone.now())
        )
        return render(
            request,
            'TI_Management_app/voting/voting_history_and_reports_search.html',
            {
                'searched': searched,
                'voting': voting
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/voting/voting_history_and_reports_search.html',
            {}
        )


@login_required
def voting_history_and_reports_detail(request, pk):
    voting = get_object_or_404(Vote, pk=pk)
    member_already_participated = VotingSessionSignature.objects.filter(vote=voting)
    member_rejected = VotingSessionSignature.objects.filter(vote=voting, reject=True)
    member_accepted = VotingSessionSignature.objects.filter(vote=voting, reject=False)

    poll = Poll.objects.filter(vote=voting)

    polls_with_responses = []

    # Loop through each poll and count how many times each choice was selected
    for poll_one in poll:
        voting_responses = VotingResponses.objects.filter(poll=poll_one)
        choice_counts = voting_responses.values('choice__answer').annotate(choice_count=Count('choice'))

        polls_with_responses.append({
            'poll_one': poll_one,
            'choice_counts': choice_counts
        })

    if voting.members.count() > 0:
        min_attendance = (voting.min_amount_commission / voting.members.count()) * 100
    else:
        min_attendance = 0

    if member_already_participated.count() > 0:
        attendance = (member_already_participated.count() / voting.members.count()) * 100
    else:
        attendance = 0

    if attendance > voting.turnout:
        grant = True
    else:
        grant = False

    return render(
        request,
        'TI_Management_app/voting/voting_history_and_reports_detail.html',
        {
            'voting': voting,
            'min_attendance': min_attendance,
            'attendance': attendance,
            'grant': grant,
            'member_already_participated': member_already_participated,
            'member_rejected': member_rejected,
            'member_accepted': member_accepted,
            # 'choices': choices,
            'poll': poll,
            'polls_with_responses': polls_with_responses,
        }
    )
