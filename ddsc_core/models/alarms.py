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
from django.utils import timezone
from datetime import date
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
    )

    EMAIL = 1
    SMS = 2
    EMAIL_AND_SMS = 3

    MESSAGE_TYPE = (
        (EMAIL, 'Email'),
        (SMS, 'SMS'),
        (EMAIL_AND_SMS, 'Email and SMS'),
    )

    URGENCY_TYPE = (
        (1, 'High'),
        (2, 'Low'),
    )

    FREQUENCY_TYPE = (
        (5, '5 min'),
        (10, '10 min'),
        (15, '15 min'),
        (30, '30 min'),
        (60, '1 hr'),
        (360, '6 hr'),
        (720, '12 hr'),
        (1440, '24 hr'),
    )

    name = models.CharField(max_length=80)
    
    single_owner = models.ForeignKey(User, null=True, blank=True)
    group_owner = models.ForeignKey(UserGroup, null=True, blank=True)
    
    description = models.CharField(max_length=20)
    frequency = models.IntegerField(
        choices = FREQUENCY_TYPE,
        default = 5,
    )
    template = models.TextField(
          default='this is a alarm message template',
    )

    urgency = models.IntegerField(
        choices = URGENCY_TYPE,
        default = 2,
    )

    logical_check = models.SmallIntegerField(
        choices = LOGIC_TYPES,
        default = AND,
    )
    message_type = models.IntegerField(
        choices = MESSAGE_TYPE,
        default=EMAIL,
    )
    previous_id = models.IntegerField(blank=True, null=True)
    active_stutus = models.BooleanField(default=False)
    date_cr = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name
    

class Alarm_Property(BaseModel):

    name = models.CharField(max_length = 80)
    value_type = models.SmallIntegerField(default=1)
    
    def __unicode__(self):
        return self.name
    

class Alarm_Item(BaseModel):

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
    property = models.ForeignKey(Alarm_Property)
    comparision = models.SmallIntegerField(
        choices = COMPARISION_TYPE,
        default = EQUAL,
    )
    value = models.FloatField(default=0.0)


class Alarm_Item_Details(BaseModel):
    alarm_details = models.OneToOneField(Alarm_Item, primary_key=True)
    timeseries = models.ForeignKey(Timeseries)
    logicalgroup = models.ForeignKey(LogicalGroup)
    location = models.ForeignKey(Location)
