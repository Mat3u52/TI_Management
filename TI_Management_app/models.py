from django.db import models
from django.utils import timezone


class Groups(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    group_name = models.CharField(max_length=250)

    def __str__(self):
        return self.group_name
