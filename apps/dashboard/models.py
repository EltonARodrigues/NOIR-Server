from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

class Cadastro(Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Valores(Model):
    idm = models.IntegerField(primary_key=True)
    data = models.DateField(null=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    co = models.FloatField()
    co2 = models.FloatField()
    mp25 = models.FloatField()
    id = models.ForeignKey(Cadastro, on_delete=models.CASCADE)
