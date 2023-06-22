from django.shortcuts import render, redirect
from app.decorators import allowed_users
from app.models import Player
from app.forms.players_form import CreatePlayerForm
from django.contrib import messages


@allowed_users(allowed_roles=['user', 'admin'])
def delete_players(request, pk):
    model = Player.objects.filter(pk=pk).first()
    if Player.objects.filter(pk=pk, user=request.user).first() or request.user.is_superuser:
        if request.method == 'POST':
            if model.name != "WALKOWER":
                model.delete()
                messages.success(request, 'Pomyślnie usunięto gracza')
    else:
        messages.error(request, 'Próba usunięcia gracza innego użytkownika')
    return redirect('my_players_list')


@allowed_users(allowed_roles=['user', 'admin'])
def update_player(request, pk):
    model = Player.objects.filter(pk=pk)
    instance = model.first()
    form = CreatePlayerForm(instance=instance)
    if request.method == 'POST':
        if Player.objects.filter(pk=pk, user=request.user).first() or request.user.is_superuser:
            form = CreatePlayerForm(request.POST)
            if form.is_valid():
                model.filter(pk=pk).update(name=str(request.POST['name']))
                messages.success(request, 'Gracz ' + str(request.POST['name']) + ' edytowany pomyślnie.')
                return redirect('my_players_list')
        else:
            messages.error(request, 'Próba edycji gracza innego użytkownika')
    context = {'form': form}
    return render(request, 'app/players/update.html', context)


@allowed_users(allowed_roles=['user', 'admin'])
def create_player(request):
    form = CreatePlayerForm()
    if request.method == 'POST':
        player_name_used = Player.objects.filter(user=request.user, name=request.POST['name']).first()
        if request.POST['name'] == "WALKOWER":
            messages.error(request, 'Nazwa \"WALKOWER\" jest niedostępna.')
        elif player_name_used:
            messages.error(request, 'Gracz o nazwie \"' + request.POST['name'] + '\" już istnieje.')
        else:
            form = CreatePlayerForm(request.POST)
            if form.is_valid():
                player = form.save(commit=False)
                player.user = request.user
                player.save()

                messages.success(request, 'Gracz ' + player.name + ' dodany pomyślnie')
                return redirect('my_players_list')
    context = {'form': form}
    return render(request, 'app/players/add.html', context)


@allowed_users(allowed_roles=['user', 'admin'])
def my_players_list(request):
    players = Player.objects.exclude(name="WALKOWER").filter(user=request.user)
    context = {'players': players}
    return render(request, 'app/players/list.html', context)


@allowed_users(allowed_roles=['user', 'admin'])
def all_players_list(request):
    if request.user.is_superuser:
        players = Player.objects.exclude(name="WALKOWER").filter
        context = {'players': players}
        return render(request, 'app/players/list.html', context)
    messages.error(request, 'Nie jesteś administatorem')
    return redirect('home')
