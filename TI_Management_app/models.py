from django.db import models
from django.utils import timezone


class Groups(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    group_name = models.CharField(max_length=250)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = 'Grupy'


class CardsRFID(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    serial_number = models.IntegerField()
    username = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Karty RFID'


class Cards(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    card_name = models.CharField(max_length=250)

    def __str__(self):
        return self.card_name

    class Meta:
        verbose_name_plural = 'Karty Lojalnościowe'


class CardStatus(models.Model):
    STATUS_CHOICES = (
        ('none', 'None'),
        ('demandReceived', 'Zapotrzebowanie odebrane'),
        ('requestSent', 'Zapotrzebowanie wysłane'),
        ('sent', 'Przysłana'),
        ('received', 'Odebrana'),
        ('deactivated', 'Dezaktywowana'),
    )
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    card_identity = models.CharField(max_length=250, blank=False, default=None)
    card_status = models.CharField(max_length=250, choices=STATUS_CHOICES, default='none')

    def __str__(self):
        return self.card_identity

    class Meta:
        verbose_name_plural = 'Status Kart'
