from __future__ import unicode_literals

import math
import os
import uuid
import json

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from django.db import models
from django.utils import timezone


def date_now():
    return timezone.now().date()


class AutoDateTimeField(models.DateTimeField):
    """Custom Datetime Class that saves the datetime field without using the pre-built auto_now or auto_now_add"""

    def pre_save(self, model_instance, add):
        return timezone.now()


class Payment(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField()
    user = models.ForeignKey('userApp.User', on_delete=models.CASCADE)


    total = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Expired', 'Expired'),
        ('Paid', 'Paid'),
        ('Declined', 'Declined')
    ))
    date_issued = AutoDateTimeField(default=timezone.now)
    date_of_deadline = models.DateTimeField(blank=True, null=True)
    date_of_payment = models.DateTimeField(blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "Payment ID: " + str(self.id) + ", " + self.title

    
