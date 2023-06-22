from django.db import models
from app.models.player_model import Player
from app.models.round_model import Round


class Arena(models.Model):
    round = models.ForeignKey(Round, null=True, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Player, related_name='player1',  on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2', on_delete=models.CASCADE)
    arena_number = models.IntegerField('Stolik nr', null=True)

    def __str__(self):
        return self.round.tournament.name \
               + ' - runda_' + str(self.round.round_number) \
               + ' - stolik_' + str(self.arena_number)
