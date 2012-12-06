from django.db import models


class Unit(models.Model):
    code = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=60, unique=True)
    dimension = models.CharField(max_length=12, null=True)
    conversion_factor = models.CharField(max_length=12, null=True)
    group = models.CharField(max_length=60, null=True)

    class Meta:
        app_label = "ddsc_core"
