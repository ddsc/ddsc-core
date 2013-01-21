# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from lizard_security.models import UserGroup
from ddsc_core.models.models import BaseModel
from ddsc_core.models.models import Timeseries
from ddsc_core.models.models import Location
from ddsc_core.models.models import LogicalGroup
# Create your models here.
class Alarm(BaseModel):
    AND = 0
    OR = 1
    EQUAL = 2
    NOT_EQUAL = 3
    GRATER = 4
    LESS = 5

    LOGIC_TYPES = (
        (AND, 'And'),
        (OR, 'OR'),
        (EQUAL, '=='),
        (NOT_EQUAL, '!='),
        (GRATER, '>'),
        (LESS, '<'),
    )

    EMAIL = 1
    SMS = 2
    EMAIL_AND_SMS = 3

    MESSAGE_TYPE = (
        (EMAIL, 'Email'),
        (SMS, 'Sms'),
        (EMAIL_AND_SMS, 'Email and SMS'),
    )

    name = models.CharField(max_length=80)
    owner_id = models.ForeignKey(User)
    owner_group = models.ForeignKey(UserGroup)
    description = models.CharField(max_length=20)
    frequency = models.IntegerField(default=5)
    template = models.TextField(
          default='this is a alarm message template',
    )
    urgency = models.IntegerField(default = 1)
    logical_check = models.SmallIntegerField(
        choices = LOGIC_TYPES,
        default = AND,
    )
    message_type = models.IntegerField(
        choices = MESSAGE_TYPE,
        default=EMAIL,
    )
    previous_id = models.IntegerField(default=1)
    active_stutus = models.BooleanField(default=False)
    date_created = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Alarm_Iterm(BaseModel):

    EQUAL = 1
    NOT_EQUAL = 2
    GRATER = 3
    LESS = 4

    COMPARISION_TYPE = (
        (EQUAL, '=='),
        (NOT_EQUAL, '!='),
        (GRATER, '>'),
        (LESS, '<'),
    )

    alarm = models.ForeignKey(Alarm)
    property_id = models.IntegerField(default=1)
    comparision = models.SmallIntegerField(
        choices = COMPARISION_TYPE,
        default = EQUAL,
    )
    value = models.FloatField(default=0.0)
    
    def __unicode__(self):
        return self.name

class Alarm_Property(BaseModel):

    name = models.CharField(max_length = 80)
    value_type = models.SmallIntegerField(default=1)
    
    def __unicode__(self):
        return self.name
    
class Alarm_Iterm_Details(BaseModel):
    alarm_details = models.OneToOneField(Alarm_Iterm, primary_key=True)
    timeseries = models.ForeignKey(Timeseries)
    logicalgroup = models.ForeignKey(LogicalGroup)
    location = models.ForeignKey(Location)    

    def __unicode__(self):
        return self.name
