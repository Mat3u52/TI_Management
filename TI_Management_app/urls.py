from django.urls import path
from . import views

urlpatterns = [
    path('', views.members_list, name='members_list'),
    path('TI_Management_app/<int:pk>/', views.member_detail, name='member_detail'),
]
