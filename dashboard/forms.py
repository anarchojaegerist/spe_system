from django.forms import ModelForm
from django import forms
from .models import Alert, File

class ReplyForm(forms.Form):
    title = forms.CharField(label='Reply title', max_length=60)
    body = forms.CharField(label='Reply body', max_length=1000)


class AlertModelForm(ModelForm):
    class Meta:
        model = Alert
        fields = [
            'student',
            'coordinator',
            'title',
            'body',
        ]

    def __init__(self, *args, **kwargs):

        print()
        
    

class CsvForm(ModelForm):
    class Meta:
        model = File
        fields = {'file_name'}


