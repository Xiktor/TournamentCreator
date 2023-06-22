from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from app.models.player_model import Player


class Tournament(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField('Nazwa', max_length=100, null=True)
    start_date = models.DateTimeField('Rozpoczęcie', null=True)
    max_players = models.IntegerField(
        'Max graczy',
        null=False,
        validators=[MinValueValidator(2), MaxValueValidator(500)]
    )
    is_started = models.BooleanField('Rozpoczęty', null=False, default=False)
    is_finished = models.BooleanField('Zakończony', null=False, default=False)
    players = models.ManyToManyField(Player, 'Gracze')

    def __str__(self):
        return self.name
