from django import forms
from app.models import Player


class CreatePlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = '__all__'
        exclude = ('user',)
