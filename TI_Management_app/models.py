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
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True)
    card_rfid = models.ForeignKey(CardsRFID, on_delete=models.CASCADE, null=True)
    card_status = models.ForeignKey(CardStatus, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name_plural = 'Członkowie'

