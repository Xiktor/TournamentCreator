from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from app.decorators import allowed_users
from app.models import Tournament, Round, Arena, Player, Result
from app.forms.tournaments_form import CreateTournamentForm, UpdateTournamentForm
import numpy as np
from django.contrib import messages


@allowed_users(allowed_roles=['user', 'admin'])
def delete_tournaments(request, pk):
    model = Tournament.objects.filter(pk=pk)
    if model.filter(user=request.user).first() or request.user.is_superuser:
        if request.method == 'POST':
            if model.filter(is_started=False, is_finished=False).first() or request.user.is_superuser:
                model.delete()
                messages.success(request, 'Pomyślnie usunięto turniej')
            else:
                messages.error(request, 'Turniej można usunąć jedynie przed jego rozpoczęciem')
    else:
        messages.error(request, 'Próba usunięcia turnieju innego użytkownika')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class RoundsStatusHelper:
    round_number = 0
    finished_table = 0
    total_table = 0


def count_finished_arenas_on_round(pk):
    my_list = []
    for round_ in Round.objects.filter(tournament=pk):
        arenas = list(Arena.objects.filter(round=round_.pk))
        arenas_finished = 0
        for arena in arenas:
            results = list(Result.objects.filter(arena=arena))
            for result in results:
                if result.winner:
                    arenas_finished = arenas_finished + 1
        x = RoundsStatusHelper()
        x.round_number = round_.round_number
        x.finished_table = arenas_finished
        x.total_table = len(arenas)
        my_list.append(x)
    return my_list


def tournaments_detail(request, pk):
    if request.user.is_anonymous:
        model = Tournament.objects.filter(pk=pk)
        if model.filter(is_started=True, is_finished=False):
            context = {'tournament': model.first(), 'rounds_status': count_finished_arenas_on_round(pk)}
            return render(request, 'app/tournaments/detail.html', context)
        else:
            messages.error(request, "Użytkownik anonimowy może przeglądać jedynie trwające turnieje")
            return redirect('home')
    else:
        model = Tournament.objects.filter(pk=pk)
        context = {'tournament': model.first(), 'rounds_status': count_finished_arenas_on_round(pk)}
        return render(request, 'app/tournaments/detail.html', context)


@allowed_users(allowed_roles=['user', 'admin'])
def update_tournament(request, pk):
    model = Tournament.objects.filter(pk=pk)
    if model.filter(user=request.user).first() or request.user.is_superuser:
        if model.filter(is_started=False, is_finished=False).first() or request.user.is_superuser:
            instance = model.first()
            form = CreateTournamentForm(user=request.user, instance=instance)
            if request.method == 'POST':
                form = UpdateTournamentForm(request.POST)
                if form.is_valid():
                    model.filter(pk=pk).update(name=str(request.POST['name']))
                    model.filter(pk=pk).update(max_players=int(request.POST['max_players']))
                    model.filter(pk=pk).update(
                        start_date=datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
                    )
                    model.filter(pk=pk).first().players.clear()

                    selected_players = list(form.cleaned_data.get('players'))
                    for player in selected_players:
                        model.filter(pk=pk).first().players.add(player.id)
                    messages.success(request, 'Turniej ' + str(request.POST['name']) + ' edytowany pomyślnie.')
                    return redirect('tournaments_list', 'planned')
                else:
                    messages.error(request, 'Do turnieju musi być przypisany co najmniej jeden gracz.')
            context = {'form': CreateTournamentForm(user=request.user, instance=instance)}
            return render(request, 'app/tournaments/update.html', context)
        else:
            messages.error(request, 'Turniej można edytować jedynie przed jego rozpoczęciem')
    else:
        messages.error(request, 'Próba edycji turnieju innego użytkownika')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@allowed_users(allowed_roles=['user', 'admin'])
def create_tournament(request):
    form = CreateTournamentForm(user=request.user)

    walkower = Player.objects.filter(user=request.user, name='WALKOWER').first()
    if not walkower:
        p = Player()
        p.user = request.user
        p.name = "WALKOWER"
        p.save()

    if request.method == 'POST':
        form = CreateTournamentForm(request.user, request.POST)
        if form.is_valid():
            tournament_name_used = Tournament.objects.filter(
                user=request.user,
                name=request.POST['name']
            ).first()
            if not tournament_name_used:
                selected_players = list(form.cleaned_data.get('players'))
                if int(request.POST['max_players']) >= len(selected_players):
                    tournament = form.save(commit=False)
                    tournament.user = request.user
                    tournament.is_started = False
                    tournament.is_finished = False
                    tournament.save()

                    for player in selected_players:
                        tournament.players.add(player.id)
                    tournament.save()

                    messages.success(request, 'Turniej ' + tournament.name + ' utworzony pomyślnie')

                    return redirect('tournaments_list', 'planned')
                else:
                    messages.error(
                        request,
                        'Próbowano przypisać zbyt wielu Graczy (ustawiono limit ' +
                        str(request.POST['max_players']) + ' uczestników).'
                    )
            else:
                messages.error(request, 'Turniej o nazwie \"' + request.POST['name'] + '\" już istnieje.')
        else:
            messages.error(
                request,
                'Maksymalna liczba graczy musi być większa niż 2 oraz musi być minimum 1 przypisany gracz.'
            )

    context = {'form': form}
    return render(request, 'app/tournaments/add.html', context)


def all_tournaments_in_progress(request):
    title = "Wszystkie trawjące turnieje"
    tournaments = Tournament.objects.filter(
        is_started=True,
        is_finished=False
    )
    context = {'tournaments': tournaments, 'title': title}
    return render(request, 'app/tournaments/list.html', context)


def filtered_all_tournaments_in_progress(request):
    date_from = str(request.POST['date_from'])
    date_to = str(request.POST['date_to'])
    title = "Wszystkie trawjące turnieje"
    tournaments = Tournament.objects.filter(
        is_started=True,
        is_finished=False,
        start_date__gte=date_from,
        start_date__lte=date_to
    )
    context = {
        'tournaments': tournaments,
        'title': title,
        'period_time': date_from + ' - ' + date_to
    }
    return render(request, 'app/tournaments/list.html', context)


@allowed_users(allowed_roles=['user', 'admin'])
def tournaments_list(request, value):
    if value == 'all':
        if request.user.is_superuser:
            tournaments = Tournament.objects.all()
            title = "Wszystkie turnieje"
        else:
            messages.error(request, 'Nie jesteś administatorem')
            return redirect('home')
    elif value == 'planned':
        tournaments = Tournament.objects.filter(
            user=request.user,
            is_started=False,
            is_finished=False
        )
        title = "Turnieje zaplanowane"
    elif value == 'in_progress':
        tournaments = Tournament.objects.filter(
            user=request.user,
            is_started=True,
            is_finished=False
        )
        title = "Turnieje w trakcie"
    else:
        title = "Turnieje zakończone"
        tournaments = Tournament.objects.filter(
            user=request.user,
            is_started=False,
            is_finished=True
        )
    context = {'tournaments': tournaments, 'title': title}
    return render(request, 'app/tournaments/list.html', context)


@allowed_users(allowed_roles=['user', 'admin'])
def filtered_tournaments_list(request, value):
    date_from = str(request.POST['date_from'])
    date_to = str(request.POST['date_to'])
    if value == 'all':
        if request.user.is_superuser:
            tournaments = Tournament.objects.filter(
                start_date__gte=date_from,
                start_date__lte=date_to
            )
            title = "Wszystkie turnieje"
        else:
            messages.error(request, 'Nie jesteś administatorem')
            return redirect('home')
    elif value == 'planned':
        tournaments = Tournament.objects.filter(
            user=request.user,
            is_started=False,
            is_finished=False,
            start_date__gte=date_from,
            start_date__lte=date_to
        )
        title = "Turnieje zaplanowane"
    elif value == 'in_progress':
        tournaments = Tournament.objects.filter(
            user=request.user,
            is_started=True,
            is_finished=False,
            start_date__gte=date_from,
            start_date__lte=date_to
        )
        title = "Turnieje w trakcie"
    else:
        title = "Turnieje zakończone"
        tournaments = Tournament.objects.filter(
            user=request.user,
            is_started=False,
            is_finished=True,
            start_date__gte=date_from,
            start_date__lte=date_to
        )
    context = {
        'tournaments': tournaments,
        'title': title,
        'period_time': date_from + ' - ' + date_to
    }
    return render(request, 'app/tournaments/list.html', context)


@allowed_users(allowed_roles=['user', 'admin'])
def start_tournament(request, pk):
    if Tournament.objects.filter(pk=pk, user=request.user).first() or request.user.is_superuser:
        tournament = Tournament.objects.filter(id=pk).first()

        players = list(tournament.players.all())

        indexes = list(range(0, len(players)))
        np.random.shuffle(indexes)

        players_count = len(players)
        if players_count > 1:
            power_of_2 = 1
            round_count = 0
            while players_count > power_of_2:
                power_of_2 = power_of_2 * 2
                round_count += 1

            walkovers = power_of_2 - players_count
            arenas_in_first_round_count = power_of_2/2
            if walkovers != 0:
                walkover_every_how_many_arenas = arenas_in_first_round_count/walkovers
            arenas_with_walkovers = []

            while walkovers > 0:
                if not arenas_with_walkovers:
                    arenas_with_walkovers.append(1)
                else:
                    arenas_with_walkovers.append((arenas_with_walkovers[-1] + walkover_every_how_many_arenas)//1)
                walkovers -= 1
            walkover_instance = Player.objects.filter(name='WALKOWER').first()

            i = 1
            while round_count >= i:
                round_instance = Round()
                round_instance.tournament = tournament
                round_instance.round_number = i
                round_instance.save()
                if round_instance.round_number == 1:
                    for x in range(power_of_2//2):
                        arena = Arena()
                        arena.round = round_instance
                        arena.arena_number = x+1
                        arena.player1 = players[indexes.pop()]
                        if x+1 in arenas_with_walkovers:
                            arena.player2 = walkover_instance
                        else:
                            arena.player2 = players[indexes.pop()]
                        arena.save()

                        if arena.player2 == walkover_instance:
                            result = Result()
                            result.arena = arena
                            result.winner = arena.player1
                            result.result = '1:0'
                            result.save()
                i += 1

            tournament.is_started = True
            tournament.save()
            return redirect('/tournaments/detail/' + pk)
        else:
            messages.error(request, "Aby rozpocząć turniej, przypisz do niego minimum 2 graczy")
            return redirect('tournaments_list', 'planned')
    else:
        messages.error(request, 'Próba rozpoczęcia turnieju innego użytkownika')
        return redirect('tournaments_list', 'planned')


@allowed_users(allowed_roles=['user', 'admin'])
def finish_tournaments(request, pk):
    if Tournament.objects.filter(pk=pk, user=request.user).first() or request.user.is_superuser:
        tournament = Tournament.objects.filter(id=pk)
        tournament.update(is_finished=True, is_started=False)

        return redirect('tournaments_list', 'finished')
    else:
        messages.error(request, 'Próba zakończenia turnieju innego użytkownika')
        return redirect('tournaments_list', 'planned')
