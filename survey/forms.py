from django.db.models import query
from django.forms import ModelForm, ChoiceField, CheckboxSelectMultiple, inlineformset_factory
from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import widgets, Select, SelectMultiple
from django.forms.fields import DateTimeField, MultipleChoiceField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import DateTimeInput, HiddenInput
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Answer, Question, Submission, Survey, Coordinator, Evaluation

class QuestionModelForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


QuestionFormset = inlineformset_factory(
    Survey, Survey.questions.through, form = QuestionModelForm, fields = '__all__', extra=1
)

class SurveyModelForm(ModelForm):
    class Meta:
        model = Survey
        fields = [
            'spe_number',
            'introductory_text',
            'date_opened',
            'date_closed',
        ]
        widgets = {
            'date_opened': DateTimeInput(attrs={'type': 'date'}),
            'date_closed': DateTimeInput(attrs={'type': 'date'})
        }


class AnswerModelForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        super(AnswerModelForm, self).__init__(*args, **kwargs)

        type = kwargs.pop('type')
        if type == 'R':
            self.fields['comment'].widget = HiddenInput()
        else:
            self.fields['rating'].widget = HiddenInput()

AnswerFormSet = inlineformset_factory(
    Evaluation, Answer, form = AnswerModelForm
)
