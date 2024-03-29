from django.urls import path
from . import views

app_name = 'TI_Management_app'

urlpatterns = [
    path(
        '',
        views.members_list,
        name='members_list'
    ),
    path(
        'TI_Management_app/members-table-list/',
        views.members_table_list,
        name='members_table_list'
    ),
    path(
        'TI_Management_app/members-list-export-csv/',
        views.member_export_csv,
        name='member_export_csv'
    ),
    path(
        'TI_Management_app/<int:pk>/',
        views.member_detail,
        name='member_detail'
    ),
    path(
        'TI_Management_app/new/',
        views.member_new,
        name='member_new'
    ),
    path(
        'TI_Management_app/member-function-add/',
        views.member_function_add,
        name='member_function_add'
    ),
    path(
        'TI_Management_app/member-function-edit/<int:pk>/',
        views.member_function_edit,
        name='member_function_edit'
    ),
    path(
        'TI_Management_app/member-occupation-add/',
        views.member_occupation_add,
        name='member_occupation_add'
    ),
    path(
        'TI_Management_app/member-occupation-edit/<int:pk>/',
        views.member_occupation_edit,
        name='member_occupation_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/edit/',
        views.member_edit,
        name='member_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-card/',
        views.member_card_edit,
        name='member_card_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/member-deactivate/',
        views.member_deactivate,
        name='member_deactivate'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-file/',
        views.member_file_edit,
        name='member_file_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/delete-file/<int:pk1>/',
        views.member_file_delete,
        name='member_file_delete'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-loyalty-card-add/<int:pk1>/',
        views.member_loyalty_card_add,
        name='member_loyalty_card_add'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-loyalty-card-edit/<int:pk1>/',
        views.member_loyalty_card_edit,
        name='member_loyalty_card_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-loyalty-card-id-edit/<int:pk1>/',
        views.member_loyalty_card_id_edit,
        name='member_loyalty_card_id_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-loyalty-card-delete/<int:pk1>/',
        views.member_loyalty_card_delete,
        name='member_loyalty_card_delete'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-member-group-add/<int:pk1>/',
        views.member_group_add,
        name='member_group_add'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-group-delete/<int:pk1>/',
        views.member_group_delete,
        name='member_group_delete'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-member-Notepad-add/',
        views.member_notepad_add,
        name='member_notepad_add'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-member-notepad-edit/<int:pk1>/',
        views.member_notepad_edit,
        name='member_notepad_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-member-notepad-history/<str:title>/',
        views.member_notepad_history,
        name='member_notepad_history'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-member-notepad-history-pdf/<str:title>/',
        views.member_notepad_history_pdf,
        name='member_notepad_history_pdf'
    ),
    path(
        'TI_Management_app/<int:pk>/edit-member-notepad-delete-all/',
        views.member_notepad_delete_all,
        name='member_notepad_delete_all'
    ),
    path(
        'TI_Management_app/member-search/',
        views.member_search,
        name='member_search'
    ),
    path(
        'TI_Management_app/groups/',
        views.groups_list,
        name='groups_list'
    ),
    path(
        'TI_Management_app/group-detail/<int:pk>/',
        views.group_detail,
        name='group_detail'
    ),
    path(
        'TI_Management_app/group-detail/<int:pk>/group-notepad-add/',
        views.group_notepad_add,
        name='group_notepad_add'
    ),
    path(
        'TI_Management_app/group-detail/<int:pk>/group-notepad-edit/<int:pk1>/',
        views.group_notepad_edit,
        name='group_notepad_edit'
    ),
    path(
        'TI_Management_app/<int:pk>/group-notepad-history/<int:pk1>/',
        views.group_notepad_history,
        name='group_notepad_history'
    ),
    path(
        'TI_Management_app/<int:pk>/group-notepad-history-pdf/<int:pk1>/',
        views.group_notepad_history_pdf,
        name='group_notepad_history_pdf'
    ),
    path(
        'TI_Management_app/group-detail/<int:pk>/edit-file/',
        views.group_file_edit,
        name='group_file_edit'
    ),
    path(
        'TI_Management_app/group-detail/<int:pk>/delete-file/<int:pk1>/',
        views.group_file_delete,
        name='group_file_delete'
    ),
    path(
        'TI_Management_app/group-member-search/<int:pk>/',
        views.group_member_search,
        name='group_member_search'
    ),
    path(
        'TI_Management_app/groups-add/',
        views.groups_add,
        name='groups_add'
    ),
    path(
        'TI_Management_app/group-edit/<int:pk>/',
        views.groups_edit,
        name='groups_edit'
    ),
    path(
        'TI_Management_app/group-add-member/<int:pk>/<int:pk1>/',
        views.group_add_member,
        name='group_add_member'
    ),
    path(
        'TI_Management_app/group-delete/<int:pk>/',
        views.group_delete_all,
        name='group_delete_all'
    ),
    path(
        'TI_Management_app/group-detail/<int:pk>/group-delete-member/<int:pk1>/',
        views.group_delete_member,
        name='group_delete_member'
    ),
    path(
        'TI_Management_app/group-search/',
        views.group_search,
        name='group_search'
    ),
    path(
        'TI_Management_app/loyalty-cards-list/',
        views.loyalty_card_list,
        name='loyalty_card_list'
    ),
    path(
        'TI_Management_app/loyalty-cards-detail/<int:pk>/<str:category>/',
        views.loyalty_card_detail,
        name='loyalty_card_detail'
    ),
    path(
        'TI_Management_app/loyalty/cards/add/',
        views.loyalty_card_add,
        name='loyalty_card_add'
    ),
    path(
        'TI_Management_app/loyalty-cards-edit/<int:pk>/',
        views.loyalty_card_edit,
        name='loyalty_card_edit'
    ),
    path(
        'TI_Management_app/loyalty-cards-add-member/<int:pk>/<int:pk1>/',
        views.loyalty_card_add_member,
        name='loyalty_card_add_member'
    ),
    path(
        'TI_Management_app/loyalty-cards-detail/<int:pk>/loyalty-cards-delete-member/<int:pk1>/',
        views.loyalty_card_delete_member,
        name='loyalty_card_delete_member'
    ),
    path(
        'TI_Management_app/loyalty-cards-add-file-order/<int:pk>/',
        views.loyalty_cards_add_file_order,
        name='loyalty_cards_add_file_order'
    ),
    path(
        'TI_Management_app/loyalty-cards-add-file-to-be-picked-up/<int:pk>/',
        views.loyalty_cards_add_file_to_be_picked_up,
        name='loyalty_cards_add_file_to_be_picked_up'
    ),
    path(
        'TI_Management_app/loyalty-cards-add-member-file-order/<int:pk>/',
        views.loyalty_cards_add_member_file_order,
        name='loyalty_cards_add_member_file_order'
    ),
    path(
        'TI_Management_app/loyalty-cards-add-member-file-order-search/<int:pk>/',
        views.loyalty_card_member_file_order_search,
        name='loyalty_card_member_file_order_search'
    ),
    path(
        'TI_Management_app/loyalty-cards-add-member-file-to-be-picked-up/<int:pk>/',
        views.loyalty_cards_add_member_file_to_be_picked_up,
        name='loyalty_cards_add_member_file_to_be_picked_up'
    ),
    path(
        'TI_Management_app/loyalty-cards-add-member-file-to-be-picked-up-search/<int:pk>/',
        views.loyalty_card_member_file_to_be_picked_up_search,
        name='loyalty_card_member_file_to_be_picked_up_search'
    ),
    path(
        'TI_Management_app/loyalty-cards-member-search/<int:pk>/',
        views.loyalty_card_member_search,
        name='loyalty_card_member_search'
    ),
    path(
        'TI_Management_app/loyalty-cards-search/',
        views.loyalty_card_search,
        name='loyalty_card_search'
    ),
    path(
        'TI_Management_app/documents-database/',
        views.documents_database,
        name='documents_database'
    ),
    path(
        'TI_Management_app/documents-database-edit/<int:pk>/',
        views.documents_database_edit,
        name='documents_database_edit'
    ),
    path(
        'TI_Management_app/documents-database-delete/<int:pk>/',
        views.documents_database_delete,
        name='documents_database_delete'
    ),
    path(
        'TI_Management_app/documents-database-search/',
        views.documents_database_search,
        name='documents_database_search'
    ),
    path(
        'TI_Management_app/documents-database-category/',
        views.documents_database_category,
        name='documents_database_category'
    ),
    path(
        'TI_Management_app/documents-database-category-edit/<int:pk>/',
        views.documents_database_category_edit,
        name='documents_database_category_edit'
    ),
    path(
        'TI_Management_app/documents-database-category-delete/<int:pk>/',
        views.documents_database_category_delete,
        name='documents_database_category_delete'
    ),
    path(
        'TI_Management_app/finance-list/',
        views.finance_list,
        name='finance_list'
    ),
    path(
        'TI_Management_app/relife-figure-add/',
        views.relief_figure_add,
        name='relief_figure_add'
    ),
    path(
        'TI_Management_app/relife-figure-edit/<int:pk>/',
        views.relief_figure_edit,
        name='relief_figure_edit'
    ),
    path(
        'TI_Management_app/relife-figure-delete/<int:pk>/',
        views.relief_figure_delete,
        name='relief_figure_delete'
    ),
    path(
        'TI_Management_app/relation-register-relief-add/',
        views.relation_register_relief_add,
        name='relation_register_relief_add'
    ),
    path(
        'TI_Management_app/relation-register-relief-edit/<int:pk>/',
        views.relation_register_relief_edit,
        name='relation_register_relief_edit'
    ),
    path(
        'TI_Management_app/relation-register-relief-delete/<int:pk>/',
        views.relation_register_relief_delete,
        name='relation_register_relief_delete'
    ),
    path(
        'TI_Management_app/register-relief-step-one/',
        views.register_relief_step_one,
        name='register_relief_step_one'
    ),
    path(
        'TI_Management_app/register-relief-step-one-search/',
        views.register_relief_step_one_search,
        name='register_relief_step_one_search'
    ),
    path(
        'TI_Management_app/finance/register-relief-step-one/<int:pk>/',
        views.register_relief_step_two,
        name='register_relief_step_two'
    ),
    path(
        'TI_Management_app/finance/register-relief-step-three/<int:pk>/',
        views.register_relief_step_three,
        name='register_relief_step_three'
    ),
    path('TI_Management_app/get-author-details/',
         views.get_relief_details,
         name='get_relief_details'),
    path(
        'TI_Management_app/finance/register-relief-step-four/<int:pk>/',
        views.register_relief_step_four,
        name='register_relief_step_four'
    ),
    path(
        'TI_Management_app/finance/register-relief-step-five/<int:pk>/',
        views.register_relief_step_five,
        name='register_relief_step_five'
    ),
    path(
        'TI_Management_app/finance/register-relief-valid/<int:pk>/',
        views.register_relief_valid,
        name='register_relief_valid'
    ),
    path(
        'TI_Management_app/finance/relief-status-list/',
        views.relief_status_list,
        name='relief_status_list'
    ),
    path(
        'TI_Management_app/finance/relief-status-list-search/',
        views.relief_status_list_search,
        name='relief_status_list_search'
    ),
    path(
        'TI_Management_app/finance/relief-status-to-be-signed/<int:pk>/',
        views.relief_status_to_be_signed,
        name='relief_status_to_be_signed'
    ),
    path(
        'TI_Management_app/finance/relief-confirmed-list/',
        views.relief_confirmed_list,
        name='relief_confirmed_list'
    ),
    path(
        'TI_Management_app/finance/relief-confirmed-list-search/',
        views.relief_confirmed_list_search,
        name='relief_confirmed_list_search'
    ),
]

