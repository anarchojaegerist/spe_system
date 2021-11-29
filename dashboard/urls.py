# dashboard/urls.py
from django.urls import path
from .views import CoordinatorAlertDetailView, CoordinatorAlertListView, MessageCreateView, ReplyFormView, campus_view, create_team_report, team_view, student_view, student_list

urlpatterns = [
    path('campus-view/', campus_view, name='campus_view'),
    path('<int:pk>/campus-team-view/', team_view, name='team_view'),
    path('<int:pk>/team-student-view/', student_view, name='student_view'),
    path('<int:pk>/create-team-report/', create_team_report, name='create_team_report'),
    path('student-list/', student_list, name='student_list'),
    path('c/alert-list-view/', CoordinatorAlertListView.as_view(), name='coordinator_alert_list_view'),
    path('c/<int:alert_id>/alert-detail-view', CoordinatorAlertDetailView.as_view(), name='coordinator_alert_detail_view'),
    path('c/<int:alert_id>/alert-reply', ReplyFormView.as_view(), name='alert_reply_form'),
    path('c/<int:alert_id>/add-reply', MessageCreateView.as_view(), name='add_message')
]