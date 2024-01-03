from django.urls import path
from . import views
# from .views import MemberFileView

urlpatterns = [
    path('', views.members_list, name='members_list'),
    path('TI_Management_app/<int:pk>/', views.member_detail, name='member_detail'),
    path('TI_Management_app/new/', views.member_new, name='member_new'),
    path('TI_Management_app/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('TI_Management_app/<int:pk>/editCard/', views.member_card_edit, name='member_card_edit'),
    # path('TI_Management_app/<int:pk>/editFile/', MemberFileView.as_view(), name='member_file_edit'),
    path('TI_Management_app/<int:pk>/editFile/', views.member_file_edit, name='member_file_edit'),
    path('TI_Management_app/<int:pk>/deleteFile/<int:pk1>/', views.member_file_delete, name='member_file_delete'),
    path('TI_Management_app/<int:pk>/editLoyaltyCard/', views.member_loyalty_card_edit, name='member_loyalty_card_edit'),
    path('TI_Management_app/member_search/', views.member_search, name='member_search'),
]
