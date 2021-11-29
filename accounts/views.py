from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied

from .models import User, Student, Coordinator
# Create your views here.

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