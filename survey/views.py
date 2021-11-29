from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import messages
from django.db import transaction
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView

from .models import Question, Submission, Survey
from accounts.models import Coordinator, Student, User
from .forms import AddDuplicateQuestionForm, QuestionFormset, QuestionModelForm, SurveyModelForm
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

class UserIsCoordinatorMixin:

    def dispatch(self, request, *args, **kwargs):
        if Coordinator.objects.filter(user_id = self.request.user.id):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class UserIsStudentMixin:

    def dispatch(self, request, *args, **kwargs):
        if Student.objects.filter(user_id = self.request.user.id):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class SurveyListView(UserIsCoordinatorMixin, LoginRequiredMixin, ListView):
    model = Survey
    template_name = 'view_surveys.html'

    
    def get_queryset(self):
        coordinator = Coordinator.objects.get(user_id = self.request.user.id)
        return Survey.objects.filter(coordinator_id = coordinator.id)

    def get_context_data(self):
        context = super().get_context_data()
        coordinator = Coordinator.objects.get(user_id = self.request.user.id)
        context['user'] = self.request.user
        context['surveys'] = Survey.objects.filter(coordinator_id = coordinator.id)
        return context

class SurveyCreateView(LoginRequiredMixin, CreateView):
    model = Survey
    fields = [
        'spe_number',
        'introductory_text',
        'date_opened',
        'date_closed',
        ]
    template_name = 'create_survey.html'
    success_url = reverse_lazy('view_surveys')
    success_message = 'Success: Survey was created'

    """
    def get_object(self, queryset=None):
        # Generate autoid
        last_survey = Survey.objects.latest('id')
        auto_id = last_survey.id + 1

        # Get coordinator
        coordinator_obj = Coordinator.objects.get(user_id = self.request.user.id)

        object = Survey(id = auto_id, coordinator_id = coordinator_obj.id)

        return object
    """

    def get_context_data(self, **kwargs):
        context = super(SurveyCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['questions'] = QuestionFormset(self.request.POST)
        else:
            context['questions'] = QuestionFormset()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']

        with transaction.atomic():
            self.object = form.save()

            if questions.is_valid():
                questions.instance = self.object
                questions.save()
            
        return super(SurveyCreateView, self).form_valid(form)

    """
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = self.form_class(request.POST)
        s = self.get_object()
        print(f"Survey ID at post(): {s.id}")

        if s.questions.count() > 1:
            if form.is_valid():
                return HttpResponseRedirect(reverse('view_surveys'))
            else:
                return HttpResponseRedirect(reverse('create_survey'))
        else: 
            messages.error(request, "Error: A survey must have at least 1 question.")
            return HttpResponseRedirect(reverse('create_survey'))
    """

class SurveyUpdateQuestionsView(LoginRequiredMixin, UpdateView): 
    
    model = Survey
    form_class = SurveyModelForm
    template_name = 'update_survey_questions.html'

    def get_initial(self):
        initial = super(SurveyUpdateQuestionsView, self).get_initial()
        initial = initial.copy()
        s = Survey.objects.get(id = self.kwargs['survey_id'])
        initial['spe_number'] = s.spe_number
        initial['introductory_text'] = s.introductory_text
        initial['date_opened'] = s.date_opened
        initial['date_closed'] = s.date_closed

        return initial

    
    def get_context_data(self):
        context = super().get_context_data()
        s = Survey.objects.get(id=self.kwargs['survey_id'])
        context['survey'] = s
        questions = s.questions.all()
        context['questions'] = questions

        return context

    
    def get_object(self, queryset=None):
        object = get_object_or_404(Survey, id=self.kwargs['survey_id'])
        return object


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        survey_id = self.kwargs['survey_id']
        questions = self.kwargs['questions']

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_surveys'))
        else:
            return HttpResponseRedirect(reverse('view_surveys'))


    def get_success_url(self):
        return reverse_lazy('view_surveys')

    success_message = 'Success: Question was created'


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'create_question.html'
    form_class = QuestionModelForm
    success_message = 'Success: Question created.'
    
    def get_success_url(self):
        survey_id=self.kwargs['survey_id']
        return reverse_lazy('update_survey_questions', kwargs={'survey_id': survey_id})

    def post(self, request, *args, **kwargs):
        """Override post() so that question is related to current survey being edited, in addition to just the question object creation."""

        form = self.form_class(request.POST)
        survey = Survey.objects.get(id=self.kwargs['survey_id'])

        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            survey.questions.add(question)
            
            form.save()
            return HttpResponseRedirect(reverse_lazy('update_survey_questions', kwargs = {'survey_id': survey.id}))

            
    
class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'update_question.html'
    form_class = QuestionModelForm
    success_message = 'Success: Question updated.'
    success_url = reverse_lazy('')
    
    def get_success_url(self):
        survey_id=self.kwargs['survey_id']
        return reverse_lazy('update_survey_questions', kwargs={'survey_id': survey_id})

    def get_object(self, queryset=None):
        object = get_object_or_404(Question, id=self.kwargs['question_id'])
        return object
    

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'delete_question.html'
    success_message = 'Success: Question was deleted'
    
    def get_success_url(self):
        survey_id=self.kwargs['survey_id']
        return reverse_lazy('update_survey_questions', kwargs={'survey_id': survey_id})

    def get_object(self, queryset=None):
        object = get_object_or_404(Question, id=self.kwargs['question_id'])
        return object


class TempQuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'create_question.html'
    form_class = QuestionModelForm
    success_message = 'Success: Question created.'
    

    def post(self, request, *args, **kwargs):
        """Override post() so that question is related to current survey being edited, in addition to just the question object creation."""

        form = self.form_class(request.POST)
        survey = Survey.objects.get(id=self.kwargs['survey_id'])

        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            survey.questions.add(question)
            
            form.save()
            return HttpResponseRedirect(reverse_lazy('update_survey_questions', kwargs = {'survey_id': survey.id}))


class TempAddDuplicateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'add_duplicate_question.html'
    form_class = AddDuplicateQuestionForm
    success_message = 'Success: Duplicate question was added'

    def get_success_url(self):
        survey_id=self.kwargs['survey_id']
        return reverse_lazy('create_survey', kwargs={'survey_id': survey_id})

    
    def get_object(self, queryset=None):
        object = Survey(id = self.kwargs['survey_id'], coordinator_id = c.id)
        return object

    
    def get_form_kwargs(self):
        form_kwargs =  super().get_form_kwargs()
        form_kwargs['survey_id'] = self.kwargs['survey_id']
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def post(self, request, *args, **kwargs):
        """Override post() so that question is related to current survey being edited, in addition to just the question object creation."""

        form = self.form_class(request.POST, survey_id = self.kwargs['survey_id'], user = self.request.user)
        # survey = Survey.objects.get(id=self.kwargs['survey_id'])
        survey = self.get_object()
        

        if form.is_valid():
            questions = form.cleaned_data.get('questions')
            # for q in questions:
                # print("q")
                # survey.questions.add(q)
                
            return HttpResponseRedirect(reverse_lazy(self.get_success_url(), kwargs = {'survey_id': survey.id, 'questions': questions}))


class AddDuplicateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'add_duplicate_question.html'
    form_class = AddDuplicateQuestionForm
    success_message = 'Success: Duplicate question was added'

    def get_success_url(self):
        survey_id=self.kwargs['survey_id']
        return reverse_lazy('update_survey_questions', kwargs={'survey_id': survey_id})

    
    def get_object(self, queryset=None):
        object = Survey.objects.get(id = self.kwargs['survey_id'])
        return object

    
    def get_form_kwargs(self):
        form_kwargs =  super().get_form_kwargs()
        form_kwargs['survey_id'] = self.kwargs['survey_id']
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def post(self, request, *args, **kwargs):
        """Override post() so that question is related to current survey being edited, in addition to just the question object creation."""

        form = self.form_class(request.POST, survey_id = self.kwargs['survey_id'], user = self.request.user)
        # survey = Survey.objects.get(id=self.kwargs['survey_id'])
        survey = self.get_object()
        questions = survey.questions.all()

        if form.is_valid():
            for q in questions:
                survey.questions.add(q)
                
            return HttpResponseRedirect(reverse_lazy(self.get_success_url(), kwargs = {'survey_id': survey.id}))

    
class StudentSurveyListView(LoginRequiredMixin, UserIsStudentMixin, ListView):
    print()


class SubmissionCreateView(LoginRequiredMixin, UserIsStudentMixin, CreateView):
    model = Submission
    template_name = 'add_submission.html'
    

