# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.gis.db import models

from ddsc_core.models.models import BaseModel


class Folder(BaseModel):
    """Maps an FTP to a Django user via his home directory.

    In fact, it's not necessarily his home directory, but
    any directory monitored by incron for this user.
    """
    path = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.path


class IPAddress(BaseModel):
    label = models.GenericIPAddressField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.label

    class Meta(BaseModel.Meta):
        verbose_name = "IP address"
        verbose_name_plural = "IP addresses"
