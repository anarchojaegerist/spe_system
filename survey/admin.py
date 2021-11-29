from django.contrib import admin
from .models import Comment, Evaluation, Rating
from .models import Submission, Survey, Question

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Evaluation)
admin.site.register(Submission)
admin.site.register(Rating)
admin.site.register(Comment)