from django.forms import ModelForm
from django import forms
from .models import File

class CsvForm(ModelForm):
    class Meta:
        model = File
        fields = {'file_name'}
