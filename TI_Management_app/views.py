from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import MembersZZTI
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import MemberForm
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required


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
    members = MembersZZTI.objects.all()
    return render(request, 'TI_Management_app/members_list.html', {'members': members})


def member_detail(request, pk):
    member = get_object_or_404(MembersZZTI, pk=pk)
    return render(request, 'TI_Management_app/member_detail.html', {'member': member})


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
