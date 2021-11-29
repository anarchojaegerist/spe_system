# survey/urls.py
from django.urls import path
from survey import views
from .views import SurveyCreateView, SurveyListView

urlpatterns = [
    path('create-survey/', SurveyCreateView.as_view(), name='create_survey'),
    path('view-surveys/', SurveyListView.as_view(), name='view_surveys'),
    path('<int:survey_id>/update-survey-questions/', views.SurveyUpdateQuestionsView.as_view(), name='update_survey_questions'),
    path('<int:survey_id>/create-question/', views.QuestionCreateView.as_view(), name='create_question'),
    path('<int:survey_id>/update-question/<int:question_id>', views.QuestionUpdateView.as_view(), name='update_question'),
    path('<int:survey_id>/delete-question/<int:question_id>', views.QuestionDeleteView.as_view(), name='delete_question'),
    path('<int:survey_id>/add-duplicate-question', views.AddDuplicateQuestionView.as_view(), name='add_duplicate_question'),
    path('temp-add-duplicate-question', views.TempAddDuplicateQuestionView.as_view(), name='temp_add_duplicate_question'),
    path('student/view-surveys/', SurveyListView.as_view(), name='student_view_surveys'),
]
