# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.gis.db import models

from ddsc_core.models.models import BaseModel


APP_LABEL = "ddsc_core"


class Folder(BaseModel):
    path = models.CharField(max_length=64)
    user = models.ForeignKey(User)


class IPAddress(BaseModel):
    label = models.CharField(max_length=15)
    user = models.ForeignKey(User)
