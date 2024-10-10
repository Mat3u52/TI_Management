import csv
import datetime
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Groups,
    Cards,
    CardsRFID,
    CardStatus,
    MembersZZTI,
    Notepad,
    # Application,
    Task,
    GroupsMember,
    MembersFile,
    Activities,
    ActivityStatus,
    Vote,
    Poll,
    Choice,
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
    FileRegisterRelief,
    SignatureRelief,
    AverageSalary,
    Scholarships,
    KindOfFinanceDocument,
    KindOfFinanceExpense,
    FileFinance,
    BankStatement,
    VotingSessionKickOff,
    VotingSessionKickOffSignature,
    VotingSessionSignature,
    VotingResponses,
    VoteFile
)
from django.http import HttpResponse

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
# admin.site.register(Poll)
# admin.site.register(Choice)


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Eksport do CSV'


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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
        'street',
        'city',
        'postcode',
        'house_number',
        'float_number',
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
        'author',
        'recommended_by'
    )
    list_filter = (
        'id',
        'forename',
        'surname',
        'street',
        'city',
        'postcode',
        'house_number',
        'float_number',
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
        'author',
        'recommended_by'
    )
    search_fields = (
        'surname',
    )
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):

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
        # 'description',
        'vote_type',
        'vote_method_online',
        'vote_method_offline',
        'date_start',
        'date_end',
        'importance',
        'date_accede',
        'period',
        'min_amount_members',
        'min_amount_commission',
        'turnout'
        # 'members'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title',
        # 'description',
        'vote_type',
        'vote_method_online',
        'vote_method_offline',
        'date_start',
        'date_end',
        'importance',
        'date_accede',
        'period',
        'min_amount_members',
        'min_amount_commission',
        'turnout'
        # 'members'
    )
    search_fields = (
        'title',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'vote',
        'question',
        # 'description',
        'number_of_responses'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'vote',
        'question',
        # 'description',
        'number_of_responses'
    )
    search_fields = (
        'question',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'poll',
        'answer',
        'correct',
        'open_ended_answer'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'poll',
        'answer',
        'correct',
        'open_ended_answer'
    )
    search_fields = (
        'poll',
    )
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
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
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(RelationRegisterRelief)
class RelationRegisterReliefAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'title',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    list_filter = (
        'title',
        'created_date',
        'updated_date',
        'slug',
        'author'
    )
    search_fields = (
        'title',
    )
    actions = [export_to_csv]


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
        'date_of_accident',
        'complete',
        'date_of_signed_by_the_applicant',
        'agreement',
        'payment_confirmation',
        'date_of_payment_confirmation'
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
        'date_of_accident',
        'complete',
        'date_of_signed_by_the_applicant',
        'agreement',
        'payment_confirmation',
        'date_of_payment_confirmation'
    )
    search_fields = (
        'relief',
    )
    actions = [export_to_csv]


@admin.register(SignatureRelief)
class SignatureReliefAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'register_relief',
        'created_date',
        'updated_date',
        'slug',
        'author',
        'member',
        'signature'
    )
    list_filter = (
        'register_relief',
        'created_date',
        'updated_date',
        'slug',
        'author',
        'member',
        'signature'
    )
    search_fields = (
        'register_relief',
    )
    actions = [export_to_csv]


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
    actions = [export_to_csv]


@admin.register(AverageSalary)
class AverageSalaryAdmin(admin.ModelAdmin):
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
        'salary'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title',
        'salary'
    )
    search_fields = (
        'title',
    )
    actions = [export_to_csv]


@admin.register(Scholarships)
class ScholarshipsAdmin(admin.ModelAdmin):
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
        'member',
        'average_salary',
        'application_creation_date',
        'seminary_start_date',
        'seminary_end_date',
        'member_salary',
        'preferred_university',
        'average_grade',
        'grading_scale',
        'tuition_fee_amount',
        'file_scholarship_application',
        'file_scanned_confirmation_of_payment_for_studies',
        'file_declaration_of_income',
        'file_resolution_consenting',
        'file_document_confirming_of_the_semester',
        'file_university_regulations_of_the_grading_scale',
        'confirmation_of_student_id',
        'scholarship_rate',
        'confirmation_of_scholarship',
        'confirmation_date'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title',
        'member',
        'average_salary',
        'application_creation_date',
        'seminary_start_date',
        'seminary_end_date',
        'member_salary',
        'preferred_university',
        'average_grade',
        'grading_scale',
        'tuition_fee_amount',
        'file_scholarship_application',
        'file_scanned_confirmation_of_payment_for_studies',
        'file_declaration_of_income',
        'file_resolution_consenting',
        'file_document_confirming_of_the_semester',
        'file_university_regulations_of_the_grading_scale',
        'confirmation_of_student_id',
        'scholarship_rate',
        'confirmation_of_scholarship',
        'confirmation_date'
    )
    search_fields = (
        'title',
    )
    actions = [export_to_csv]


@admin.register(KindOfFinanceDocument)
class KindOfFinanceDocumentAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title_doc'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title_doc'
    )
    search_fields = (
        'title_doc',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(KindOfFinanceExpense)
class KindOfFinanceExpenseAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title_expense'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title_expense'
    )
    search_fields = (
        'title_expense',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(FileFinance)
class FileFinanceAdmin(admin.ModelAdmin):
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
        'file',
        'type_of_document',
        'figure',
        'quantity',
        'payment_date',
        'resolution',
        'resolution_requirement',
        'expense_name',
        'psychologist',
        'member'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title',
        'file',
        'type_of_document',
        'figure',
        'quantity',
        'payment_date',
        'resolution',
        'resolution_requirement',
        'expense_name',
        'psychologist',
        'member'
    )
    search_fields = (
        'title',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(BankStatement)
class BankStatementAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title_bank_statement',
        'file_bank_statement',
        'year_bank_statement',
        'month_bank_statement',
        'quantity_bank_statement',
        'starting_balance',
        'final_balance',
        'income_bank_statement'

    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title_bank_statement',
        'file_bank_statement',
        'year_bank_statement',
        'month_bank_statement',
        'quantity_bank_statement',
        'starting_balance',
        'final_balance',
        'income_bank_statement'

    )
    search_fields = (
        'title_bank_statement',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(VotingSessionKickOff)
class VotingSessionKickOffAdmin(admin.ModelAdmin):
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
        'vote',
        'commission_confirmed',
        'session_start',
        'session_end',
        'session_closed'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'title',
        'vote',
        'commission_confirmed',
        'session_start',
        'session_end',
        'session_closed'
    )
    search_fields = (
        'title',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(VotingSessionKickOffSignature)
class VotingSessionKickOffSignatureAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'voting_session_kick_off',
        'member',
        'signature'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'voting_session_kick_off',
        'member',
        'signature'
    )
    search_fields = (
        'voting_session_kick_off',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(VotingSessionSignature)
class VotingSessionSignatureAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'vote',
        'voting_session_kick_off',
        'member',
        'signature',
        'confirmation',
        'reject'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'vote',
        'voting_session_kick_off',
        'member',
        'signature',
        'confirmation',
        'reject'
    )
    search_fields = (
        'voting_session_kick_off',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(VotingResponses)
class VotingResponsesAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'vote',
        'voting_session_kick_off',
        'poll',
        'choice'
    )
    list_filter = (
        'created_date',
        'updated_date',
        'slug',
        'author',
        'vote',
        'voting_session_kick_off',
        'poll',
        'choice'
    )
    search_fields = (
        'slug',
    )
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'


@admin.register(VoteFile)
class VoteFileAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created_date']
        return self.readonly_fields

    list_display = (
        'voting',
        'title',
        'file',
        'created_date',
        'slug',
        'author',
        'updated_date'
    )
    list_filter = (
        'voting',
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
    actions = [export_to_csv]
    # date_hierarchy = 'created_date'
