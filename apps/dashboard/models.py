import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, UUIDField


class UUIDModel(Model):
    class Meta:
        abstract = True

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Sensor(UUIDModel):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class GasesCollected(UUIDModel):
    date = models.DateField(null=True)
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    co = models.FloatField(default=0)
    co2 = models.FloatField(default=0)
    mp25 = models.FloatField(default=0)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
