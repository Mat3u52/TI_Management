from django.contrib import admin
from django.utils.html import format_html
from .models import Groups, Cards, CardsRFID, CardStatus, MembersZZTI, Notepad, Application

admin.site.site_header = 'Admin Panel TI Management'

# admin.site.register(Groups)
# admin.site.register(CardsRFID)
# admin.site.register(Cards)
# admin.site.register(CardStatus)
# admin.site.register(MembersZZTI)
# admin.site.register(Notepad)
admin.site.register(Application)


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('group_name', 'created_date')
    list_filter = ('group_name', 'created_date')
    search_fields = ('group_name',)
    date_hierarchy = 'created_date'


@admin.register(CardsRFID)
class CardsRFIDAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('username', 'serial_number', 'created_date')
    list_filter = ('username', 'serial_number', 'created_date')
    search_fields = ('serial_number',)
    date_hierarchy = 'created_date'


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('card_name', 'created_date')
    list_filter = ('card_name', 'created_date')
    search_fields = ('card_name',)
    date_hierarchy = 'created_date'


@admin.register(CardStatus)
class CardStatusAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('card', 'card_identity', 'card_status', 'created_date')
    list_filter = ('card', 'card_identity', 'card_status', 'created_date')
    search_fields = ('card_identity', 'card_status')
    # raw_id_fields = ('author',)
    date_hierarchy = 'created_date'
    # ordering = ('card_identity', 'created_date')


@admin.register(MembersZZTI)
class MembersZZTIAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" width="50px"/>'.format(obj.image.url))
        except:
            pass
    image_tag.short_description = 'Image'

    list_display = ('id', 'forename', 'surname', 'sex', 'phone_number', 'email', 'date_of_accession',
                    'date_of_abandonment', 'type_of_contract', 'date_of_contract', 'group',
                    'card_rfid', 'card_status', 'image_tag', 'created_date')
    list_filter = ('id', 'forename', 'surname', 'sex', 'phone_number', 'email', 'date_of_accession',
                   'date_of_abandonment', 'type_of_contract', 'date_of_contract', 'group',
                   'card_rfid', 'card_status', 'created_date')
    search_fields = ('surname',)
    date_hierarchy = 'created_date'


@admin.register(Notepad)
class NotepadAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('title', 'published_date', 'importance', 'status', 'member', 'file', 'created_date')
    list_filter = ('title', 'published_date', 'importance', 'status', 'member', 'file', 'created_date')
    search_fields = ('title',)
    date_hierarchy = 'created_date'
