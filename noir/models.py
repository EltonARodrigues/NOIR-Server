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
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Valores(models.Model):
    data = models.DateField()
    temperatura = models.FloatField()
    umidade = models.FloatField()
    co = models.FloatField()
    co2 = models.FloatField()
    pm25 = models.FloatField()
    cadastro = models.ForeignKey(Cadastro,on_delete=models.CASCADE)


