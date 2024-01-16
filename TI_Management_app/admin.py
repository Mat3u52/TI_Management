from django.contrib import admin
from django.utils.html import format_html
from .models import (Groups, Cards, CardsRFID, CardStatus,
                     MembersZZTI, Notepad, Application, Task,
                     GroupsMember, MembersFile, Activities, ActivityStatus,
                     Vote, Questions, Answers)

admin.site.site_header = 'Panel Administratora zzti LUMS'

# admin.site.register(Groups)
# admin.site.register(CardsRFID)
# admin.site.register(Cards)
# admin.site.register(CardStatus)
# admin.site.register(MembersZZTI)
# admin.site.register(Notepad)
# admin.site.register(Application)
# admin.site.register(Task)
# admin.site.register(Vote)
# admin.site.register(Question)
# admin.site.register(Answers)


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

    list_display = ('card', 'member', 'card_identity', 'card_start_pin', 'card_status', 'date_of_action',
                    'created_date', 'file_name', 'file', 'file_date', 'file_name_a', 'file_a', 'file_a_date', 'responsible', 'confirmed')
    list_filter = ('card', 'member', 'card_identity', 'card_start_pin', 'card_status', 'date_of_action',
                   'created_date', 'file_name', 'file', 'file_date', 'file_name_a', 'file_a', 'file_a_date', 'responsible', 'confirmed')
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

    list_display = ('id', 'forename', 'surname', 'role', 'occupation', 'member_nr', 'sex', 'birthday', 'birthplace',
                    'pin', 'phone_number', 'email', 'date_of_accession',
                    'date_of_abandonment', 'type_of_contract', 'date_of_contract', 'expiration_date_contract',
                    'group', 'card', 'image_tag', 'created_date')
    list_filter = ('id', 'forename', 'surname', 'role', 'occupation', 'member_nr', 'sex', 'birthday', 'birthplace',
                   'pin', 'phone_number', 'email', 'date_of_accession', 'expiration_date_contract',
                   'date_of_abandonment', 'type_of_contract', 'date_of_contract',
                   'group', 'card', 'created_date')
    search_fields = ('surname',)
    date_hierarchy = 'created_date'


@admin.register(MembersFile)
class MembersFile(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('member', 'title', 'file', 'created_date')
    list_filter = ('member', 'title', 'file', 'created_date')
    search_fields = ('title',)
    date_hierarchy = 'created_date'


@admin.register(Notepad)
class NotepadAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('title', 'published_date', 'importance', 'method', 'status', 'member',
                    'responsible', 'file', 'created_date', 'confirmed')
    list_filter = ('title', 'published_date', 'importance', 'method', 'status', 'member',
                   'responsible', 'file', 'created_date', 'confirmed')
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


@admin.register(Activities)
class CardsActivities(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('title', 'capacity', 'expiring_date', 'created_date')
    list_filter = ('title', 'capacity', 'expiring_date', 'created_date')
    search_fields = ('title',)
    date_hierarchy = 'created_date'


@admin.register(ActivityStatus)
class CardsActivityStatus(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('activities', 'member', 'activity_status', 'description', 'spend', 'assigned_date', 'created_date')
    list_filter = ('activities', 'member', 'activity_status', 'description', 'spend', 'assigned_date', 'created_date')
    search_fields = ('activities',)
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


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('title', 'description', 'date_start', 'date_end', 'importance',)
    list_filter = ('title', 'description', 'date_start', 'date_end', 'importance',)
    search_fields = ('title',)
    date_hierarchy = 'created_date'


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('question', 'id',)
    list_filter = ('question', 'id',)
    search_fields = ('question',)
    date_hierarchy = 'created_date'


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = ('answer', 'status', 'status_description',)
    list_filter = ('answer', 'status', 'status_description',)
    search_fields = ('answer',)
    date_hierarchy = 'created_date'

