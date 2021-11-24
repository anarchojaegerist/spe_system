from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Comment, Question, Rating, Survey

class QuestionModelForm(BSModalModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class addSurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = [
            'spe_number',
            'introductory_text',
            'date_opened',
            'date_closed',
        ]

class addRatingAnswer(ModelForm):
    class Meta:
        model = Rating
        fields = ['answer']


class addCommentAnswer(ModelForm):
    class Meta:
        model = Comment
        fields = ['answer']