from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import MembersZZTI
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import MemberForm
from django.views.generic import DetailView
from django.views.generic import TemplateView


class Image(TemplateView):
    form = MemberForm
    template_name = 'TI_Management_app/image.html'

    def members(self, request, *args, **kwargs):
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.members(request, *args, **kwargs)


class ImageDisplay(DetailView):
    model = MembersZZTI
    template_name = 'TI_Management_app/image_display.html'
    context_object_name = 'image'

