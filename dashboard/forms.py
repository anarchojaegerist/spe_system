from django.forms import ModelForm
from django import forms
from .models import File

class ReplyForm(forms.Form):
    title = forms.CharField(label='Reply title', max_length=60)
    body = forms.CharField(label='Reply body', max_length=1000)


class CsvForm(ModelForm):
    class Meta:
        model = File
        fields = {'file_name'}


