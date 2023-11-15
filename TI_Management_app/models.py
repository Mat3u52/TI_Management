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


class CardStatus(models.Model):
    STATUS_CHOICES = (
        ('none', 'Brak statusu'),
        ('demandReceived', 'Zapotrzebowanie odebrane'),
        ('requestSent', 'Zapotrzebowanie wysłane'),
        ('sent', 'Przysłana'),
        ('received', 'Odebrana'),
        ('deactivated', 'Dezaktywowana'),
    )
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    card_identity = models.CharField(max_length=250, blank=False, default=None, unique=True)
    card_status = models.CharField(max_length=250, choices=STATUS_CHOICES, default='none')

    def __str__(self):
        return self.card_identity

    class Meta:
        verbose_name_plural = 'Status Kart'


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
    forename = models.CharField(max_length=250, blank=True, default=None)
    surname = models.CharField(max_length=250, blank=True, default=None)
    sex = models.CharField(max_length=250, choices=SEX_CHOICES, default=None)
    phone_number = PhoneField(max_length=12, blank=True, help_text='Contact phone number')
    email = models.EmailField(max_length=250, blank=True, help_text='user@user.com')
    date_of_accession = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    date_of_abandonment = models.DateTimeField(default=None, blank=True, null=True)
    type_of_contract = models.CharField(max_length=250, choices=CONTRACT_CHOICES, default=None)
    date_of_contract = models.DateTimeField(default=None, blank=True, null=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True)
    card_rfid = models.ForeignKey(CardsRFID, on_delete=models.CASCADE, null=True, blank=True)
    card_status = models.ForeignKey(CardStatus, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return f"{self.forename} {self.surname}"

    class Meta:
        verbose_name_plural = 'Członkowie'


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'uploads/%Y/%m/%d/user_{0}/{1}'.format(instance.user.id, filename)


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
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=350, null=False, blank=False)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    importance = models.CharField(max_length=250, choices=IMPORTANCE_CHOICES, default=None)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=None)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Notatki'


class Application(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    kind_of_application = models.CharField(max_length=350, null=False, blank=False)
    date_of_application = models.DateTimeField(default=timezone.now)
    date_of_payout = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(MembersZZTI, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.kind_of_application

    class Meta:
        verbose_name_plural = 'Wnioski'

