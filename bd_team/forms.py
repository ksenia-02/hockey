from django import forms
from .models import *

class PlayerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].empthy_label = "Игровая позиция не выбрана"

    class Meta:
        model = Player
        fields = ['name','date_birth','role','citizenship','number', 'photo']
        widgets = {
            'name': forms.TextInput(attrs = {'class':'form-control'}),
            'date_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'citizenship': forms.TextInput(attrs={'class': 'form-control'}),
        }
class GameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Game
        fields = ['date', 'opponent', 'area', 'role', 'score']
