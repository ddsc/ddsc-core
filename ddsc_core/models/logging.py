# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import unicode_literals

from django.db import models

from ddsc_core.models.models import BaseModel


class LogRecord(BaseModel):
    """A log record."""
    time = models.DateTimeField(db_index=True, help_text="created at")
    host = models.CharField(max_length=64, db_index=True, help_text="hostname")
    message = models.TextField(help_text="log message")
    level = models.CharField(max_length=8, db_index=True, help_text="severity")
    source = models.CharField(max_length=256, help_text="source code file")
    line = models.SmallIntegerField(help_text="line number")

    def __unicode__(self):
        return self.message
