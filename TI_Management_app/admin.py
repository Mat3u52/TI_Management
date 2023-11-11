from django.contrib import admin
from .models import Groups, Cards, CardsRFID, CardStatus, MembersZZTI

# admin.site.register(Groups)
# admin.site.register(CardsRFID)
# admin.site.register(Cards)
# admin.site.register(CardStatus)
admin.site.register(MembersZZTI)
admin.site.site_header = 'Admin Panel TI Management'


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'created_date')
    list_filter = ('group_name', 'created_date')
    search_fields = ('group_name',)
    date_hierarchy = 'created_date'


@admin.register(CardsRFID)
class CardsRFIDAdmin(admin.ModelAdmin):
    list_display = ('username', 'serial_number', 'created_date')
    list_filter = ('username', 'serial_number', 'created_date')
    search_fields = ('serial_number',)
    date_hierarchy = 'created_date'


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'created_date')
    list_filter = ('card_name', 'created_date')
    search_fields = ('card_name',)
    date_hierarchy = 'created_date'


@admin.register(CardStatus)
class CardStatusAdmin(admin.ModelAdmin):
    list_display = ('card_identity', 'card_status', 'created_date')
    list_filter = ('card_identity', 'card_status', 'created_date')
    search_fields = ('card_identity', 'card_status')
    # raw_id_fields = ('author',)
    date_hierarchy = 'created_date'
    # ordering = ('card_identity', 'created_date')
