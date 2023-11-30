import datetime

from django.db import models
from django.utils import timezone
from phone_field import PhoneField


class Groups(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    group_name = models.CharField(max_length=250, blank=False, default=None)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = 'Grupy'


class CardsRFID(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    serial_number = models.IntegerField(unique=True)
    username = models.CharField(max_length=250, blank=False, default=None)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Karty RFID'


class Cards(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    card_name = models.CharField(max_length=250, blank=False, default=None, unique=True)

    def __str__(self):
        return self.card_name

    class Meta:
        verbose_name_plural = 'Karty Lojalnościowe'


class MembersZZTI(models.Model):
    SEX_CHOICES = (
        ('female', 'Kobieta'),
        ('male', 'Mężczyzna'),
    )
    CONTRACT_CHOICES = (
        ('indefinite_period_of_time', 'Na czas nieokreślony'),
        ('limited_duration', 'Na czas określony'),
    )
    created_date = models.DateTimeField(default=timezone.now)
    forename = models.CharField(max_length=250, blank=True, null=True, default=None)
    surname = models.CharField(max_length=250, blank=True, null=True, default=None)
    role = models.CharField(max_length=250, blank=True, null=True, default=None)
    member_nr = models.CharField(max_length=250, blank=True, null=True, default=None)
    sex = models.CharField(max_length=250, choices=SEX_CHOICES, blank=True, null=True, default=None)

    birthday = models.DateTimeField(default=None, blank=True, null=True)
    birthplace = models.CharField(max_length=250, blank=True, null=True, default=None)
    pin = models.CharField(max_length=250, blank=True, null=True, default=None)

    phone_number = PhoneField(max_length=12, blank=True, null=True, default=None, help_text='Contact phone number')
    email = models.EmailField(max_length=250, blank=True, null=True, default=None, help_text='user@user.com')
    date_of_accession = models.DateTimeField(default=timezone.now, blank=True, null=True)
    date_of_abandonment = models.DateTimeField(default=None, blank=True, null=True)
    type_of_contract = models.CharField(max_length=250, choices=CONTRACT_CHOICES, blank=True, null=True, default=None)
    date_of_contract = models.DateTimeField(default=None, blank=True, null=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # card_rfid = models.ForeignKey(CardsRFID, on_delete=models.CASCADE, null=True, blank=True, default=None)
    card = models.CharField(max_length=350, blank=True, null=True, default=None)
    # card_status = models.ForeignKey(CardStatus, on_delete=models.CASCADE, null=True, blank=True, default=None)
    image = models.ImageField(null=True, blank=True, upload_to='images/', default='images/NoImage.png')

    def __str__(self):
        return f"{self.forename} {self.surname}"

    class Meta:
        verbose_name_plural = 'Członkowie'


class Notepad(models.Model):
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
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='notepad', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=350, null=False, blank=False)
    content = models.TextField(null=True, blank=True, default=None)
    published_date = models.DateTimeField(default=timezone.now)
    importance = models.CharField(max_length=250, choices=IMPORTANCE_CHOICES, default=None)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=None)
    file = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Notatki'


class GroupsMember(models.Model):
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='groupsMember', null=True, blank=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True, default=None)
    created_date = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return self.group

    class Meta:
        verbose_name_plural = 'Grupy Członek'


class Application(models.Model):
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='application', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    kind_of_application = models.CharField(max_length=350, null=False, blank=False)
    description = models.TextField(null=True, blank=True, default=None)
    date_of_application = models.DateTimeField(default=timezone.now)
    date_of_payout = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.kind_of_application

    class Meta:
        verbose_name_plural = 'Finanse'


class CardStatus(models.Model):
    STATUS_CHOICES = (
        ('none', 'Brak statusu'),
        ('demandReceived', 'Zapotrzebowanie odebrane'),
        ('requestSent', 'Zapotrzebowanie wysłane'),
        ('sent', 'Przysłana'),
        ('received', 'Odebrana'),
        ('deactivated', 'Dezaktywowana'),
    )
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, related_name='cardStatus', null=True, blank=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    card_identity = models.CharField(max_length=250, blank=False, default=None, unique=True)
    card_status = models.CharField(max_length=250, choices=STATUS_CHOICES, default='none')
    date_of_action = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.card_identity

    class Meta:
        verbose_name_plural = 'Status Kart'


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
    task_name = models.CharField(max_length=350, null=False, blank=False)
    category = models.CharField(max_length=250, choices=CATEGORY_CHOICES, default=None)
    description = models.TextField()
    deadline = models.DateTimeField(default=None, blank=True, null=True)
    frequency = models.CharField(max_length=250, choices=FREQUENCY_CHOICES, default=None)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, null=True, blank=True)
    importance = models.CharField(max_length=250, choices=IMPORTANCE_CHOICES, default=None)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=None)

    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name_plural = 'Zadania'
