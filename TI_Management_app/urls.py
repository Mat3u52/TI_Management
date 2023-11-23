from django.urls import path
from . import views

urlpatterns = [
    path('', views.members_list, name='members_list'),
]
