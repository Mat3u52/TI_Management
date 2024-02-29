from django.db import models
from django.utils import timezone
from phone_field import PhoneField
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Groups(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorGroups')
    group_name = models.CharField(max_length=250, blank=False, default=None, unique=True)

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Grupy'
        ordering = ('-created_date',)

    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.group_name)
        super().save(*args, **kwargs)


class MemberFunction(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorMemberFunction')
    member_function = models.CharField(max_length=250, blank=False, default=None, unique=True)

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Funkcja Członka'
        ordering = ('-created_date',)

    def __str__(self):
        return self.member_function

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.member_function)
        super().save(*args, **kwargs)


class MemberOccupation(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorMemberOccupation')
    member_occupation = models.CharField(max_length=250, blank=False, default=None, unique=True)

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Stanowisko Członka'
        ordering = ('-created_date',)

    def __str__(self):
        return self.member_occupation

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.member_occupation}")
        super().save(*args, **kwargs)


class CardsRFID(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    serial_number = models.IntegerField(unique=True)
    username = models.CharField(max_length=250, blank=False, default=None)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Karty RFID'


class Cards(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorCards')
    card_name = models.CharField(max_length=250, blank=False, default=None, unique=True)

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Karty Lojalnościowe'
        ordering = ('-created_date',)

    def __str__(self):
        return self.card_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.card_name)
        super().save(*args, **kwargs)


class Answers(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    answer = models.CharField(max_length=250, blank=False, default=None, unique=True)
    status = models.BooleanField(default=False)
    status_description = models.BooleanField(default=False)
    # description = models.TextField(null=True, blank=True, default=None)
    # status_description = models.BooleanField()

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name_plural = 'Odpowiedzi'


class Questions(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    question = models.CharField(max_length=250, blank=False, default=None, unique=True)
    # answer = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='question', null=True, blank=True)

    answer = models.ManyToManyField(Answers)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Pytania'


class DocumentsDatabaseCategory(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorDocumentsDatabaseCategory')
    title = models.CharField(max_length=250, null=False, blank=False)
    responsible = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Baza Dokumentów Kategorie'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class DocumentsDatabase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorDocumentsDatabase')
    category = models.ForeignKey(DocumentsDatabaseCategory, on_delete=models.CASCADE, related_name='documentsDatabaseCategpry', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='documentsDatabase/%Y/%m/%d/%H%M%S/')
    responsible = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Baza Dokumentów'
        ordering = ('-created_date',)

    def __str__(self):
        return (f"{self.title} "
                f"{self.category}")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class MembersZZTI(models.Model):
    SEX_CHOICES = (
        ('female', 'Kobieta'),
        ('male', 'Mężczyzna'),
    )
    CONTRACT_CHOICES = (
        ('indefinite_period_of_time', 'Na czas nieokreślony'),
        ('limited_duration', 'Na czas określony'),
    )
    # created_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorMembers')
    forename = models.CharField(max_length=250, blank=False, null=False)
    surname = models.CharField(max_length=250, blank=False, null=False)
    role = models.ForeignKey(MemberFunction, on_delete=models.CASCADE, null=True, blank=True, default=None)
    occupation = models.ForeignKey(MemberOccupation, on_delete=models.CASCADE, null=True, blank=True, default=None)
    member_nr = models.CharField(max_length=250, blank=False, null=False, unique=True)
    sex = models.CharField(max_length=250, choices=SEX_CHOICES, blank=True, null=True, default=None)
    birthday = models.DateTimeField(default=None, blank=True, null=True)
    birthplace = models.CharField(max_length=250, blank=True, null=True, default=None)
    pin = models.IntegerField(blank=False, null=False, unique=True)
    phone_number = PhoneField(max_length=12, blank=True, null=True, default=None, help_text='Contact phone number')
    email = models.EmailField(max_length=250, blank=False, null=False, unique=True, help_text='user@user.com')
    date_of_accession = models.DateTimeField(default=timezone.now, blank=False, null=False)
    date_of_abandonment = models.DateTimeField(default=None, blank=True, null=True)
    type_of_contract = models.CharField(max_length=250, choices=CONTRACT_CHOICES, blank=True, null=True, default=None)
    date_of_contract = models.DateTimeField(default=None, blank=True, null=True)
    expiration_date_contract = models.DateTimeField(default=None, blank=True, null=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True, default=None)
    card = models.CharField(max_length=250, blank=True, null=True, default=None)
    image = models.ImageField(null=True, blank=True, upload_to='images/%Y/%m/%d/%H%M%S/', default='images/NoImage.png')
    deactivate = models.BooleanField(default=False)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Członkowie'
        ordering = ('-created_date',)

    def __str__(self):
        return (f"{self.forename} {self.surname} {self.role} {self.occupation} {self.member_nr} {self.sex} "
                f"{self.birthday} {self.birthplace} {self.pin} {self.phone_number} {self.email} "
                f"{self.date_of_accession} {self.date_of_abandonment} {self.type_of_contract} {self.date_of_contract} "
                f"{self.expiration_date_contract} {self.group} {self.card} {self.image} {self.deactivate}")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.forename}-{self.surname}-{self.member_nr}")
        super().save(*args, **kwargs)


class Vote(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True, default=None)
    date_start = models.DateTimeField(default=None, blank=True, null=True)
    date_end = models.DateTimeField(default=None, blank=True, null=True)
    importance = models.BooleanField(default=False)
    # questions = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # question = models.ManyToManyField(Questions)

    questions = models.ManyToManyField(Questions, related_name='voteQuestion')
    members = models.ManyToManyField(MembersZZTI, related_name='voteMember')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Głosowanie'


class MembersFile(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorMembersFile')
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='membersFile', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='uploadsMember/%Y/%m/%d/%H%M%S/')
    history = HistoricalRecords()

    ordering = ('-created_date',)

    class Meta:
        verbose_name_plural = 'Członkowie Pliki'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class GroupsFile(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorGroupsFile')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='groupsFile', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='uploadsGroup/%Y/%m/%d/%H%M%S/')
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Grupy Pliki'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.group}")
        super().save(*args, **kwargs)


class GroupsNotepad(models.Model):
    IMPORTANCE_CHOICES = (
        ('none', 'Nie dotyczy'),
        ('low', 'Niski'),
        ('standard', 'Umiarkowany'),
        ('important', 'Ważny'),
        ('veryImportant', 'Bardzo ważny'),
        ('critical', 'Krytyczny'),
    )

    METHOD_CHOICES = (
        ('personally', 'Osobiście'),
        ('email', 'E-mail'),
        ('telephone', 'Telefonicznie'),
        ('zoom', 'ZOOM'),
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('other', 'Inny'),
    )

    STATUS_CHOICES = (
        ('ongoing', 'W trakcie'),
        ('closed', 'Zamknięty'),
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorGroupsNotepad')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='groupsNotepad', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    content = models.TextField(null=True, blank=True, default=None)
    published_date = models.DateTimeField(blank=True, null=True)
    importance = models.CharField(max_length=250, choices=IMPORTANCE_CHOICES, default=None)
    method = models.CharField(max_length=250, choices=METHOD_CHOICES, default=None)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=None)
    responsible = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Grupy Komunikacja'
        ordering = ('-created_date',)

    def __str__(self):
        return (f"{self.title} "
                f"{self.content} "
                f"{self.importance} "
                f"{self.status} "
                f"{self.method} "
                f"{self.published_date}")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Notepad(models.Model):
    IMPORTANCE_CHOICES = (
        ('none', 'Nie dotyczy'),
        ('low', 'Niski'),
        ('standard', 'Umiarkowany'),
        ('important', 'Ważny'),
        ('veryImportant', 'Bardzo ważny'),
        ('critical', 'Krytyczny'),
    )

    METHOD_CHOICES = (
        ('personally', 'Osobiście'),
        ('email', 'E-mail'),
        ('telephone', 'Telefonicznie'),
        ('zoom', 'ZOOM'),
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('other', 'Inny'),
    )

    STATUS_CHOICES = (
        ('ongoing', 'W trakcie'),
        ('closed', 'Zamknięty'),
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorNotepad')
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='notepad', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    content = models.TextField(null=True, blank=True, default=None)
    published_date = models.DateTimeField(blank=True, null=True)
    importance = models.CharField(max_length=250, choices=IMPORTANCE_CHOICES, default=None)
    method = models.CharField(max_length=250, choices=METHOD_CHOICES, default=None)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=None)
    responsible = models.CharField(max_length=250, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='uploadsNotepad/%Y/%m/%d/%H%M%S/')
    confirmed = models.BooleanField(default=False)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Komunikacja'
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.title} {self.content} {self.importance} {self.status} {self.method} {self.file}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class GroupsMember(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorGroupsMember')
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='groupsMember', null=True, blank=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='groupsGroup', null=False, blank=False, default=None)

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Grupy Członek'
        ordering = ('-created_date',)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.group}-{self.member}")
        super().save(*args, **kwargs)


class Application(models.Model):  # Finances member explicitly
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorApplication')
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='application', null=True, blank=True)
    kind_of_application = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True, default=None)
    date_of_application = models.DateTimeField(default=timezone.now)
    date_of_payout = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Finanse'
        ordering = ('-created_date',)

    def __str__(self):
        return self.kind_of_application

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.kind_of_application}-{self.member}")
        super().save(*args, **kwargs)


class Relief(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorRelief')
    title = models.CharField(max_length=250, null=False, blank=False, unique=True)
    figure = models.FloatField(null=False, blank=False)
    grace = models.IntegerField(null=False, blank=False)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Zapomogi'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('TI_Management_app:relife_add',
                       args=[self.created_date.year,
                             self.created_date.month,
                             self.created_date.day, self.slug])


class OrderedCardDocument(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorOrderedCardDocument')
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name='loyaltyCardOrder', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='OrderedCardDocument/%Y/%m/%d/%H%M%S/')
    responsible = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Dokumenty Zlecona'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ToBePickedUpCardDocument(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorToBePickedUpCardDocument')
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name='loyaltyCardToBePickedUp', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='ToBePickedUpCardDocument/%Y/%m/%d/%H%M%S/')
    responsible = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Dokumenty Odbioru'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


def validate_unique_or_null(value):
    if value is None or value.strip() == '':
        # If the value is None or an empty string, consider it as null
        return

    if isinstance(value, str):
        # If value is a string, check for uniqueness in the queryset
        existing_records = CardStatus.objects.filter(card_identity=value)
    else:
        # If value is an instance of the model, exclude it and check for uniqueness
        existing_records = CardStatus.objects.exclude(pk=value.pk).filter(card_identity=value.card_identity)

    if existing_records.exists():
        raise ValidationError('This field must be unique or null.')


class CardStatus(models.Model):
    STATUS_CHOICES = (
        ('none', 'Brak statusu'),
        ('active', 'Aktywna'),
        ('toOrder', 'Do zlecenia'),
        ('ordered', 'Zlecona'),
        ('toBePickedUp', 'Do odbioru'),
        ('deactivated', 'Dezaktywowana'),
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorCardStatus')
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='cardStatus', null=True, blank=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name='loyaltyCardStatus')
    ordered_doc = models.ForeignKey(OrderedCardDocument, on_delete=models.SET_NULL, related_name='orderedDoc', null=True, blank=True)
    to_be_picked_up_doc = models.ForeignKey(ToBePickedUpCardDocument, on_delete=models.SET_NULL, related_name='toBePickedUpCardDoc', null=True, blank=True)
    card_identity = models.CharField(max_length=250, blank=True, null=True, validators=[validate_unique_or_null])
    card_start_pin = models.CharField(max_length=250, blank=True, null=True, default=None)
    card_status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=None)
    date_of_action = models.DateTimeField(default=timezone.now, blank=True, null=True)
    file_name = models.CharField(max_length=250, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='uploadsLoyaltyCards/%Y/%m/%d/%H%M%S/')
    file_date = models.DateTimeField(blank=True, null=True)
    file_name_a = models.CharField(max_length=250, null=True, blank=True)
    file_a = models.FileField(null=True, blank=True, upload_to='uploadsLoyaltyCards_a/%Y/%m/%d/%H%M%S/')
    file_a_date = models.DateTimeField(blank=True, null=True)
    responsible = models.CharField(max_length=250, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Status Kart'
        ordering = ('-created_date',)

    def __str__(self):
        return (f"{self.card_status} "
                f"{self.card_identity} "
                f"{self.card} "
                f"{self.ordered_doc} "
                f"{self.to_be_picked_up_doc}")

    # def save(self, **kwargs):
    #     self.card_identity = self.card_identity or None
    #     super().save(**kwargs)

    def save(self, *args, **kwargs):
        self.card_identity = self.card_identity or None
        if not self.slug:
            self.slug = slugify(f"{self.card}-{self.member}")
        super().save(*args, **kwargs)


class Activities(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=250, null=False, blank=False)
    capacity = models.IntegerField(blank=True, null=True)
    expiring_date = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Aktywności'


class ActivityStatus(models.Model):
    ACTIVITY_STATUS_CHOICES = (
        ('none', 'Brak statusu'),
        ('collect', 'Odebrano'),
        ('forCollection', 'Do odbioru'),
    )
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='activityStatus', null=True, blank=True)
    activities = models.ForeignKey(Activities, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True, default=None)
    activity_status = models.CharField(max_length=250, choices=ACTIVITY_STATUS_CHOICES, default='none')
    spend = models.IntegerField(blank=True, null=True)
    assigned_date = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return self.activities

    class Meta:
        verbose_name_plural = 'Aktywności Status'


class Task(models.Model):
    CATEGORY_CHOICES = (
        ('other', 'Inny'),
        ('bhp', 'BHP'),
        ('hr', 'HR'),
    )
    FREQUENCY_CHOICES = (
        ('none', 'Brak'),
        ('daily', 'Codziennie'),
        ('week', 'Tydzień'),
        ('two_weeks', 'Dwa tygodnie'),
        ('month', 'Miesiąc'),
        ('quarter', 'Kwartał'),
        ('half_year', 'Pół roku'),
        ('year', 'Rok'),
    )
    IMPORTANCE_CHOICES = (
        ('none', 'Nie dotyczy'),
        ('standard', 'Standard'),
        ('important', 'Ważny'),
        ('critical', 'Krytyczny'),
    )
    STATUS_CHOICES = (
        ('ongoing', 'W trakcie'),
        ('closed', 'Zamknięty'),
    )
    created_date = models.DateTimeField(default=timezone.now)
    task_name = models.CharField(max_length=250, null=False, blank=False)
    category = models.CharField(max_length=250, choices=CATEGORY_CHOICES, default=None)
    description = models.TextField()
    deadline = models.DateTimeField(default=None, blank=True, null=True)
    frequency = models.CharField(max_length=250, choices=FREQUENCY_CHOICES, default=None)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='task', null=True, blank=True)
    importance = models.CharField(max_length=250, choices=IMPORTANCE_CHOICES, default=None)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=None)

    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name_plural = 'Zadania'
