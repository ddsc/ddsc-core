# (c) Fugro Geoservices. MIT licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from ddsc_core.models.models import BaseModel

from datetime import datetime


AND = 0
OR = 1
LOGIC_TYPES = (
    (AND, 'And'),
    (OR, 'OR'),
)


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
    single_or_group = models.ForeignKey(
        ContentType,
        limit_choices_to={"model__in": ("user", "usergroup")},
        default=1,
    )
    description = models.TextField(
        null=True,
        blank=True,
        default='',
        help_text="optional description",
    )
    frequency = models.IntegerField(
        choices=FREQUENCY_TYPE,
        default=5,
    )
    template = models.TextField(
        default='this is a alarm message template',
    )

    urgency = models.IntegerField(
        choices=URGENCY_TYPE,
        default=2,
    )

    logical_check = models.SmallIntegerField(
        choices=LOGIC_TYPES,
        default=AND,
    )
    message_type = models.IntegerField(
        choices=MESSAGE_TYPE,
        default=EMAIL,
    )
    previous_alarm = models.ForeignKey('self', null=True, blank=True)
    active_status = models.BooleanField(default=True)
    last_checked = models.DateTimeField(default=datetime(1900, 1, 1, 0, 0))
    date_cr = models.DateTimeField(default=timezone.now)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('single_or_group', 'object_id')
    first_born = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.first_born is True:
            self.first_born = False
            super(Alarm, self).save(*args, **kwargs)
        else:
            try:
                Alarm.objects.get(previous_alarm_id=self.pk)
                raise Exception('you can not change the history!')
            except ObjectDoesNotExist:
                self.previous_alarm = self
                alm_itm_list = Alarm_Item.objects.filter(alarm_id=self.pk)
                self.pk = None
                self.active_status = True
                self.last_checked = datetime(1900, 1, 1, 0, 0)
                self.date_cr = timezone.now()
                super(Alarm, self).save(*args, **kwargs)
                for alm_itm in alm_itm_list:
                    alm_itm.pk = None
                    alm_itm.alarm = self
                    super(Alarm_Item, alm_itm).save(*args, **kwargs)
                pre_alm = Alarm.objects.get(pk=self.previous_alarm_id)
                pre_alm.active_status = False
                super(Alarm, pre_alm).save(*args, **kwargs)

    def make_active(self, *args, **kwargs):
        if self.active_status is False:
            alm = Alarm.objects.get(active_status=True, name=self.name)
            alm.active_status = False
            self.active_status = True
            super(Alarm, alm).save(*args, **kwargs)
            super(Alarm, self).save(*args, **kwargs)


class Alarm_Item(BaseModel):
    class ComparisionType:
        EQUAL = 1
        NOT_EQUAL = 2
        GRATER = 3
        LESS = 4

    COMPARISION_TYPE = (
        (ComparisionType.EQUAL, '=='),
        (ComparisionType.NOT_EQUAL, '!='),
        (ComparisionType.GRATER, '>'),
        (ComparisionType.LESS, '<'),
    )

    class ValueType:
        LATEST_VALUE = 1
        NR_MEASUR = 2
        PR_RELIABLE = 3
        PR_DOUBTFUL = 4
        PR_UNRELIABLE = 5
        MIN_MEASUR = 6
        MAX_MEASUR = 7
        AVG_MEASUR = 8
        STD_MEASUR = 9
        TIME_SINCE_LAST_MEASUR = 10
        PR_DEV_EXPECTED_NR_MEASUR = 11

    VALUE_TYPE = (
        (ValueType.LATEST_VALUE, 'a. Waarde'),
        (ValueType.NR_MEASUR, 'b. Status - Aantal metingen'),
        (ValueType.PR_RELIABLE, 'c. Status - Percentage' +
            ' betrouwbare waarden'),
        (ValueType.PR_DOUBTFUL, 'd. Status - Percentage' +
            ' twijfelachtige waarden'),
        (ValueType.PR_UNRELIABLE, 'e. Status - Percentage' +
            ' onbetrouwbare waarden'),
        (ValueType.MIN_MEASUR, 'f. Status - Minimum meetwaarde'),
        (ValueType.MAX_MEASUR, 'g. Status - Maximum meetwaarde'),
        (ValueType.AVG_MEASUR, 'h. Status - Gemiddelde meetwaarde'),
        (ValueType.STD_MEASUR, 'i. Status - Standaard deviatie'),
        (ValueType.TIME_SINCE_LAST_MEASUR, 'j. Status - Tijd sinds' +
            ' laatste meting'),
        (ValueType.PR_DEV_EXPECTED_NR_MEASUR, 'k. Status - Procentuele' +
            ' afwijking van het aantal te verwachten metingen'),
    )

    alarm = models.ForeignKey(
        Alarm, limit_choices_to={'active_status': [True]})
    comparision = models.SmallIntegerField(
        choices=COMPARISION_TYPE,
        default=ComparisionType.EQUAL,
    )
    value_type = models.IntegerField(
        choices=VALUE_TYPE,
        default=1,
    )
    value_double = models.FloatField(null=True, blank=True)
    value_text = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    value_int = models.IntegerField(null=True, blank=True)
    value_bool = models.NullBooleanField(null=True, blank=True)
    alarm_type = models.ForeignKey(
        ContentType,
        limit_choices_to={"model__in": ("timeseries", "logical"
                                        + "group", "location", )},
        default=1,
    )
    object_id = models.PositiveIntegerField()
    logical_check = models.SmallIntegerField(
        choices=LOGIC_TYPES,
        default=AND,
    )
    content_object = generic.GenericForeignKey('alarm_type', 'object_id')
    first_born = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.first_born is True:
            self.first_born = False
            super(Alarm_Item, self).save(*args, **kwargs)
        else:
            try:
                Alarm.objects.get(previous_alarm_id=self.alarm_id)
                raise Exception(
                    "This is a historical alarm item which can not be edited!")
            except ObjectDoesNotExist:
                alm_itm_self = self
                alm = self.alarm
                alm_prev_id = alm.pk
                alm_itm_list = Alarm_Item.objects.filter(alarm_id=alm.pk)
                alm.active_status = False
                super(Alarm, alm).save(*args, **kwargs)
                alm.pk = None
                alm.first_born = False
                alm.active_status = True
                alm.last_checked = datetime(1900, 1, 1, 0, 0)
                alm.date_cr = timezone.now()
                alm.previous_alarm_id = alm_prev_id
                super(Alarm, alm).save(*args, **kwargs)

                for alm_itm in alm_itm_list:
                    if alm_itm.pk != alm_itm_self.pk:
                        alm_itm.pk = None
                        alm_itm.alarm = alm
                        super(Alarm_Item, alm_itm).save(*args, **kwargs)
                    else:
                        alm_itm_self.pk = None
                        alm_itm_self.alarm = alm
                        super(Alarm_Item, alm_itm_self).save(*args, **kwargs)


class Alarm_Active(BaseModel):
    alarm = models.ForeignKey(Alarm)
    first_triggered_on = models.DateTimeField(
        default=datetime(1900, 1, 1, 0, 0)
    )
    message = models.TextField()
    deactivated_on = models.DateTimeField(default=datetime(1900, 1, 1, 0, 0))
    active = models.BooleanField(default=True)
