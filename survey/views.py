from django.forms.models import modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms.widgets import DateTimeInput, HiddenInput
from django.urls import reverse
from django.db import transaction
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView

from .models import Evaluation, Question, Submission, Survey, Answer
from accounts.models import Coordinator, Student, User
from dashboard.models import Offering, Team
from .forms import AnswerFormSet, AnswerModelForm, QuestionFormset, QuestionModelForm, SurveyModelForm
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
    template_name = 'coordinator_survey_list_view.html'

    
    def get_queryset(self):
        coordinator = Coordinator.objects.get(user_id = self.request.user.id)
        return Survey.objects.filter(coordinator_id = coordinator.id)

    def get_context_data(self):
        context = super().get_context_data()
        coordinator = Coordinator.objects.get(user_id = self.request.user.id)
        context['user'] = self.request.user
        context['surveys'] = Survey.objects.filter(coordinator_id = coordinator.id)
        return context

def survey_create_view(request):
    form = SurveyModelForm()
    formset = QuestionFormset(instance=Survey())
    if request.method == 'POST':
        form = SurveyModelForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            formset = QuestionFormset(request.POST, request.FILES,
                instance=lesson)
            if formset.is_valid():
                formset.save()
                return render(request, 'coordinator_survey_list_view',)
    return render(request, "page.html", {
        'form': form, 'formset': formset
    })

class SurveyCreateView(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyModelForm
    template_name = 'create_survey.html'
    success_url = reverse_lazy('coordinator_survey_list_view')
    success_message = 'Success: Survey was created'
    formset = modelformset_factory(Question, form=QuestionModelForm, extra=3)
    
    def get_context_data(self, **kwargs):
        context = super(SurveyCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['questions'] = QuestionFormset(queryset=Question.objects.none())
        else:
            context['questions'] = QuestionFormset(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        """Override post() so that question is related to current survey being edited, in addition to just the question object creation."""

        form = self.form_class(request.POST)
        formset = self.formset(request.POST)
        coordinator_object = Coordinator.objects.get(user_id = request.user.id)

        if form.is_valid():
            survey = form.save(commit=False)
            survey.coordinator_id = coordinator_object.id

            for f in formset:
                question = f.save(commit=False)
                question.save()
                survey.questions.add(question)
            
            form.save()
            return HttpResponseRedirect(reverse_lazy('coordinator_survey_list_view'))


class SurveyUpdateView(LoginRequiredMixin, UpdateView): 
    
    model = Survey
    form_class = SurveyModelForm
    template_name = 'update_survey.html'
    formset = modelformset_factory(Question, form=QuestionModelForm, extra=0)

    def get_context_data(self, **kwargs):
        context = super(SurveyUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['questions'] = QuestionFormset(queryset=Question.objects.none())
        else:
            context['questions'] = QuestionFormset(instance=self.object)

        return context

    
    def get_object(self, queryset=None):
        object = get_object_or_404(Survey, id=self.kwargs['survey_id'])
        return object


    def get_success_url(self):
        return reverse_lazy('coordinator_survey_list_view')

    def post(self, request, *args, **kwargs):
        """Override post() so that question is related to current survey being edited, in addition to just the question object creation."""

        form = self.form_class(request.POST, request.FILES)
        formset = self.formset(request.POST, request.FILES)
        formset.save()
        coordinator_object = Coordinator.objects.get(user_id = request.user.id)
        print(formset.is_valid())
        print(formset.non_form_errors())
        print(formset.errors)

        if form.is_valid():
            survey = form.save(commit=False)
            survey.coordinator_id = coordinator_object.id

            for f in formset:
                question = f.save(commit=False)
                print(question)
                question.save()
                survey.questions.add(question)
            
            form.save()
            return HttpResponseRedirect(reverse_lazy('coordinator_survey_list_view'))

    success_message = 'Success: Question was created'


class SurveyDeleteView(LoginRequiredMixin, DeleteView):
    model = Survey
    template_name = 'delete_survey.html'
    success_message = 'Success: Survey was deleted'
    
    def get_success_url(self):
        return reverse_lazy('coordinator_survey_list_view')

    def get_object(self, queryset=None):
        object = get_object_or_404(Survey, id=self.kwargs['survey_id'])
        return object


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'create_question.html'
    form_class = QuestionModelForm
    success_message = 'Success: Question created.'
    success_url = reverse_lazy('coordinator_survey_list_view')

    def post(self, request, *args, **kwargs):
        """Override post() so that question is related to current survey being edited, in addition to just the question object creation."""

        form = self.form_class(request.POST)
        survey = Survey.objects.get(id=self.kwargs['survey_id'])

        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            survey.questions.add(question)
            
            form.save()
            return HttpResponseRedirect(reverse_lazy('coordinator_survey_list_view'))

            
    
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

    def get_object(self, queryset=None):
        object = Survey.objects.get(id = self.kwargs['survey_id'])
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        team_members = []
        student_object = Student.objects.get(user_id = self.request.user.id)
        team_object = Team.objects.none()
        survey_object = Survey.objects.get(id = kwargs['survey_id'])
        submission_object = Submission.objects.create(
            student = student_object,
            survey = survey_object,
            spe_number = survey_object.spe_number
        )

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
        context['submission'] = submission_object

        return context

class SubmissionCreateView(LoginRequiredMixin, UserIsStudentMixin, UpdateView):
    model = Submission
    template_name = 'add_submission.html'
    fields = '__all__'
    AnswerFormSet = modelformset_factory(Answer, form=AnswerModelForm, extra=0)

    def get_object(self, queryset=None):
        survey_object = Survey.objects.get(id = self.kwargs['survey_id'])
        
        return survey_object

    def get_context_data(self, **kwargs):
        print(self.kwargs['survey_id'])
        context = super().get_context_data(**kwargs)
        submission_object = Submission.objects.get(id = self.kwargs['submission_id'])
        survey_object = Survey.objects.get(id = self.kwargs['survey_id'])
        student_object = Student.objects.get(user_id = self.request.user.id)
        team_object = Team.objects.get(id = student_object.team_id)

        for s in team_object.students.all():

            if s.id == student_object.id:
                evaluation_object = Evaluation.objects.create(
                    student = student_object, 
                    evaluatee = student_object, 
                    submission = submission_object,
                    type = 'S'
                )
                
                """
                evaluations.append(Evaluation.objects.create(
                    student = student_object, 
                    evaluatee = student_object, 
                    submission = submission_object,
                    type = 'S'
                
                ))
                """
                # Get self evaluation questions from survey
                for q in survey_object.questions.all():
                    
                    if q.evaluation_type == 'S':
                        a = Answer.objects.create(
                            question = q, evaluation = evaluation_object,)
                        evaluation_object.answers.add(a)
            else:
                evaluation_object = Evaluation.objects.create(
                    student = student_object, 
                    evaluatee = s, 
                    submission = submission_object,
                    type = 'P'
                )
                """
                evaluations.append(Evaluation.objects.create(
                    student = student_object,
                    evaluatee = s,
                    submission = submission_object,
                    type = 'P'
                ))
                """
                for q in survey_object.questions.all():
                    
                    if q.evaluation_type == 'P':
                        a = Answer.objects.create(
                            question = q, evaluation = evaluation_object,)
                        evaluation_object.answers.add(a)
            
            submission_object.evaluations.add(evaluation_object)

        if self.request.POST:
            context['evaluations'] = QuestionFormset(queryset=Evaluation.objects.none())
        else:
            context['evaluations'] = QuestionFormset(instance=self.object)
        return context
    
    


