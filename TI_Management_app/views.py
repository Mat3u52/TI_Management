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
    FileRegisterRelief
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
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
    SignatureReliefForm
)
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
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


# class Image(TemplateView):
#     form = MemberForm
#     template_name = 'TI_Management_app/image.html'
#
#     def member(self, request, *args, **kwargs):
#         form = MemberForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save()
#             return HttpResponseRedirect(reverse_lazy('image_display', kwargs={'pk': obj.id}))
#
#         context = self.get_context_data(form=form)
#         return self.render_to_response(context)
#
#     def get(self, request, *args, **kwargs):
#         return self.member(request, *args, **kwargs)
#
#
# class ImageDisplay(DetailView):
#     model = MembersZZTI
#     template_name = 'TI_Management_app/image_display.html'
#     context_object_name = 'image'


@login_required
def members_list(request):
    members_obj = MembersZZTI.objects.all().order_by('-created_date')

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
        'TI_Management_app/members_list.html',
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

    return render(request,
                  'TI_Management_app/members_table_list.html',
                  {'page': page,
                   'members': members})


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
    # accessed = get_object_or_404(Cards, pk__in=different_elements)

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

    return render(request, 'TI_Management_app/member_detail.html',
                  {'member': member,
                   'accessible_ids': accessible_ids,
                   'card_names': card_names,
                   'different_elements': different_elements,
                   'accessible': accessible,
                   'accessible_group': accessible_group,
                   'different_elements_group': different_elements_group,
                   'card_history_entries': card_history_entries,
                   'seen_cards': seen_cards,
                   'note_entries': note_entries,
                   'seen_note': seen_note})


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
            messages.success(request, "Zaktualizowano!")

            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberDeactivateForm(instance=member)
    return render(request, 'TI_Management_app/member_deactivate.html',
                  {'form': form,
                   'member': member,
                   'member_loyalty_cards': member_loyalty_cards,
                   'member_groups': member_groups})


def error_404_view(request, exception):
    data = {"name": "TI_Management"}
    return render(request, 'TI_Management_app/404.html', data)


@login_required
def member_new(request):
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            member.save()
            messages.success(request, "Dodano nowego członka!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberForm()
    return render(request, 'TI_Management_app/member_new.html', {'form': form})


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
        # birthday = member.birthday
        # form = MemberForm(instance=member, initial={'birthday': birthday})
    return render(request, 'TI_Management_app/member_edit.html', {'form': form,
                                                                  'member': member})


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
        'TI_Management_app/member_function_add.html',
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
        'TI_Management_app/member_function_edit.html',
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
            messages.success(request, f"Dodano nowy zawód {occupation.member_occupation}!")
            return redirect('TI_Management_app:member_occupation_add')
    else:
        form = MemberOccupationForm()
    return render(request, 'TI_Management_app/member_occupation_add.html',
                  {'form': form, 'all_occupation': all_occupation})


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
            messages.success(request, f"Zaktualizowano zawód {occupation.member_occupation}!")
            return redirect('TI_Management_app:member_occupation_add')
    else:
        form = MemberOccupationForm(instance=occupation)
    return render(
        request,
        'TI_Management_app/member_occupation_edit.html',
        {
            'form': form,
            'all_occupation': all_occupation,
            'occupation': occupation
        }
    )


@login_required
def member_card_edit(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            member.save()
            messages.success(request, "Zaktualizowano!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'TI_Management_app/member_card_edit.html',
                  {
                      'form': form,
                      'member': member}
                  )


def member_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        members = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
                                             Q(surname__contains=searched.capitalize()) |
                                             Q(member_nr__contains=searched) |
                                             Q(phone_number__contains=searched))
        return render(request,
                      'TI_Management_app/member_search.html',
                      {'searched': searched,
                       'members': members})
    else:
        return render(request,
                      'TI_Management_app/member_search.html',
                      {})


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
    return render(request, 'TI_Management_app/member_file_edit.html',
                  {
                      'form': form,
                      'member': member}
                  )


@login_required
def member_file_delete(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_file = get_object_or_404(MembersFile, pk=pk1)

    member.author = request.user
    member_file.file.delete()
    member_file.delete()
    return redirect('TI_Management_app:member_detail', pk=member.pk)


def loyalty_card_list(request):
    loyalty_card_obj = Cards.objects.all()

    paginator = Paginator(loyalty_card_obj, 5)
    page = request.GET.get('page')
    try:
        loyalty_card = paginator.page(page)
    except PageNotAnInteger:
        loyalty_card = paginator.page(1)
    except EmptyPage:
        loyalty_card = paginator.page(paginator.num_pages)

    return render(request,
                  'TI_Management_app/loyalty_card_list.html',
                  {'page': page,
                   'loyalty_card': loyalty_card})


def loyalty_card_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        loyalty_card = Cards.objects.filter(Q(card_name__contains=searched))
        return render(request,
                      'TI_Management_app/loyalty_card_search.html',
                      {'searched': searched,
                       'loyalty_card': loyalty_card})
    else:
        return render(request,
                      'TI_Management_app/loyalty_card_search.html',
                      {})


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
            Q(phone_number__contains=searched)
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
            'TI_Management_app/loyalty_card_member_search.html',
            {
                'searched': searched,
                'loyalty_card_member': loyalty_card_member,
                'loyalty_card': loyalty_card,
                'loyalty_card_validator': loyalty_card_validator,
                'members_in_validator': members_in_validator,
            }
        )
    else:
        return render(request,
                      'TI_Management_app/loyalty_card_member_search.html',
                      {})


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

    return render(request, 'TI_Management_app/loyalty_card_detail.html',
                  {'loyalty_card': loyalty_card,
                   'status_card_file': status_card_file,
                   'status_card_file_a': status_card_file_a,
                   'ordered_card_file': ordered_card_file,
                   'to_be_picked_up_doc_card_file': to_be_picked_up_doc_card_file,
                   'form': form})


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
    return render(request, 'TI_Management_app/loyalty_card_add.html',
                  {'form': form})


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
    return render(request, 'TI_Management_app/loyalty_card_edit.html',
                  {'form': form})


@login_required
def loyalty_card_add_member(request, pk, pk1):
    # TODO: confirmation by tapping the card to the reader
    loyalty_card = get_object_or_404(Cards, pk=pk)
    loyalty_card_member_add = get_object_or_404(MembersZZTI, pk=pk1)
    loyalty_card_validator = CardStatus.objects.all()
    if request.method == "POST":
        form = LoyaltyCardAddMemberForm(request.POST)
        if form.is_valid():
            loyalty_card_member = form.save(commit=False)
            loyalty_card_member.author = request.user
            loyalty_card_member.card = loyalty_card
            loyalty_card_member.member = loyalty_card_member_add
            loyalty_card_member.date_of_action = timezone.now()
            loyalty_card_member.save()
            messages.success(request, "Dodano nowego uczestnika!")
            return redirect('TI_Management_app:loyalty_card_detail', pk=loyalty_card.pk, category='none')
    else:
        username = request.user.username
        form = LoyaltyCardAddMemberForm(initial={'card': loyalty_card,
                                                 'member': loyalty_card_member_add,
                                                 'responsible': username})
    return render(request, 'TI_Management_app/loyalty_card_add_member.html',
                  {'form': form,
                   'loyalty_card': loyalty_card,
                   'loyalty_card_member_add': loyalty_card_member_add,
                   'loyalty_card_validator': loyalty_card_validator})


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
        form = OrderedCardDocumentForm(initial={'card': loyalty_card,
                                                'responsible': username})
    return render(request, 'TI_Management_app/loyalty_cards_add_file_order.html',
                  {
                      'form': form,
                      'loyalty_card': loyalty_card}
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
        form = ToBePickedUpCardDocumentForm(initial={'card': loyalty_card,
                                                     'responsible': username})
    return render(request, 'TI_Management_app/loyalty_cards_add_file_to_be_picked_up.html',
                  {
                      'form': form,
                      'loyalty_card': loyalty_card}
                  )


@login_required
def loyalty_cards_add_member_file_order(request, pk):
    loyalty_card = get_object_or_404(CardStatus, pk=pk)
    if request.method == "POST":
        form = LoyaltyCardsAddMemberFileOrderForm(request.POST, request.FILES, instance=loyalty_card)
        if form.is_valid():
            loyalty_card_member = form.save(commit=False)
            loyalty_card_member.author = request.user
            loyalty_card_member.file_date = timezone.now()
            loyalty_card_member.save()
            messages.success(request, f"Dodano dokument!")
            return redirect('TI_Management_app:loyalty_card_list')
    else:
        form = LoyaltyCardsAddMemberFileOrderForm(instance=loyalty_card)
    return render(request, 'TI_Management_app/loyalty_cards_add_member_file_order.html',
                  {'form': form,
                   'loyalty_card': loyalty_card})


@login_required
def loyalty_card_member_file_order_search(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    loyalty_card_validator = CardStatus.objects.all()
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        loyalty_card_member = MembersZZTI.objects.filter(
            Q(forename__contains=searched.capitalize()) |
            Q(surname__contains=searched.capitalize()) |
            Q(member_nr__contains=searched) |
            Q(phone_number__contains=searched)
        )
        return render(request,
                      'TI_Management_app/loyalty_card_member_file_order_search.html',
                      {'searched': searched,
                       'loyalty_card_member': loyalty_card_member,
                       'loyalty_card': loyalty_card,
                       'loyalty_card_validator': loyalty_card_validator})
    else:
        return render(request,
                      'TI_Management_app/loyalty_card_member_file_order_search.html',
                      {})


@login_required
def loyalty_cards_add_member_file_to_be_picked_up(request, pk):
    loyalty_card = get_object_or_404(CardStatus, pk=pk)
    if request.method == "POST":
        form = LoyaltyCardsAddMemberFileToBePickedUpForm(request.POST, request.FILES, instance=loyalty_card)
        if form.is_valid():
            loyalty_card_member = form.save(commit=False)
            loyalty_card_member.author = request.user
            loyalty_card_member.file_a_date = timezone.now()
            loyalty_card_member.save()
            messages.success(request, "Dodano dokument!")
            return redirect('TI_Management_app:loyalty_card_list')
    else:
        form = LoyaltyCardsAddMemberFileToBePickedUpForm(instance=loyalty_card)
    return render(request, 'TI_Management_app/loyalty_cards_add_member_file_to_be_picked_up.html',
                  {'form': form,
                   'loyalty_card': loyalty_card})


@login_required
def loyalty_card_member_file_to_be_picked_up_search(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    loyalty_card_validator = CardStatus.objects.all()
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        loyalty_card_member = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
                                                         Q(surname__contains=searched.capitalize()) |
                                                         Q(member_nr__contains=searched) |
                                                         Q(phone_number__contains=searched))
        return render(request,
                      'TI_Management_app/loyalty_card_member_file_to_be_picked_up_search.html',
                      {'searched': searched,
                       'loyalty_card_member': loyalty_card_member,
                       'loyalty_card': loyalty_card,
                       'loyalty_card_validator': loyalty_card_validator})
    else:
        return render(request,
                      'TI_Management_app/loyalty_card_member_file_to_be_picked_up_search.html',
                      {})


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
    ordered_card_file = OrderedCardDocument.objects.all()
    if request.method == "POST":
        form = CardStatusEditForm(request.POST, request.FILES, instance=member_loyalty_card)
        if form.is_valid():
            member_loyalty_card = form.save(commit=False)
            member_loyalty_card.author = request.user
            member_loyalty_card.member = member
            member_loyalty_card.date_of_action = timezone.now()
            member_loyalty_card.save()
            messages.success(request, f"Zaktualizowano!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = CardStatusEditForm(instance=member_loyalty_card)
    return render(request, 'TI_Management_app/member_loyalty_card_edit.html',
                  {
                      'form': form,
                      'member': member,
                      'member_loyalty_card': member_loyalty_card,
                      'ordered_card_file': ordered_card_file}
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
    return render(request, 'TI_Management_app/member_loyalty_card_id_edit.html',
                  {
                      'form': form,
                      'member': member,
                      'member_loyalty_card': member_loyalty_card}
                  )


@login_required
def member_loyalty_card_add(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    card_add = get_object_or_404(Cards, pk=pk1)
    if request.method == "POST":
        form = CardStatusForm(request.POST, request.FILES)
        if form.is_valid():
            loyalty_card = form.save(commit=False)
            loyalty_card.author = request.user
            loyalty_card.member = member
            loyalty_card.card = card_add
            loyalty_card.date_of_action = timezone.now()
            loyalty_card.save()
            messages.success(request, "Dodano członka!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        username = request.user.username
        form = CardStatusForm(initial={'responsible': username})
    return render(request, 'TI_Management_app/member_loyalty_card_add.html',
                  {
                      'form': form,
                      'member': member,
                      'card_add': card_add}
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


# @login_required
def groups_list(request):
    groups_obj = Groups.objects.all()

    paginator = Paginator(groups_obj, 5)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    return render(request,
                  'TI_Management_app/groups_list.html',
                  {'page': page,
                   'groups': groups})


@login_required
def group_member_search(request, pk):
    group_available = get_object_or_404(Groups, pk=pk)
    group_validator = GroupsMember.objects.all()
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        group_members = MembersZZTI.objects.filter(Q(forename__contains=searched.capitalize()) |
                                                   Q(surname__contains=searched.capitalize()) |
                                                   Q(member_nr__contains=searched) |
                                                   Q(phone_number__contains=searched))

        # members_without_group = MembersZZTI.objects.filter(groupsMember__isnull=True)
        members_without_group = group_members.exclude(groupsMember__group__pk=pk)

        return render(request,
                      'TI_Management_app/group_member_search.html',
                      {'searched': searched,
                       'group_members': group_members,
                       'group_available': group_available,
                       'group_validator': group_validator,
                       'members_without_group': members_without_group})
    else:
        return render(request,
                      'TI_Management_app/group_member_search.html',
                      {})


@login_required
def groups_add(request):
    if request.method == "POST":
        form = GroupsForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.author = request.user
            group.save()
            messages.success(request, f"Dodano nową grupe {group.group_name}!")
            return redirect('TI_Management_app:groups_list')
    else:
        form = GroupsForm()
    return render(request, 'TI_Management_app/groups_add.html', {'form': form})


@login_required
def groups_edit(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    if request.method == "POST":
        form = GroupsEditForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.author = request.user
            group.save()
            messages.success(request, f"Zaktualizowano grupe {group.group_name}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form = GroupsEditForm(instance=group)
    return render(request, 'TI_Management_app/groups_edit.html',
                  {'form': form,
                   'group': group})


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

    return render(request, 'TI_Management_app/group_detail.html',
                  {'group': group,
                   'form_gender': form_gender,
                   'form_role': form_role,
                   # 'form_occupation': form_occupation,
                   'form_export': form_export})


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
    return render(request, 'TI_Management_app/group_file_edit.html',
                  {
                      'form': form,
                      'group': group})


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
            group_notepad = form.save(commit=False)
            group_notepad.author = request.user
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
        'TI_Management_app/group_notepad_add.html',
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
            group_notepad = form.save(commit=False)
            group_notepad.author = request.user
            group_notepad.group = group
            group_notepad.published_date = timezone.now()
            group_notepad.save()
            messages.success(request, f"Zaktualizowano notatkę grupy {group_notepad.group}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form = GroupNotepadForm(instance=notepad)
    return render(
        request,
        'TI_Management_app/group_notepad_edit.html',
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
        'TI_Management_app/group_notepad_history.html',
        {
            'group': group,
            'group_notepad_history_obj': group_notepad_history_obj,
            'notepad': notepad
        }
    )


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


def group_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        groups = Groups.objects.filter(Q(group_name__contains=searched))
        return render(request,
                      'TI_Management_app/group_search.html',
                      {'searched': searched,
                       'groups': groups})
    else:
        return render(request,
                      'TI_Management_app/group_search.html',
                      {})


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
    return render(request, 'TI_Management_app/member_group_add.html',
                  {
                      'form': form,
                      'member': member,
                      'group': group}
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
            messages.success(request, f"Dodano nowego uczestnika do grupy{group_member.member}!")
            return redirect('TI_Management_app:group_detail', pk=group.pk)
    else:
        form = GroupAddMemberForm(initial={'group': group})
    return render(request, 'TI_Management_app/group_add_member.html',
                  {'form': form, 'group': group, 'member': member})


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
            notepad = form.save(commit=False)
            notepad.author = request.user
            notepad.member = member
            notepad.published_date = timezone.now()
            notepad.save()
            messages.success(request, f"Dodano notatkę {notepad.title}!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        username = request.user.username
        form = NotepadMemberForm(initial={'responsible': username})
    return render(request, 'TI_Management_app/member_notepad_add.html',
                  {
                      'form': form,
                      'member': member}
                  )


@login_required
def member_notepad_edit(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    notepad = get_object_or_404(Notepad, pk=pk1)
    if request.method == "POST":
        form = NotepadMemberForm(request.POST, request.FILES)
        if form.is_valid():
            notepad = form.save(commit=False)
            notepad.author = request.user
            notepad.member = member
            notepad.published_date = timezone.now()
            notepad.save()
            messages.success(request, f"Zaktualizowano notatkę {notepad.title}!")
            return redirect('TI_Management_app:member_detail', pk=member.pk)
    else:
        form = NotepadMemberForm(instance=notepad)
    return render(request, 'TI_Management_app/member_notepad_edit.html',
                  {
                      'form': form,
                      'member': member,
                      'notepad': notepad}
                  )


@login_required
def member_notepad_history(request, pk, title):
    member = MembersZZTI.objects.get(id=pk)
    member_notepad_history_obj = (member.notepad.filter(
        Q(published_date__lte=timezone.now()) &
        Q(title__contains=title)
    ).order_by('-published_date'))

    return render(request, 'TI_Management_app/member_notepad_history.html',
                  {'member': member,
                   'member_notepad_history_obj': member_notepad_history_obj,
                   'title': title})


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

    return FileResponse(buf, as_attachment=True, filename=f"HistoriaKomunikacji-{member.forename} {member.surname}.pdf")


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
        'TI_Management_app/documents_database_category.html',
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
        'TI_Management_app/documents_database_category_edit.html',
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
        'TI_Management_app/documents_database.html',
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
        'TI_Management_app/documents_database_edit.html',
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
            Q(title__contains=searched) |
            Q(file__contains=searched) |
            Q(category__title__contains=searched)
        )
        return render(
            request,
            'TI_Management_app/documents_database_search.html',
            {
                'searched': searched,
                'documents': documents
            }
        )
    else:
        return render(
            request,
            'TI_Management_app/documents_database_search.html',
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
def finance_list(request):
    members_obj = MembersZZTI.objects.all().order_by('-created_date')
    paginator = Paginator(members_obj, 50)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)
    return render(request,
                  'TI_Management_app/members_list.html',
                  {'page': page,
                   'members': members})


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
        return render(request,
                      'TI_Management_app/finance/register_relief_step_one_search.html',
                      {'searched': searched,
                       'members': members})
    else:
        return render(request,
                      'TI_Management_app/finance/register_relief_step_one_search.html',
                      {})


@login_required
def register_relief_step_two(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberEditReliefForm(request.POST, instance=member)
        if form.is_valid():
            address_member = form.save(commit=False)
            address_member.author = request.user
            address_member.save()
            messages.success(
                request,
                f"1/4 - Zaktualizowano adres {member.forename} {member.surname}!"
            )
            return redirect('TI_Management_app:register_relief_step_three', pk=member.pk)
    else:
        form = MemberEditReliefForm(instance=member)
        # form = MemberEditReliefForm()
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
            register_relife = form.save(commit=False)
            register_relife.author = request.user
            register_relife.member = member
            register_relife.save()
            messages.success(request, "2/4 - Walidacja zapomogi!")
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


@login_required
def register_relief_step_five(request, pk):
    one_registered_relife = get_object_or_404(RegisterRelief, pk=pk)
    member = one_registered_relife.member

    if request.method == "POST":
        form = CardRegisterReliefForm(request.POST, instance=member)

        if form.is_valid():
            if member.card is form.cleaned_data['card']:
                one_registered_relife.complete = True
                one_registered_relife.date_of_signed_by_the_applicant = timezone.now()
                one_registered_relife.save()

                messages.success(request, "4/4 - Dodano domumenty do zapomogi!")
                return redirect('TI_Management_app:register_relief_valid', pk=one_registered_relife.pk)
    else:
        # form = CardRegisterReliefForm(instance=member)
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
            'relief': relief
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
        return render(request,
                      'TI_Management_app/finance/relief_status_list_search.html',
                      {})


@login_required
def relief_status_to_be_signed(request, pk):
    relief_to_be_signed = get_object_or_404(RegisterRelief, pk=pk)

    if request.method == "POST":
        form = SignatureReliefForm(request.POST)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.author = request.user
            # signature.member = member
            signature.save()
            messages.success(request, "Dodano podpis!")
            return redirect('TI_Management_app:relief_status_to_be_signed', pk=relief_to_be_signed.pk)
    else:
        form = SignatureReliefForm()

    return render(
        request,
        'TI_Management_app/finance/relief_status_to_be_signed.html',
        {
            'form': form,
            'relief_to_be_signed': relief_to_be_signed
        }
    )
