from django import forms
from .models import *

class AddPlayer(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Player
        fields = ['name','date_birth','role','citizenship','number']