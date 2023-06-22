from django import forms
from app.models import Tournament, Player


class CreateTournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = '__all__'
        exclude = ['is_started', 'is_finished', 'user']

        widgets = {
            'start_date': forms.DateInput(
                format='%d-%m-%Y',
                attrs={'class': 'form-control',
                       'type': 'date'
                       }),
            'players': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, user, *args, **kwargs):
        super(CreateTournamentForm, self).__init__(*args, **kwargs)
        self.fields['players'].queryset = Player.objects.exclude(name="WALKOWER").filter(user=user)


class UpdateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'
        exclude = ['is_started', 'is_finished', 'user']

        widgets = {
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control',
                       'type': 'date'
                       }),
            'players': forms.CheckboxSelectMultiple(),
        }
