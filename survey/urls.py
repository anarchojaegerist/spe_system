# survey/urls.py
from django.urls import path
from survey import views
from .views import create_survey, display_surveys, edit_survey

urlpatterns = [
    path('create-survey/', create_survey, name='create_survey'),
    path('view-surveys/', display_surveys, name='surveys'),
    path('<int:pk>/edit/', edit_survey, name='edit_survey'),
    path('<int:pk>/create-question', views.QuestionCreateView.as_view(), name='create_question'),
    path('<int:pk>/update-question/<int:pk_2>', views.QuestionUpdateView.as_view(), name='update_question'),
    path('<int:pk>/delete-question/<int:pk_2>', views.QuestionDeleteView.as_view(), name='delete_question'),
]
