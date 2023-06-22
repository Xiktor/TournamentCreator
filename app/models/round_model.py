from django.db import models
from app.models.tournament_model import Tournament


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round_number = models.IntegerField('Runda nr',null=True)

    def __str__(self):
        return self.tournament.name + ' - runda_' + str(self.round_number)
