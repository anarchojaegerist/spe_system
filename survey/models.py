from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.constraints import UniqueConstraint
from accounts.models import Student, Coordinator
from dashboard.models import Offering

# Create your models here.

class Question(models.Model):
    
    class Meta:
        """Metadata options for the Question model."""
        db_table = 'question'

    
    prompt = models.CharField(max_length=300, blank=False)

    weighting = models.DecimalField(
        max_digits=4, decimal_places=2, default=0)

    # Choice definition for question type
    COMMENT = 'C'
    RATING = 'R'
    QUESTION_TYPE_CHOICES = [
        (COMMENT, 'Comment Question'),
        (RATING, 'Rating Question'),
    ]
    question_type = models.CharField(
        max_length=1, choices=QUESTION_TYPE_CHOICES, blank=False)
    
    # Choice definition for evaluation type
    SELF = 'S'
    PEER = 'P'
    EVALUATION_TYPE_CHOICES = [
        (SELF, 'Self Evaluation'),
        (PEER, 'Peer Evaluation'),
    ]
    evaluation_type = models.CharField(
        max_length=1, choices=EVALUATION_TYPE_CHOICES, blank=False)

    def __str__(self):
        return 'Question #{}: {}'.format(self.id, self.prompt)


class Survey(models.Model):
    
    class Meta:
        """Metadata options for the Survey model."""
        db_table = 'survey'


    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE, 
        blank=False, related_name='surveys')

    spe_number = models.PositiveSmallIntegerField(null=True)
    title = models.CharField(max_length=60)
    introductory_text = models.CharField(max_length=1600, null=True)
    date_opened = models.DateTimeField(null=True)
    date_closed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField(Question, related_name='surveys')
    offerings = models.ManyToManyField(Offering, related_name='surveys')


class Submission(models.Model):
    
    class Meta:
        """Metadata options for the Submission model."""
        db_table = 'submission'
    
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=False,
        related_name='submissions')

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, blank=False,
        related_name='submissions')

    spe_number = models.PositiveSmallIntegerField()
    date_submitted = models.DateTimeField(null=True)
    is_submitted = models.BooleanField(default=False)
    

class Evaluation(models.Model):
    
    class Meta:
        """Metadata options for the Evaluation model."""
        db_table = 'evaluation'

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=False,
        related_name='evaluations_by_student')

    evaluatee = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=False,
        related_name='evaluations_by_peers')

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, blank=False,
        related_name='evaluations')


class Rating(models.Model):

    class Meta:
        """Metadata options for the Rating model."""
        db_table = 'rating'

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=False,
        related_name='ratings')
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.CASCADE, blank=False,
        related_name='ratings')
    answer = models.PositiveSmallIntegerField()


class Comment(models.Model):

    class Meta:
        """Metadata options for the Comment model."""
        db_table = 'comment'


    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=False,
        related_name='comments')
    evaluation = models.ForeignKey(
        Evaluation, on_delete=models.CASCADE, blank=False,
        related_name='comments')
    answer = models.CharField(max_length=1200)
