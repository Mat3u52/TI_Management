from django.urls import path
from . import views
# from .views import MemberFileView

urlpatterns = [
    path('', views.members_list,
         name='members_list'),
    path('TI_Management_app/<int:pk>/',
         views.member_detail,
         name='member_detail'),
    path('TI_Management_app/new/',
         views.member_new,
         name='member_new'),
    path('TI_Management_app/<int:pk>/edit/',
         views.member_edit,
         name='member_edit'),
    path('TI_Management_app/<int:pk>/editCard/',
         views.member_card_edit,
         name='member_card_edit'),
    # path('TI_Management_app/<int:pk>/editFile/', MemberFileView.as_view(), name='member_file_edit'),
    path('TI_Management_app/<int:pk>/editFile/',
         views.member_file_edit,
         name='member_file_edit'),
    path('TI_Management_app/<int:pk>/deleteFile/<int:pk1>/',
         views.member_file_delete,
         name='member_file_delete'),
    path('TI_Management_app/<int:pk>/editLoyaltyCardAdd/',
         views.member_loyalty_card_add,
         name='member_loyalty_card_add'),
    path('TI_Management_app/<int:pk>/editLoyaltyCardEdit/<int:pk1>/',
         views.member_loyalty_card_edit,
         name='member_loyalty_card_edit'),
    path('TI_Management_app/<int:pk>/editLoyaltyCardDelete/<int:pk1>/',
         views.member_loyalty_card_delete,
         name='member_loyalty_card_delete'),
    path('TI_Management_app/<int:pk>/editMemberGroupAdd/',
         views.member_group_add,
         name='member_group_add'),
    path('TI_Management_app/<int:pk>/editGroupDelete/<int:pk1>/',
         views.member_group_delete,
         name='member_group_delete'),
    path('TI_Management_app/<int:pk>/editMemberNotepadAdd/',
         views.member_notepad_add,
         name='member_notepad_add'),
    path('TI_Management_app/<int:pk>/editMemberNotepadEdit/<int:pk1>/',
         views.member_notepad_edit,
         name='member_notepad_edit'),
    path('TI_Management_app/<int:pk>/editMemberNotepadHistory/',
         views.member_notepad_history,
         name='member_notepad_history'),
    path('TI_Management_app/<int:pk>/editMemberNotepadDeleteAll/',
         views.member_notepad_delete_all,
         name='member_notepad_delete_all'),


    path('TI_Management_app/groups/',
         views.groups_list,
         name='groups_list'),
    path('TI_Management_app/groups_add/',
         views.groups_add,
         name='groups_add'),

    path('TI_Management_app/group_edit/<int:pk>',
         views.groups_edit,
         name='groups_edit'),

    path('TI_Management_app/group_add_member/<int:pk>',
         views.group_add_member,
         name='group_add_member'),



    path('TI_Management_app/group_detail/<int:pk>/',
         views.group_detail,
         name='group_detail'),

    path('TI_Management_app/group_delete/<int:pk>/',
         views.group_delete_all,
         name='group_delete_all'),


    path('TI_Management_app/group_detail/<int:pk>/group_delete_member/<int:pk1>',
         views.group_delete_member,
         name='group_delete_member'),


    path('TI_Management_app/group_search/',
         views.group_search,
         name='group_search'),


    path('TI_Management_app/member_search/',
         views.member_search,
         name='member_search'),
]
