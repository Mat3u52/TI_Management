from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import MembersZZTI, MembersFile, CardStatus, GroupsMember, Notepad, Groups, Cards, OrderedCardDocument, ToBePickedUpCardDocument
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import (MemberForm, MemberFileForm, CardStatusForm, GroupsMemberForm, NotepadMemberForm,
                    GroupsForm, GroupsEditForm, GroupAddMemberForm,
                    LoyaltyCardForm, LoyaltyCardAddMemberForm,
                    LoyaltyCardsAddMemberFileOrderForm,
                    LoyaltyCardsAddMemberFileToBePickedUpForm,
                    OrderedCardDocumentForm,
                    ToBePickedUpCardDocumentForm)
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


class Image(TemplateView):
    form = MemberForm
    template_name = 'TI_Management_app/image.html'

    def member(self, request, *args, **kwargs):
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.member(request, *args, **kwargs)


class ImageDisplay(DetailView):
    model = MembersZZTI
    template_name = 'TI_Management_app/image_display.html'
    context_object_name = 'image'


def members_list(request):
    members_obj = MembersZZTI.objects.all()

    paginator = Paginator(members_obj, 3)
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
    # return render(request, 'TI_Management_app/members_list.html', {'members': members})


def member_detail(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    accessible = Cards.objects.all()
    accessible_ids = accessible.values_list('id', flat=True)
    user_cards = CardStatus.objects.filter(member_id=pk, card__isnull=False)
    card_names = user_cards.values_list('card', flat=True).distinct()
    different_elements = set(accessible_ids).difference(set(card_names))
    # accessed = get_object_or_404(Cards, pk__in=different_elements)

    return render(request, 'TI_Management_app/member_detail.html',
                  {'member': member,
                   'accessible_ids': accessible_ids,
                   'card_names': card_names,
                   'different_elements': different_elements,
                   'accessible': accessible})


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
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm()
    return render(request, 'TI_Management_app/member_new.html', {'form': form})


@login_required
def member_edit(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            # member.save(update_fields=['forename'])
            member.save()
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'TI_Management_app/member_edit.html', {'form': form,
                                                                  'member': member})


@login_required
def member_card_edit(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            member.save()
            return redirect('member_detail', pk=member.pk)
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
        members = MembersZZTI.objects.filter(Q(forename__contains=searched) |
                                             Q(surname__contains=searched) |
                                             Q(member_nr__contains=searched))
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
            member_file.member = member
            member_file.author = request.user
            member_file.save()
            return redirect('member_detail', pk=member.pk)
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
    return redirect('member_detail', pk=member.pk)


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
        loyalty_card_member = MembersZZTI.objects.filter(Q(forename__contains=searched) |
                                                         Q(surname__contains=searched) |
                                                         Q(member_nr__contains=searched))
        return render(request,
                      'TI_Management_app/loyalty_card_member_search.html',
                      {'searched': searched,
                       'loyalty_card_member': loyalty_card_member,
                       'loyalty_card': loyalty_card,
                       'loyalty_card_validator': loyalty_card_validator})
    else:
        return render(request,
                      'TI_Management_app/loyalty_card_member_search.html',
                      {})


def loyalty_card_detail(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    status_card_file = CardStatus.objects.order_by('-file_date')
    status_card_file_a = CardStatus.objects.order_by('-file_a_date')
    ordered_card_file = OrderedCardDocument.objects.all()
    to_be_picked_up_doc_card_file = ToBePickedUpCardDocument.objects.all()
    return render(request, 'TI_Management_app/loyalty_card_detail.html',
                  {'loyalty_card': loyalty_card,
                   'status_card_file': status_card_file,
                   'status_card_file_a': status_card_file_a,
                   'ordered_card_file': ordered_card_file,
                   'to_be_picked_up_doc_card_file': to_be_picked_up_doc_card_file})


@login_required
def loyalty_card_add(request):
    if request.method == "POST":
        form = LoyaltyCardForm(request.POST)
        if form.is_valid():
            loyalty_card = form.save(commit=False)
            loyalty_card.author = request.user
            loyalty_card.save()
            return redirect('loyalty_card_list')
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
            return redirect('loyalty_card_detail', pk=loyalty_card.pk)
    else:
        form = LoyaltyCardForm(instance=loyalty_card)
    return render(request, 'TI_Management_app/loyalty_card_edit.html',
                  {'form': form})


@login_required
def loyalty_card_add_member(request, pk, pk1):
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
            loyalty_card_member.save()
            return redirect('loyalty_card_detail', pk=loyalty_card.pk)
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
            return redirect('loyalty_card_detail', pk=loyalty_card.pk)
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
            return redirect('loyalty_card_detail', pk=loyalty_card.pk)
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
            return redirect('loyalty_card_list')
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
        loyalty_card_member = MembersZZTI.objects.filter(Q(forename__contains=searched) |
                                                         Q(surname__contains=searched) |
                                                         Q(member_nr__contains=searched))
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
            return redirect('loyalty_card_list')
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
        loyalty_card_member = MembersZZTI.objects.filter(Q(forename__contains=searched) |
                                                         Q(surname__contains=searched) |
                                                         Q(member_nr__contains=searched))
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
    return redirect('loyalty_card_detail', pk=loyalty_card.pk)


@login_required
def loyalty_card_delete_all(request, pk):
    loyalty_card = get_object_or_404(Cards, pk=pk)
    loyalty_card.author = request.user

    loyalty_card.delete()

    return redirect('loyalty_card_detail')


def loyalty_cards_export_all_users(request, pk):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=wszyscy_uczestnicy_kary_lojalnosciowej_{timezone.now()}.txt'

    loyalty_card_all_users = get_object_or_404(Cards, pk=pk)

    lines = []
    for loyalty_card_all_user in loyalty_card_all_users.loyaltyCardStatus.all():
        lines.append(f"{loyalty_card_all_user.card};{loyalty_card_all_user.member};"
                     f"{loyalty_card_all_user.member.phone_number};{loyalty_card_all_user.member.email}\n")

    response.writelines(lines)
    return response


def loyalty_cards_export_to_be_picked_up(request, pk):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=karty_do_odbioru_{timezone.now()}.txt'

    loyalty_card_all_users = get_object_or_404(Cards, pk=pk)

    lines = []
    for loyalty_card_all_user in loyalty_card_all_users.loyaltyCardStatus.all():
        if loyalty_card_all_user.card_status == 'toBePickedUp':
            lines.append(f"{loyalty_card_all_user.card};{loyalty_card_all_user.member};"
                         f"{loyalty_card_all_user.member.phone_number};{loyalty_card_all_user.member.email}\n")

    response.writelines(lines)
    return response


def loyalty_cards_export_ordered(request, pk):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=karty_zamowione_{timezone.now()}.txt'

    loyalty_card_all_users = get_object_or_404(Cards, pk=pk)

    lines = []
    for loyalty_card_all_user in loyalty_card_all_users.loyaltyCardStatus.all():
        if loyalty_card_all_user.card_status == 'ordered':
            lines.append(f"{loyalty_card_all_user.card};{loyalty_card_all_user.member};"
                         f"{loyalty_card_all_user.member.phone_number};{loyalty_card_all_user.member.email}\n")

    response.writelines(lines)
    return response


def loyalty_cards_export_to_order(request, pk):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=zlecenia_na_karte_{timezone.now()}.txt'

    loyalty_card_all_users = get_object_or_404(Cards, pk=pk)

    lines = []
    for loyalty_card_all_user in loyalty_card_all_users.loyaltyCardStatus.all():
        if loyalty_card_all_user.card_status == 'toOrder':
            lines.append(f"{loyalty_card_all_user.card};{loyalty_card_all_user.member};"
                         f"{loyalty_card_all_user.member.phone_number};{loyalty_card_all_user.member.email}\n")

    response.writelines(lines)
    return response


def loyalty_cards_export_deactivated(request, pk):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=karty_dezaktywowane_{timezone.now()}.txt'

    loyalty_card_all_users = get_object_or_404(Cards, pk=pk)

    lines = []
    for loyalty_card_all_user in loyalty_card_all_users.loyaltyCardStatus.all():
        if loyalty_card_all_user.card_status == 'deactivated':
            lines.append(f"{loyalty_card_all_user.card};{loyalty_card_all_user.member};"
                         f"{loyalty_card_all_user.member.phone_number};{loyalty_card_all_user.member.email}\n")

    response.writelines(lines)
    return response


@login_required
def member_loyalty_card_edit(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_loyalty_card = get_object_or_404(CardStatus, pk=pk1)
    ordered_card_file = OrderedCardDocument.objects.all()
    if request.method == "POST":
        form = CardStatusForm(request.POST, request.FILES, instance=member_loyalty_card)
        if form.is_valid():
            member_loyalty_card = form.save(commit=False)
            member_loyalty_card.member = member
            member_loyalty_card.author = request.user
            member_loyalty_card.date_of_action = timezone.now()
            member_loyalty_card.save()
            return redirect('member_detail', pk=member.pk)
    else:
        form = CardStatusForm(instance=member_loyalty_card)
    return render(request, 'TI_Management_app/member_loyalty_card_edit.html',
                  {
                      'form': form,
                      'member': member,
                      'member_loyalty_card': member_loyalty_card,
                      'ordered_card_file': ordered_card_file}
                  )


@login_required
def member_loyalty_card_add(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)

    card_add = get_object_or_404(Cards, pk=pk1)

    if request.method == "POST":
        form = CardStatusForm(request.POST, request.FILES)
        if form.is_valid():
            loyalty_card = form.save(commit=False)
            loyalty_card.member = member

            loyalty_card.card = card_add

            loyalty_card.author = request.user
            loyalty_card.date_of_action = timezone.now()
            loyalty_card.save()
            return redirect('member_detail', pk=member.pk)
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
    member_loyalty_card.file.delete()
    member_loyalty_card.card.delete()
    member_loyalty_card.file_a.delete()
    member_loyalty_card.delete()
    return redirect('member_detail', pk=member.pk)


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
def groups_add(request):
    if request.method == "POST":
        form = GroupsForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.author = request.user
            group.save()
            return redirect('groups_list')
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
            return redirect('group_detail', pk=group.pk)
    else:
        form = GroupsEditForm(instance=group)
    return render(request, 'TI_Management_app/groups_edit.html', {'form': form})


def group_detail(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    return render(request, 'TI_Management_app/group_detail.html',
                  {'group': group})


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
def member_group_add(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = GroupsMemberForm(request.POST)
        if form.is_valid():
            loyalty_card = form.save(commit=False)
            loyalty_card.member = member
            loyalty_card.author = request.user
            loyalty_card.save()
            return redirect('member_detail', pk=member.pk)
    else:
        form = GroupsMemberForm()
    return render(request, 'TI_Management_app/member_group_add.html',
                  {
                      'form': form,
                      'member': member}
                  )


@login_required
def group_add_member(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    if request.method == "POST":
        form = GroupAddMemberForm(request.POST)
        if form.is_valid():
            group_member = form.save(commit=False)
            group_member.author = request.user
            group_member.group = group
            group_member.save()
            return redirect('group_detail', pk=group.pk)
    else:
        form = GroupAddMemberForm(initial={'group': group})
    return render(request, 'TI_Management_app/group_add_member.html',
                  {'form': form, 'group': group})


@login_required
def member_group_delete(request, pk, pk1):
    member = get_object_or_404(MembersZZTI, pk=pk)
    member_group = get_object_or_404(GroupsMember, pk=pk1)

    member.author = request.user
    member_group.delete()
    return redirect('member_detail', pk=member.pk)


@login_required
def group_delete_member(request, pk, pk1):
    group = get_object_or_404(Groups, pk=pk)
    member_group = get_object_or_404(GroupsMember, pk=pk1)

    group.author = request.user
    member_group.delete()
    return redirect('group_detail', pk=group.pk)


@login_required
def group_delete_all(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    group.author = request.user

    group.delete()

    return redirect('groups_list')


@login_required
def member_notepad_add(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    if request.method == "POST":
        form = NotepadMemberForm(request.POST, request.FILES)
        if form.is_valid():
            notepad = form.save(commit=False)
            notepad.member = member
            notepad.author = request.user
            notepad.published_date = timezone.now()
            notepad.save()
            return redirect('member_detail', pk=member.pk)
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
            notepad.member = member
            notepad.author = request.user
            notepad.published_date = timezone.now()
            notepad.save()
            return redirect('member_detail', pk=member.pk)
    else:
        form = NotepadMemberForm(instance=notepad)
    return render(request, 'TI_Management_app/member_notepad_edit.html',
                  {
                      'form': form,
                      'member': member,
                      'notepad': notepad}
                  )


@login_required
def member_notepad_history(request, pk):
    member = MembersZZTI.objects.get(id=pk)
    member_notepad_history_obj = member.notepad.filter(published_date__lte=timezone.now()).order_by('-published_date')

    return render(request, 'TI_Management_app/member_notepad_history.html',
                  {'member': member,
                   'member_notepad_history_obj': member_notepad_history_obj})


@login_required
def member_notepad_history_pdf(request, pk):
    member = MembersZZTI.objects.get(id=pk)
    member_notepad_history_obj = member.notepad.filter(published_date__lte=timezone.now()).order_by('-published_date')

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
        # lines.append(history.member)
        lines.append(f"Tytuł: {history.title}")
        lines.append(" ")
        lines.append(f"Opis: {history.content}")
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

    # for line in lines:
    #     textob.textLine(line)
    #     c.getPageNumber()
    #
    # c.drawText(textob)
    # c.showPage()
    # c.save()
    # buf.seek(0)




    y = 10
    for line in lines:
        c.beginText()
        c.setFont("Verdana", 14)

        # textob = c.beginText()
        # textob.setTextOrigin(inch, inch)
        # textob.setFont("Verdana", 14)
        # textob.textLine(line)

        # wraped_text = "\n".join(wrap(line, 80))
        # t.textLines(wraped_text)
        y += 10
        c.drawString(10, y, line)
        c.getPageNumber()
        if "-------" in line:
            c.showPage()
            y = 0

    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f"HistoriaKomunikacji-{member}.pdf")



@login_required
def member_notepad_delete_all(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    # member_group = get_object_or_404(GroupsMember, pk=pk1)
    member.author = request.user

    notepad_obj = MembersZZTI.objects.get(id=pk)
    # todo  notepad_obj.notepad.file.delete()

    notepad_obj.notepad.all().delete()

    return redirect('member_detail', pk=member.pk)




# class MemberFileView(LoginRequiredMixin, CreateView):
#     model = MembersFile
#     form_class = MemberFileForm
#     template_name = 'TI_Management_app/member_file_edit.html'
#
#     def form_valid(self, form):
#         form.instance.member_id = self.kwargs['pk']
#         return super().form_valid(form)
#
#     success_url = reverse_lazy('members_list')


