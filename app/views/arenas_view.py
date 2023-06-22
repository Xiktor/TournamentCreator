from django.shortcuts import redirect, render

from app.decorators import allowed_users
from app.forms.results_form import ResultsForm, CreateResultForm
from app.models.arena_model import Arena


@allowed_users(allowed_roles=['user', 'admin'])
def enter_result(request, pk):
    arena = Arena.objects.filter(pk=pk).first()
    form = ResultsForm(arena)
    if request.method == 'POST':
        form = CreateResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.arena = arena
            result.save()

            return redirect('/tournaments/detail/' + str(arena.round.tournament.id))

    context = {'form': form}
    return render(request, 'app/arenas/enter_result.html', context)
