from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Groups,
    Cards,
    CardsRFID,
    CardStatus,
    MembersZZTI,
    Notepad,
    Application,
    Task,
    GroupsMember,
    MembersFile,
    Activities,
    ActivityStatus,
    Vote,
    Questions,
    Answers,
    OrderedCardDocument,
    ToBePickedUpCardDocument,
    MemberFunction,
    MemberOccupation,
    GroupsFile,
    GroupsNotepad,
    DocumentsDatabase,
    DocumentsDatabaseCategory,
    Relief,
    RelationRegisterRelief,
    RegisterRelief,
    FileRegisterRelief
)

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


@admin.register(DocumentsDatabaseCategory)
class DocumentsDatabaseCategoryAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'created_date',
        'responsible',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'title',
        'created_date',
        'responsible',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(DocumentsDatabase)
class DocumentsDatabaseAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'category',
        'file',
        'created_date',
        'responsible',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'title',
        'category',
        'file',
        'created_date',
        'responsible',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'group_name',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    list_filter = (
        'group_name',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    search_fields = (
        'group_name',
    )
    # date_hierarchy = 'created_date'


@admin.register(MemberFunction)
class MemberFunctionAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'member_function',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    list_filter = (
        'member_function',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    search_fields = (
        'member_function',
    )
    # date_hierarchy = 'created_date'


@admin.register(MemberOccupation)
class MemberOccupationAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'member_occupation',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    list_filter = (
        'member_occupation',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    search_fields = (
        'member_occupation',
    )
    # date_hierarchy = 'created_date'


@admin.register(GroupsMember)
class GroupsMemberAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'member',
        'group',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'member',
        'group',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'group',
    )
    # date_hierarchy = 'created_date'


@admin.register(CardsRFID)
class CardsRFIDAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'username',
        'serial_number',
        'created_date'
    )
    list_filter = (
        'username',
        'serial_number',
        'created_date'
    )
    search_fields = (
        'serial_number',
    )
    # date_hierarchy = 'created_date'


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'card_name',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'card_name',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'card_name',
    )
    # date_hierarchy = 'created_date'


@admin.register(CardStatus)
class CardStatusAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'card',
        'member',
        'ordered_doc',
        'to_be_picked_up_doc',
        'card_identity',
        'card_start_pin',
        'card_status',
        'date_of_action',
        'created_date',
        'file_name',
        'file',
        'file_date',
        'file_name_a',
        'file_a',
        'file_a_date',
        'responsible',
        'confirmed',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'card',
        'member',
        'ordered_doc',
        'to_be_picked_up_doc',
        'card_identity',
        'card_start_pin',
        'card_status',
        'date_of_action',
        'created_date',
        'file_name',
        'file',
        'file_date',
        'file_name_a',
        'file_a',
        'file_a_date',
        'responsible',
        'confirmed',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'card_identity',
        'card_status'
    )
    # date_hierarchy = 'created_date'


@admin.register(MembersZZTI)
class MembersZZTIAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" width="50px"/>'.format(obj.image.url))
        except:
            pass
    image_tag.short_description = 'Image'

    list_display = (
        'id',
        'forename',
        'surname',
        'role',
        'occupation',
        'member_nr',
        'sex',
        'birthday',
        'birthplace',
        'pin',
        'phone_number',
        'email',
        'date_of_accession',
        'date_of_abandonment',
        'type_of_contract',
        'date_of_contract',
        'expiration_date_contract',
        'group',
        'card',
        'image_tag',
        'deactivate',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    list_filter = (
        'id',
        'forename',
        'surname',
        'role',
        'occupation',
        'member_nr',
        'sex',
        'birthday',
        'birthplace',
        'pin',
        'phone_number',
        'email',
        'date_of_accession',
        'expiration_date_contract',
        'date_of_abandonment',
        'type_of_contract',
        'date_of_contract',
        'group',
        'card',
        'deactivate',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    search_fields = (
        'surname',
    )
    # date_hierarchy = 'created_date'


@admin.register(MembersFile)
class MembersFileAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'member',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'member',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(GroupsFile)
class GroupsFileAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'group',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'group',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(GroupsNotepad)
class GroupsNotepadAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'published_date',
        'importance',
        'method',
        'status',
        'group',
        'responsible',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'title',
        'published_date',
        'importance',
        'method',
        'status',
        'group',
        'responsible',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(Notepad)
class NotepadAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'published_date',
        'importance',
        'method',
        'status',
        'member',
        'responsible',
        'file',
        'created_date',
        'confirmed'
    )
    list_filter = (
        'title',
        'published_date',
        'importance',
        'method',
        'status',
        'member',
        'responsible',
        'file',
        'created_date',
        'confirmed'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'kind_of_application',
        'date_of_application',
        'date_of_payout',
        'member',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'kind_of_application',
        'date_of_application',
        'date_of_payout',
        'member',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'kind_of_application',
    )
    # date_hierarchy = 'created_date'


@admin.register(Activities)
class CardsActivitiesAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'capacity',
        'expiring_date',
        'created_date'
    )
    list_filter = (
        'title',
        'capacity',
        'expiring_date',
        'created_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(ActivityStatus)
class CardsActivityStatusAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'activities',
        'member',
        'activity_status',
        'description',
        'spend',
        'assigned_date',
        'created_date'
    )
    list_filter = (
        'activities',
        'member',
        'activity_status',
        'description',
        'spend',
        'assigned_date',
        'created_date'
    )
    search_fields = (
        'activities',
    )
    # date_hierarchy = 'created_date'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'task_name',
        'category',
        'deadline',
        'frequency',
        'member',
        'importance',
        'status',
        'created_date'
    )
    list_filter = (
        'task_name',
        'category',
        'deadline',
        'frequency',
        'member',
        'importance',
        'status',
        'created_date'
    )
    search_fields = (
        'task_name',
    )
    # date_hierarchy = 'created_date'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'description',
        'date_start',
        'date_end',
        'importance',
    )
    list_filter = (
        'title',
        'description',
        'date_start',
        'date_end',
        'importance',
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'question',
        'id',
    )
    list_filter = (
        'question',
        'id',
    )
    search_fields = (
        'question',
    )
    # date_hierarchy = 'created_date'


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'answer',
        'status',
        'status_description',
    )
    list_filter = (
        'answer',
        'status',
        'status_description',
    )
    search_fields = (
        'answer',
    )
    # date_hierarchy = 'created_date'


@admin.register(OrderedCardDocument)
class OrderedCardDocumentAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'card',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'card',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(ToBePickedUpCardDocument)
class ToBePickedUpCardDocumentAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'card',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'card',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(Relief)
class ReliefAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'figure',
        'grace',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'title',
        'figure',
        'grace',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    search_fields = (
        'title',
    )
    # date_hierarchy = 'created_date'


@admin.register(RelationRegisterRelief)
class RelationRegisterReliefAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title'
    )
    search_fields = (
        'title',
    )


@admin.register(RegisterRelief)
class RegisterReliefAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'member',
        'relief',
        'relation',
        'associate_forename',
        'associate_surname',
        'account_number',
        'date_of_completing_the_application',
        'date_of_receipt_the_application',
        'date_of_accident'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'member',
        'relief',
        'relation',
        'associate_forename',
        'associate_surname',
        'account_number',
        'date_of_completing_the_application',
        'date_of_receipt_the_application',
        'date_of_accident'
    )
    search_fields = (
        'relief',
    )


@admin.register(FileRegisterRelief)
class FileRegisterReliefAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title',
        'file'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title',
        'file'
    )
    search_fields = (
        'title',
    )

