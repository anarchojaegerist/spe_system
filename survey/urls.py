# survey/urls.py
from django.urls import path
from survey import views
from .views import create_survey, display_surveys, edit_survey

urlpatterns = [
    path('create-survey/', create_survey, name='create_survey'),
    path('view-all/', display_surveys, name='surveys'),
    path('<int:pk>/edit/', edit_survey, name='edit-survey'),
    path('create-question/', views.QuestionCreateView.as_view(), name='create_question'),
]
