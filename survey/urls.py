# survey/urls.py
from django.urls import path
from survey import views
from .views import StudentSurveyListView, SubmissionCreateView, SurveyCreateView, SurveyIntroView, SurveyListView, SurveyUpdateView,SurveyDeleteView

urlpatterns = [
    path('c/view-surveys/', SurveyListView.as_view(), name='coordinator_survey_list_view'),
    path('c/create-survey/', SurveyCreateView.as_view(), name='create_survey'),
    path('c/<int:survey_id>/update-survey/', SurveyUpdateView.as_view(), name='update_survey'),
    path('c/<int:survey_id>/delete-survey/', SurveyDeleteView.as_view(), name='delete_survey'),
    path('c/<int:survey_id>/create-question/', views.QuestionCreateView.as_view(), name='create_question'),
    path('c/<int:survey_id>/update-question/<int:question_id>', views.QuestionUpdateView.as_view(), name='update_question'),
    path('c/<int:survey_id>/delete-question/<int:question_id>', views.QuestionDeleteView.as_view(), name='delete_question'),
    path('s/view-surveys/', StudentSurveyListView.as_view(), name='student_survey_list_view'),
    path('s/<int:survey_id>/survey-intro/', SurveyIntroView.as_view(), name='survey_intro_view'),
    path('s/<int:survey_id>/submit-survey/<int:submission_id>', SubmissionCreateView.as_view(), name='create_submission'),
]
