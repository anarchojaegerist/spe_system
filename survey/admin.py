from django.contrib import admin
from .models import Answer, Evaluation, Submission, Survey, Question

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Evaluation)
admin.site.register(Submission)
admin.site.register(Answer)