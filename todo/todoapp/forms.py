from . models import *
from django import forms

class UpdateForm(forms.ModelForm):
    class Meta:
        model=Task
        fields = ['name', 'priority', 'date']