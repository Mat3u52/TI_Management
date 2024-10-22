from django.db import models
from django.utils import timezone
from phone_field import PhoneField
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field


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


class Headquarters(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorMemberHeadquarters')
    headquarters = models.CharField(max_length=250, blank=False, default=None, unique=True)

    street = models.CharField(max_length=250, blank=True, null=True, default='')
    city = models.CharField(max_length=250, blank=True, null=True, default='')
    postcode = models.CharField(max_length=250, blank=True, null=True, default='')
    house_number = models.CharField(max_length=50, blank=True, null=True, default='')
    float_number = models.CharField(max_length=50, blank=True, null=True, default='')

    national_court_register = models.IntegerField(null=True, blank=True)  # KRS
    tax_number = models.IntegerField(null=True, blank=True)  # NIP
    national_business_registry_number = models.IntegerField(null=True, blank=True)  # REGON

    history = HistoricalRecords()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Siedziby'
        ordering = ('-created_date',)

    def __str__(self):
        return self.headquarters

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.headquarters)
        super().save(*args, **kwargs)


class MemberFunction(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorMemberFunction')
    member_function = models.CharField(max_length=250, blank=False, default=None, unique=True)

    objects = models.Manager()

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

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorMembers')
    forename = models.CharField(max_length=250, blank=False, null=False)
    surname = models.CharField(max_length=250, blank=False, null=False)

    street = models.CharField(max_length=250, blank=True, null=True, default='')
    city = models.CharField(max_length=250, blank=True, null=True, default='')
    postcode = models.CharField(max_length=250, blank=True, null=True, default='')
    house_number = models.CharField(max_length=50, blank=True, null=True, default='')
    float_number = models.CharField(max_length=50, blank=True, null=True, default='')

    role = models.ForeignKey(MemberFunction, on_delete=models.CASCADE, null=True, blank=True, default=None)
    occupation = models.ForeignKey(MemberOccupation, on_delete=models.CASCADE, null=True, blank=True, default=None)
    headquarters = models.ForeignKey(Headquarters, on_delete=models.CASCADE, null=True, blank=True, default=None)
    member_nr = models.CharField(max_length=250, blank=False, null=False, unique=True)
    sex = models.CharField(max_length=250, choices=SEX_CHOICES, blank=True, null=True, default=None)
    birthday = models.DateTimeField(default=None, blank=True, null=True)
    birthplace = models.CharField(max_length=250, blank=True, null=True, default=None)
    pin = models.IntegerField(blank=False, null=False, unique=True)
    phone_number = PhoneField(max_length=12, blank=True, null=True, default=None, help_text='Contact phone number')
    email = models.EmailField(max_length=250, blank=False, null=False, unique=True, help_text='user@user.com')
    date_of_accession = models.DateTimeField(default=timezone.now, blank=False, null=False)
    date_of_abandonment = models.DateTimeField(default=None, blank=True, null=True)
    type_of_contract = models.CharField(max_length=250, choices=CONTRACT_CHOICES, blank=True, null=True, default='indefinite_period_of_time')
    date_of_contract = models.DateTimeField(default=None, blank=True, null=True)
    expiration_date_contract = models.DateTimeField(default=None, blank=True, null=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True, default=None)
    card = models.CharField(max_length=250, blank=True, null=True, default='')  # , unique=True
    image = models.ImageField(null=True, blank=True, upload_to='images/%Y/%m/%d/%H%M%S/', default='images/NoImage.png')
    deactivate = models.BooleanField(default=False)
    recommended_by = models.CharField(max_length=250, blank=True, null=True, default=None)
    # recommended_by = models.ForeignKey(MembersZZTI, on_delete=models.SET_NULL, null=True, related_name='authorMembers')

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
        # if self.card != '':
        #     if MembersZZTI.objects.filter(card=self.card).exists():
        #         raise ValidationError(f"Taka karta już istnieje w bazie.")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('TI_Management_app:voting_active_session_member_detail', kwargs={'slug': self.slug})


class Vote(models.Model):
    class VoteTypeChoices(models.TextChoices):
        OPEN_VOTING = 'open', 'Jawne'
        CONFIDENTIAL_VOTING = 'confidential', 'Tajne'

    class PeriodChoices(models.TextChoices):
        FROM_PERIOD = 'from', 'Od'
        TO_PERIOD = 'to', 'Do'
        NO_PERIOD = 'no', 'Brak'

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorVote')
    title = models.CharField(max_length=250, null=False, blank=False)
    description = CKEditor5Field(null=True, blank=True)
    # vote_type = models.CharField(max_length=250, choices=VOTE_TYPE_CHOICES, default=None)
    vote_type = models.CharField(max_length=100, choices=VoteTypeChoices.choices, default=VoteTypeChoices.CONFIDENTIAL_VOTING)
    period = models.CharField(max_length=100, choices=PeriodChoices.choices, default=PeriodChoices.NO_PERIOD)
    vote_method_online = models.BooleanField(default=False)
    vote_method_offline = models.BooleanField(default=False)
    date_accede = models.DateTimeField(default=None, blank=True, null=True)

    date_start = models.DateTimeField(default=None, blank=True, null=True)
    date_end = models.DateTimeField(default=None, blank=True, null=True)
    importance = models.BooleanField(default=False)

    min_amount_members = models.IntegerField(null=False, blank=False, default=0)
    min_amount_commission = models.IntegerField(null=False, blank=False, default=0)
    turnout = models.IntegerField(null=False, blank=False, default=0)

    members = models.ManyToManyField(MembersZZTI, related_name='voteMember')

    election_commission = models.ManyToManyField(MembersZZTI, related_name='voteElectionCommission')

    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Głosowanie'
        ordering = ('-created_date',)
        """"
        This feature is disabled for MySQL DB
        origin = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date'])
        ]
        """

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('TI_Management_app:voting_add', args=[self.pk])


class Poll(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorPoll')
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, null=True, related_name='votePoll')
    question = models.CharField(max_length=250, blank=False, default=None)
    description = CKEditor5Field(null=True, blank=True)
    number_of_responses = models.IntegerField(null=True, blank=True, default=0)

    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Pytania'

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
        super().save(*args, **kwargs)


class Choice(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorChoice')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, related_name='pollChoice')
    answer = models.CharField(max_length=250, blank=True, null=True, default=None)
    correct = models.BooleanField(default=False)
    open_ended_answer = models.BooleanField(default=False)
    # status = models.BooleanField(default=False)
    # status_description = models.BooleanField(default=False)

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Odpowiedzi'

    def __str__(self):
        if self.answer:
            return self.answer
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug and self.answer:
            self.slug = slugify(self.answer)
        else:
            # Generate a unique slug if the answer is missing
            self.slug = slugify(f"{self.poll}")
        super().save(*args, **kwargs)


class VotingSessionKickOff(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorVotingSessionKickOff')
    title = models.CharField(max_length=250, null=False, blank=False)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, null=True, related_name='voteVotingSessionKickOff')
    commission_confirmed = models.BooleanField(default=False)
    session_start = models.DateTimeField(default=None, blank=True, null=True)
    session_end = models.DateTimeField(default=None, blank=True, null=True)
    session_closed = models.BooleanField(default=False)

    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Sesje Głosowania Rozpoczęcie'
        ordering = ('-created_date',)
        """"
        This feature is disabled for MySQL DB
        origin = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date'])
        ]
        """

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('TI_Management_app:voting_session_kick_off', args=[self.pk])


class VotingSessionKickOffSignature(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorVotingSessionKickOffSignature')

    voting_session_kick_off = models.ForeignKey(VotingSessionKickOff, on_delete=models.CASCADE, related_name='voteVotingSessionKickOffSignature', null=False, blank=False)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='memberVotingSessionKickOffSignature', null=False, blank=False)
    signature = models.BooleanField(default=False)

    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Podpisy rozpoczęcia sesji '
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.id}-{self.member.member_nr}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.id}-{self.member.member_nr}")
        super().save(*args, **kwargs)


class VotingSessionSignature(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorVotingSessionSignature')

    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, null=True, related_name='voteVotingSessionSignature')
    voting_session_kick_off = models.ForeignKey(VotingSessionKickOff, on_delete=models.CASCADE, related_name='kickOffVotingSessionSignature', null=False, blank=False)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='memberVotingSessionSignature', null=False, blank=False)
    signature = models.BooleanField(default=False)
    confirmation = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)

    # session_end = models.DateTimeField(default=None, blank=True, null=True)

    history = HistoricalRecords()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Podpisy uczestników sesji '
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.id}-{self.member.member_nr}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.id}-{self.member.member_nr}")
        super().save(*args, **kwargs)


class VotingResponses(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorVotingResponses')

    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, null=True, related_name='voteVotingResponses')
    voting_session_kick_off = models.ForeignKey(VotingSessionKickOff, on_delete=models.CASCADE, related_name='voteVotingResponses', null=False, blank=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='pollVotingResponses', null=False, blank=False)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='choiceVotingResponses', null=False, blank=False)
    description = CKEditor5Field(null=True, blank=True)

    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Odpowiedzi z głosowania'
        ordering = ('-created_date',)
        """"
        This feature is disabled for MySQL DB
        origin = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date'])
        ]
        """

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.created_date}")
        super().save(*args, **kwargs)


class VoteFile(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorVoteFile')
    voting = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='votingVoteFile', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='uploadsVoteFile/%Y/%m/%d/%H%M%S/')
    history = HistoricalRecords()

    ordering = ('-created_date',)

    class Meta:
        verbose_name_plural = 'Głosowanie Pliki'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


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
    # content = models.TextField(null=True, blank=True, default=None)
    content = CKEditor5Field(null=True, blank=True)
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
                # f"{self.content} "
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
    content = CKEditor5Field(null=True, blank=True)
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
        return f"{self.title} {self.importance} {self.status} {self.method} {self.file}"

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
            self.slug = slugify(f"{self.group}")
        super().save(*args, **kwargs)


# class Application(models.Model):  # Finances member explicitly
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorApplication')
#     member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='application', null=True, blank=True)
#     kind_of_application = models.CharField(max_length=250, null=False, blank=False)
#     description = models.TextField(null=True, blank=True, default=None)
#     date_of_application = models.DateTimeField(default=timezone.now)
#     date_of_payout = models.DateTimeField(default=timezone.now)
#     history = HistoricalRecords()
#
#     objects = models.Manager()  # default manager
#
#     class Meta:
#         verbose_name_plural = 'Finanse'
#         ordering = ('-created_date',)
#
#     def __str__(self):
#         return self.kind_of_application
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(f"{self.kind_of_application}-{self.member}")
#         super().save(*args, **kwargs)


class KindOfFinanceDocument(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorKindOfFinanceDocument')
    # title = models.CharField(max_length=250, null=False, blank=False)
    title_doc = models.CharField(max_length=250, null=False, blank=False)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Finanse - Rodzaj dokumentu'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title_doc

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title_doc}")
        super().save(*args, **kwargs)


class KindOfFinanceExpense(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorKindOfFinanceExpense')
    # title = models.CharField(max_length=250, null=False, blank=False)
    title_expense = models.CharField(max_length=250, null=False, blank=False)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Finanse - Rodzaj wydatku'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title_expense

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title_expense}")
        super().save(*args, **kwargs)


class FileFinance(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorFileFinance')

    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=True, blank=True, upload_to='uploadsFileFinance/%Y/%m/%d/%H%M%S/')
    type_of_document = models.ForeignKey(KindOfFinanceDocument, on_delete=models.CASCADE, null=True, related_name='typeOfDocumentFileFinance')
    figure = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    payment_date = models.DateTimeField(blank=True, null=True)
    resolution = models.ForeignKey(DocumentsDatabase, on_delete=models.CASCADE, null=True, related_name='resolutionFileFinance')
    resolution_requirement = models.BooleanField(default=False)
    expense_name = models.ForeignKey(KindOfFinanceExpense, on_delete=models.CASCADE, null=True, related_name='expenseNameFileFinance')
    psychologist = models.BooleanField(default=False)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='memberFileFinance', null=True, blank=True)
    # description = RichTextField(null=True, blank=True)
    description = CKEditor5Field(null=True, blank=True)
    # description = models.TextField(null=True, blank=True, default=None)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Finanse - dokumenty'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)


class BankStatement(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorBankStatement')
    title_bank_statement = models.CharField(max_length=250, null=False, blank=False)
    file_bank_statement = models.FileField(null=False, blank=False, upload_to='uploadsBankStatement/%Y/%m/%d/%H%M%S/')
    year_bank_statement = models.IntegerField(null=False, blank=False)
    month_bank_statement = models.IntegerField(null=False, blank=False)
    quantity_bank_statement = models.IntegerField(null=False, blank=False, default=1)
    starting_balance = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    final_balance = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    income_bank_statement = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    history = HistoricalRecords()
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Wyciąg Bankowy'
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.title_bank_statement}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title_bank_statement}")
        super().save(*args, **kwargs)


class Relief(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorRelief')
    title = models.CharField(max_length=250, null=False, blank=False)  # unique = True
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


class RelationRegisterRelief(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorRelationRegisterRelief')
    title = models.CharField(max_length=250, null=False, blank=False, unique=True)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Relacje - Rejestracja Zapomogi'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)


class RegisterRelief(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorRegisterRelief')
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='memberRegisterRelief', null=False, blank=False)
    relief = models.ForeignKey(Relief, on_delete=models.CASCADE, related_name='reliefRegisterRelief', null=False, blank=False)
    relation = models.ForeignKey(RelationRegisterRelief, on_delete=models.CASCADE, related_name='relationReliefRegisterRelief', null=False, blank=False)
    associate_forename = models.CharField(max_length=250, null=True, blank=True)
    associate_surname = models.CharField(max_length=250, null=True, blank=True)
    account_number = models.CharField(max_length=26, null=True, blank=True)
    date_of_completing_the_application = models.DateTimeField(blank=True, null=True)
    date_of_receipt_the_application = models.DateTimeField(blank=True, null=True)
    date_of_accident = models.DateTimeField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    date_of_signed_by_the_applicant = models.DateTimeField(blank=True, null=True)
    agreement = models.BooleanField(default=False)  # min 3 signed
    payment_confirmation = models.BooleanField(default=False)  # min 3 signed
    date_of_payment_confirmation = models.DateTimeField(blank=True, null=True)
    # reason = models.TextField(null=True, blank=True, default=None)
    reason = models.TextField(null=True, blank=True, default=None)

    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Rejestracja zapomogi'
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.relief}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.relief}")
        super().save(*args, **kwargs)


class SignatureRelief(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorSignatureRelief')
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='memberSignatureRelief', null=False, blank=False)
    register_relief = models.ForeignKey(RegisterRelief, on_delete=models.CASCADE, related_name='registerReliefSignatureRelief', null=False, blank=False)
    signature = models.BooleanField(default=False)
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Podpisy zapomogi'
        ordering = ('-created_date',)

    def __str__(self):
        return self.register_relief

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.register_relief}")
        super().save(*args, **kwargs)


class FileRegisterRelief(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorFileRegisterRelief')
    register_relief = models.ForeignKey(RegisterRelief, on_delete=models.CASCADE, related_name='registerReliefFileRegisterRelief', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='uploadsRegisterRelief/%Y/%m/%d/%H%M%S/')
    history = HistoricalRecords()

    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Pliki - Rejestracja zapomogi'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)


class AverageSalary(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorAverageSalary')
    title = models.CharField(max_length=250, null=False, blank=False)
    salary = models.FloatField(null=False, blank=False)

    history = HistoricalRecords()
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Średnia wypłata'
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)


class Scholarships(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorScholarships')
    title = models.CharField(max_length=250, null=False, blank=False)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='memberScholarships', null=False, blank=False)
    average_salary = models.ForeignKey(AverageSalary, on_delete=models.CASCADE, related_name='averageSalaryScholarships', null=False, blank=False)
    application_creation_date = models.DateTimeField(blank=True, null=True)
    seminary_start_date = models.DateTimeField(blank=True, null=True)
    seminary_end_date = models.DateTimeField(blank=True, null=True)
    member_salary = models.FloatField(null=False, blank=False)
    preferred_university = models.BooleanField(default=False)
    average_grade = models.FloatField(null=False, blank=False)
    grading_scale = models.FloatField(null=False, blank=False)
    tuition_fee_amount = models.FloatField(null=False, blank=False)
    file_scholarship_application = models.FileField(null=False, blank=False, upload_to='uploadsScholarshipsApplication/%Y/%m/%d/%H%M%S/')
    file_scanned_confirmation_of_payment_for_studies = models.FileField(null=False, blank=False, upload_to='uploadsScholarshipsScannedConfirmationOfPaymentForStudies/%Y/%m/%d/%H%M%S/')
    file_declaration_of_income = models.FileField(null=False, blank=False, upload_to='uploadsScholarshipsDeclarationOfIncome/%Y/%m/%d/%H%M%S/')
    file_resolution_consenting = models.FileField(null=False, blank=False, upload_to='uploadsScholarshipsResolutionConsenting/%Y/%m/%d/%H%M%S/')
    file_document_confirming_of_the_semester = models.FileField(null=False, blank=False, upload_to='uploadsScholarshipsDocumentConfirmingOfTheSemester/%Y/%m/%d/%H%M%S/')
    file_university_regulations_of_the_grading_scale = models.FileField(null=False, blank=False, upload_to='uploadsScholarshipsUniversityRegulationsOfTheGradingScale/%Y/%m/%d/%H%M%S/')
    confirmation_of_student_id = models.BooleanField(default=False)
    scholarship_rate = models.FloatField(null=False, blank=False)
    confirmation_of_scholarship = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Stypendia'
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)


class OrderedCardDocument(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorOrderedCardDocument')
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name='loyaltyCardOrder', null=True, blank=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    file = models.FileField(null=False, blank=False, upload_to='orderedCardDocument/%Y/%m/%d/%H%M%S/')
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
    file = models.FileField(null=False, blank=False, upload_to='toBePickedUpCardDocument/%Y/%m/%d/%H%M%S/')
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
        raise ValidationError('To pole musi być unikalne.')


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

    def save(self, *args, **kwargs):
        self.card_identity = self.card_identity or None
        if not self.slug:
            self.slug = slugify(f"{self.card}")
        super().save(*args, **kwargs)


class DashboardCategories(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorDashboardCategories')
    title = models.CharField(max_length=250, blank=False, default=None, unique=True)
    weight = models.IntegerField(null=False, blank=False, default=0)

    history = HistoricalRecords()
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Dashboard - kategorie'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Dashboard(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique_for_date='created_date', default=None, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='authorDashboard')
    suitor = models.CharField(max_length=250, blank=False, default=None, unique=True)
    title = models.CharField(max_length=250, blank=False, default=None, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)
    the_end_date = models.DateTimeField(blank=True, null=True)
    assigned_member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='assignedMemberDashboard', null=True, blank=True)
    dashboard_categories = models.ForeignKey(DashboardCategories, on_delete=models.CASCADE, related_name='dashboardCategoriesDashboard', null=True, blank=True)
    done = models.BooleanField(default=False)
    frozen = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    history = HistoricalRecords()
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name_plural = 'Dashboard'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
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
