from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView

from .models import Question, Survey
from accounts.models import Coordinator, User
from .forms import QuestionModelForm
import logging

# Create your views here.

@login_required
def display_surveys(request):
    coordinator = Coordinator.objects.get(user_id = request.user.id)
    surveys = Survey.objects.filter(coordinator_id = coordinator.id)

    context = {
        'surveys':surveys,
        'user':request.user
    }
    return render(request, '../templates/view_surveys.html', context)


@login_required
def create_survey(request):
    questions = Survey.questions.all()
    # questions = Question.objects.all()
    template_name = 'create_survey.html'
    context = {
        'questions':questions
    }
    return render(request,'create-survey.html',context)


@login_required
def edit_survey(request, pk):
    s = Survey.objects.get(id=pk)
    questions = s.questions.all()
    template_name = 'edit_survey.html'
    context = {
        'questions':questions,
        'survey':s,
    }
    return render(request,'edit_survey.html',context)


class SurveyUpdateView(UpdateView): # new
    model = Survey
    fields = ('spe_number', 'introductory_text', 'date_opened',
    'date_closed', 'questions')
    template_name = 'survey_edit.html'
    success_message = 'Success: Question was created'
    sucess_url = reverse_lazy('')


class QuestionCreateView(BSModalCreateView):
    template_name = 'create_question.html'
    form_class = QuestionModelForm
    success_message = 'Success: Question created.'
    success_url = reverse_lazy('dashboard')


class QuestionUpdateView(BSModalUpdateView):
    model = Question
    template_name = 'update_question.html'
    form_class = QuestionModelForm
    success_message = 'Success: Question was updated'
    success_url = reverse_lazy('')


class QuestionDeleteView(BSModalDeleteView):
    model = Question
    template_name = 'delete_question.html'
    success_message = 'Success: Question was deleted'
    success_url = reverse_lazy('')
    
