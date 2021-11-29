from django.db.models import query
from django.forms import ModelForm, ChoiceField, CheckboxSelectMultiple, inlineformset_factory
from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import widgets, Select, SelectMultiple
from django.forms.fields import DateTimeField, MultipleChoiceField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import DateTimeInput
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Comment, Question, Rating, Submission, Survey, Coordinator, Evaluation

class QuestionModelForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


QuestionFormset = inlineformset_factory(
    Survey, Survey.questions.through, form = QuestionModelForm, fields = '__all__'
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

    """
    def __init__(self, *args, **kwargs):
        super(SurveyModelForm, self).__init__(*args, **kwargs)

        if 'survey_id' in kwargs:
            survey_id = kwargs.pop('survey_id')
            s = Survey.objects.get(id = survey_id)
            self.fields['questions'] = ModelMultipleChoiceField(
                widget = CheckboxSelectMultiple,
                queryset = Question.objects.exclude(survey=s))
        else:
            self.fields['questions'] = ModelMultipleChoiceField(
                widget = CheckboxSelectMultiple,
                queryset = Question.objects.all())
    """

"""
class SurveyModelForm(ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        widgets = {
            'questions': ModelMultipleChoiceField(queryset=Question.objects.all(), widget=FilteredSelectMultiple("Title", is_stacked=False, required=True))
        }

    class Media:
        css = {
            'all': ('../Lib/site-packages/django/contrib/admin/static/admin/css/widgets.css')
        }
        js = ('../static/js/jsi18n')

    def clean_questions(self):
        questions = self.cleaned_data['questions']
        return questions
"""


class AddDuplicateQuestionForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['questions']

    def __init__(self, *args, **kwargs):
        
        survey_id = kwargs.pop('survey_id')
        u = kwargs.pop('user')
        super(AddDuplicateQuestionForm, self).__init__(*args, **kwargs)
        try:
            s = Survey.objects.get(id = survey_id)
        except ObjectDoesNotExist:
            c = Coordinator.objects.get(user_id = u.id)
            s = Survey(id = survey_id, coordinator_id = c.id)
    
        # Exclude question objects that are related to the same survey as current survey object 
        self.fields['questions'] = ModelMultipleChoiceField(
            widget = CheckboxSelectMultiple,
            queryset = Question.objects.exclude(survey=s))



class RatingModelForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['answer']


RatingFormset = inlineformset_factory(
    Evaluation, Rating, fields = ['answer']
)


class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['answer']


CommentFormset = inlineformset_factory(
    Evaluation, Comment, fields = ['answer']
)