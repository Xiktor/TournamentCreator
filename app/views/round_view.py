from django.shortcuts import redirect
from app.decorators import allowed_users
from app.models.round_model import Round
from app.models.tournament_model import Tournament
from app.models.arena_model import Arena
from app.models.result_model import Result


@allowed_users(allowed_roles=['user', 'admin'])
def generate_next_round(request, pk):
    finished_round = Round.objects.filter(id=pk).first()
    tournament = Tournament.objects.filter(round=pk).first()
    total_round = tournament.round_set.count()
    if finished_round.round_number < total_round:
        next_round = Round.objects.filter(
            tournament=tournament.pk,
            round_number=finished_round.round_number+1
        ).first()

        i = 1
        winners_i = 1
        while i <= (finished_round.arena_set.count()/2):
            finished_arena_p1 = Arena.objects.filter(round=finished_round.pk, arena_number=winners_i).first()
            finished_arena_p2 = Arena.objects.filter(round=finished_round.pk, arena_number=winners_i+1).first()
            arena = Arena()
            arena.round = next_round
            arena.arena_number = i
            arena.player1 = Result.objects.filter(arena=finished_arena_p1).first().winner
            arena.player2 = Result.objects.filter(arena=finished_arena_p2).first().winner
            arena.save()
            i += 1
            winners_i += 2
    return redirect('/tournaments/detail/' + str(tournament.id))
