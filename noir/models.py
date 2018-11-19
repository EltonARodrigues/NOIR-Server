from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

class Cadastro(models.Model):
    title = models.CharField(max_length=50, default='SOME STRING')
    description = models.CharField(max_length=200)
    #code = models.CharField(max_length=6)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Valores(models.Model):
    idm = models.IntegerField(primary_key=True)
    data = models.DateField(null=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    co = models.FloatField()
    co2 = models.FloatField()
    mp25 = models.FloatField()
    #code = models.CharField(max_length=6)
    id = models.ForeignKey(Cadastro,on_delete=models.CASCADE)


