from django import forms
from django import forms
from .models import Task


class Taskform(forms.ModelForm):
    class Meta:
        model= Task
        fields = ['title','description','important']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':  'Escribe el titulo'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder':  'Escribe descripcion de la tarea'}),
            'important' : forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
