from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField('Nazwa', max_length=100, null=True)

    def __str__(self):
        return self.name
