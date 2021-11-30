from django.forms.models import modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView

from .models import Question, Submission, Survey
from accounts.models import Coordinator, Student, User
from dashboard.models import Offering, Team
from .forms import AddDuplicateQuestionForm, QuestionFormset, QuestionModelForm, SurveyModelForm
from accounts.views import UserIsStudentMixin, UserIsCoordinatorMixin
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
    QuestionFormset = modelformset_factory(Question, form=QuestionModelForm, extra=3)
    
    def get_context_data(self, **kwargs):
        context = super(SurveyCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['questions'] = QuestionFormset(queryset=Question.objects.none())
            # context['questions'] = QuestionFormset(self.request.POST, instance=self.object)
        else:
            context['questions'] = QuestionFormset(instance=self.object)
            # context['questions'] = QuestionFormset(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']

        with transaction.atomic():
            coordinator_object = Coordinator.objects.get(user_id = self.request.user.id)
            print(form)
            self.object = form.save(commit=False)
            self.object.coordinator_id = coordinator_object.id

            if questions.is_valid():
                questions.instance = self.object
                questions.save()
            
        return super(SurveyCreateView, self).form_valid(form)


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
    model = Survey
    template_name = 'student_survey_list_view.html'

    """
    def get_queryset(self):
        student_object = Student.objects.get(user_id = self.request.user.id)
        offering_object = Offering.objects.none()

        for o in Offering.objects.all():
            if student_object in o.students.all():
                offering_object = o
                
        return Survey.offerings.filter(offering_id = offering_object.id)
    """

    def get_context_data(self):
        context = super().get_context_data()
        student_object = Student.objects.get(user_id = self.request.user.id)
        offering_object = Offering.objects.none()

        for o in Offering.objects.all():
            if o.unit_code == 'ICT302' and student_object in o.students.all():
                offering_object = o 
                break

        context['user'] = self.request.user
        context['offering'] = offering_object
        context['surveys'] = offering_object.surveys.all()
        return context


class SurveyIntroView(LoginRequiredMixin, UserIsStudentMixin, TemplateView):
    model = Survey
    template_name = 'survey_intro.html'
    print()

    def get_context_data(self):
        context = super().get_context_data()
        team_members = []
        student_object = Student.objects.get(user_id = self.request.user.id)
        team_object = Team.objects.none()
        survey_object = Survey.objects.get(id = self.kwargs['survey_id'])

        for t in Team.objects.all():
            if student_object in t.students.all():
                team_object = t

        for member in team_object.students.all():
            member_user = User.objects.get(id = member.user_id)
            team_members.append({
                'given_names': member_user.given_names,
                'last_name': member_user.last_name
            })

        context['survey'] = survey_object
        context['members'] = team_members

        return context

class SubmissionCreateView(LoginRequiredMixin, UserIsStudentMixin, CreateView):
    model = Submission
    template_name = 'add_submission.html'
    

