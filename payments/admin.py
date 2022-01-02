# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from payments import models


class PaymentAdmin(admin.ModelAdmin):
    model = models.Payment
    list_display_links = ('id',)
    list_display = ['id', 'title', 'description', ]
    list_editable = ['title', 'description', ]


admin.site.register(models.Payment, PaymentAdmin)
