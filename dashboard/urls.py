# dashboard/urls.py
from django.urls import path
from .views import campus_view, create_team_report, team_view, student_view, student_list

urlpatterns = [
    path('campus-view/', campus_view, name='campus_view'),
    path('<int:pk>/campus-team-view/', team_view, name='team_view'),
    path('<int:pk>/team-student-view/', student_view, name='student_view'),
    path('<int:pk>/create-team-report/', create_team_report, name='create_team_report'),
    path('student-list/', student_list, name='student_list'),
]