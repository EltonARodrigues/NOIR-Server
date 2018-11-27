import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, UUIDField


class UUIDModel(Model):
    class Meta:
        abstract = True

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Sensor(UUIDModel):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('title', 'author', 'description',),)


    def __str__(self):
        return f'{self.title}-{self.id}'


class GasesCollected(UUIDModel):
    created_at = models.DateTimeField()
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    co = models.FloatField(default=0)
    co2 = models.FloatField(default=0)
    mp25 = models.FloatField(default=0)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('created_at', 'sensor'),)

    def __str__(self):
        return f'{self.created_at}'
