from django.contrib import admin
from django.utils.html import format_html
from .models import Groups, Cards, CardsRFID, CardStatus, MembersZZTI, Notepad, Application, Task, GroupsMember

admin.site.site_header = 'Panel Administratora zzti LUMS'

# admin.site.register(Groups)
# admin.site.register(CardsRFID)
# admin.site.register(Cards)
# admin.site.register(CardStatus)
# admin.site.register(MembersZZTI)
# admin.site.register(Notepad)
# admin.site.register(Application)
# admin.site.register(Task)


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


@admin.register(GroupsMember)
class GroupsMemberAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('member', 'group', 'created_date')
    list_filter = ('member', 'group', 'created_date')
    search_fields = ('group',)
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

    list_display = ('card', 'card_identity', 'card_status', 'date_of_action', 'created_date')
    list_filter = ('card', 'card_identity', 'card_status', 'date_of_action', 'created_date')
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

    list_display = ('id', 'forename', 'surname', 'sex', 'birthday', 'birthplace', 'pin', 'phone_number', 'email',
                    'date_of_accession',
                    'date_of_abandonment', 'type_of_contract', 'date_of_contract', 'group', 'card',
                    'image_tag', 'created_date')
    list_filter = ('id', 'forename', 'surname', 'sex', 'birthday', 'birthplace', 'pin', 'phone_number', 'email',
                   'date_of_accession',
                   'date_of_abandonment', 'type_of_contract', 'date_of_contract', 'group', 'card',
                   'created_date')
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


# class MembersZZTIInline(admin.TabularInline):
#     model = MembersZZTI


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # inlines = [
    #     MembersZZTIInline
    # ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('kind_of_application', 'date_of_application', 'date_of_payout', 'member', 'created_date')
    list_filter = ('kind_of_application', 'date_of_application', 'date_of_payout', 'member', 'created_date')
    search_fields = ('kind_of_application',)
    date_hierarchy = 'created_date'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('task_name', 'category', 'deadline', 'frequency', 'member', 'importance', 'status', 'created_date')
    list_filter = ('task_name', 'category', 'deadline', 'frequency', 'member', 'importance', 'status', 'created_date')
    search_fields = ('task_name',)
    date_hierarchy = 'created_date'

