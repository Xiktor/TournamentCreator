from django import forms
from app.models import Result, Player


class ResultsForm(forms.ModelForm):

    class Meta:
        model = Result
        fields = '__all__'
        exclude = ('arena', )

    def __init__(self, arena, *args, **kwargs):
        super(ResultsForm, self).__init__(*args, **kwargs)
        self.fields['winner'].queryset = Player.objects.exclude(name="WALKOWER")\
            .filter(id__in=(arena.player1.id, arena.player2.id))


class CreateResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        exclude = ('arena', )
