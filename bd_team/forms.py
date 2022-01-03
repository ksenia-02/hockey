from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, AbstractUser

from .models import *


class PlayerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].empthy_label = "Игровая позиция не выбрана"

    class Meta:
        model = Player
        fields = ['name', 'date_birth', 'role', 'citizenship', 'number', 'photo', 'biog', 'indicator', 'public_photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'citizenship': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Game
        fields = ['date', 'opponent', 'area', 'role', 'score']


class GamePlayerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Player_Game
        fields = ['player', 'game', 'count_washers', 'yellow_card', 'read_card']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин  ', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль  ', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Player
        fields = ['name', 'date_birth', 'role', 'citizenship', 'number', 'photo', 'biog', 'indicator', 'public_photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'citizenship': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
