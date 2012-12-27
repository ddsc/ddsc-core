# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.gis.db import models

from ddsc_core.models.models import BaseModel


class Folder(BaseModel):
    path = models.CharField(max_length=64)
    user = models.ForeignKey(User)


class IPAddress(BaseModel):
    label = models.GenericIPAddressField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.label

    class Meta(BaseModel.Meta):
        verbose_name = "IP address"
        verbose_name_plural = "IP addresses"
