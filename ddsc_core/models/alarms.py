# (c) Fugro Geoservices. MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Q
from django.utils import timezone

from lizard_security.models import UserGroup
from ddsc_core.models.models import BaseModel
from ddsc_core.models.models import Timeseries
from ddsc_core.models.models import Location
from ddsc_core.models.models import LogicalGroup

from datetime import datetime


AND = 0
OR = 1
    
LOGIC_TYPES = (
    (AND, 'And'),
    (OR, 'OR'),
)

# Create your models here.
class Alarm(BaseModel):
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
    single_or_group = models.ForeignKey(ContentType, 
        limit_choices_to = {"model__in": ("user", "usergroup")},
        default = 1,
    )
    object_id = models.PositiveIntegerField()
#    single_owner = models.ForeignKey(User, null=True, blank=True)
#    group_owner = models.ForeignKey(UserGroup, null=True, blank=True)
    description = models.TextField(
        null=True, 
        blank=True,
        default='', 
        help_text="optional description"
    )
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
    active_status = models.BooleanField(default=False)
    last_checked = models.DateTimeField(default=datetime(1900,1,1,0,0))
    date_cr = models.DateTimeField(default=timezone.now)
    
    object_id = models.PositiveIntegerField()
    
    content_object = generic.GenericForeignKey('single_or_group', 'object_id')


    def __unicode__(self):
#        if self.single_or_group.name == 'user':
#            self.object_id = self.single_owner.id
#            self.group_owner_id = ''
#        else:
#            self.object_id = self.group_owner.id
#            self.single_owner_id = ''
#        self.save()
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
    
    VALUE_TYPE = (
        (1, 'a. Waarde'),
        (2, 'b. Status - Aantal metingen'),
        (3, 'c. Status - Percentage betrouwbare waarden'),
        (4, 'd. Status - Percentage twijfelachtige waarden'),
        (5, 'e. Status - Percentage onbetrouwbare waarden'),
        (6, 'f. Status - Minimum meetwaarde'),
        (7, 'g. Status - Maximum meetwaarde'),
        (8, 'h. Status - Gemiddelde meetwaarde'),
        (9, 'i. Status - Standaard deviatie'),
        (10, 'j. Status - Tijd sinds laatste meting'),
        (11, 'k. Status - Procentuele afwijking van het aantal te verwachten metingen'),
    )

    alarm = models.ForeignKey(Alarm)
    comparision = models.SmallIntegerField(
        choices = COMPARISION_TYPE,
        default = EQUAL,
    )
    value_type = models.IntegerField(
        choices = VALUE_TYPE,
        default = 1,
    )
    value_double = models.FloatField(null=True, blank=True)
    value_text = models.CharField(
        max_length=32, 
        null=True,
        blank=True,
    )
    value_int = models.IntegerField(null=True, blank=True)
    value_bool = models.NullBooleanField(null=True, blank=True)
    alarm_type = models.ForeignKey(ContentType, 
        limit_choices_to = {"model__in": ("timeseries", "logicalgroup","location")},
        default = 1,
    )
    object_id = models.PositiveIntegerField()
#    timeseries = models.ForeignKey(
#        Timeseries,
#        null = True,
#        blank = True,
#    )
#    logicalgroup = models.ForeignKey(
#        LogicalGroup,
#        null = True,
#        blank = True,
#    )
#    location = models.ForeignKey(
#        Location,
#        null = True,
#        blank = True,
#    )
    logical_check = models.SmallIntegerField(
        choices = LOGIC_TYPES,
        default = AND,
    )
#    last_checked = models.DateTimeField(default=datetime(1900,1,1,0,0))
      
    content_object = generic.GenericForeignKey('alarm_type', 'object_id')

class Alarm_Active(BaseModel):
    alarm = models.ForeignKey(Alarm)
    first_triggered_on = models.DateTimeField(default=datetime(1900,1,1,0,0))
    message = models.TextField()
    deactivated_on = models.DateTimeField(default=datetime(1900,1,1,0,0))
    
