from django.db import models
from app.models.player_model import Player
from app.models.arena_model import Arena


class Result(models.Model):
    arena = models.ForeignKey(Arena, null=True, on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return 'zwyciezyl ' + self.winner.name
