# dashboard/urls.py
from django.urls import path
from .views import student_list

urlpatterns = [
    path('student-list/', student_list, name='student_list'),
]