from django.db import models
from django.db.models.constraints import UniqueConstraint
from accounts.models import User, Student, Coordinator

# Create your models here.

class Alert(models.Model):

    class Meta:
        """Metadata options for the Alert model."""
        db_table = 'alert'

    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        blank=False,
        related_name='alerts')

    coordinator = models.ForeignKey(
        Coordinator, 
        on_delete=models.CASCADE, 
        blank=False,
        related_name='alerts')

    title = models.CharField(max_length=60)
    body = models.CharField(max_length=500, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField()

    def __str__(self):
        return 'Alert #{} by Student {}'.format(self.id, self.student.id_number)


class Message(models.Model):
    class Meta:
        """Metadata options for the Message model."""
        db_table = 'message'

    alert = models.ForeignKey(
        Alert,
        on_delete=models.CASCADE,
        blank=False,
        related_name='messages'
    )

    sender_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='messages_sent',
    )

    receiver_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='messages_received',
    )

    body = models.CharField(max_length=200)
    date_sent = models.DateTimeField(auto_now_add=True)


def user_directory_path(instance, filename):
    # The given file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class File(models.Model):
    
    class Meta:
        """Metadata options for the File model."""
        db_table = 'file'

    file_name = models.FileField(upload_to=user_directory_path)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        blank=False,
        related_name='files')

    # Choice definition for file type
    DELIVERABLES_DECLARATION = 'DD'
    ACTIVITY_SHEET = 'AS'
    STUDENT_SHEET = 'SS'

    FILE_TYPE_CHOICES = [
        (DELIVERABLES_DECLARATION, 'Declaration of Deliverables'),
        (ACTIVITY_SHEET, 'Weekly Activity sheet'),
        (STUDENT_SHEET, 'Excel sheet of all students')
    ]
    type = models.CharField(
        max_length=12, choices=FILE_TYPE_CHOICES, blank=False)

    def __str__(self):
        return 'File #{} of type {}'.format(self.id, self.type)


class Campus(models.Model):
    
    class Meta:
        """Metadata options for the Campus model."""
        db_table = 'campus'

    name = models.CharField(max_length=80, blank=False)
    city = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return 'Campus #{}: {}'.format(self.id, self.name)


class Offering(models.Model):
    
    class Meta:
        """Metadata options for the Offering model."""
        db_table = 'offering'
        # A given unique Offering (according to teaching period and year) can only have one Coordinator assigned to it
        UniqueConstraint(
            fields= ['unit_code', 'coordinator', 'campus', 'teaching_period', 'year'],
            name = 'unique_offering_coordinator'
        )

    unit_code = models.CharField(max_length=6, blank=False)
    
    coordinator = models.ForeignKey(
        Coordinator, blank=False, on_delete=models.CASCADE,
        related_name='offerings')
    
    campus = models.ForeignKey(
        Campus, on_delete=models.CASCADE, blank=False,
        related_name='offerings')

    teaching_period = models.CharField(max_length=3, blank=False)
    year = models.PositiveSmallIntegerField(blank=False)

    students = models.ManyToManyField(Student, related_name='offerings')



class Team(models.Model):
    class Meta:
        """Metadata options for the Team model."""
        db_table = 'team'

    team_number = models.CharField(max_length=10, blank=False)
    team_name = models.CharField(max_length=20)

    campus = models.ForeignKey(
        Campus, 
        on_delete=models.CASCADE, 
        null=True,
        related_name='teams')

    offering = models.ForeignKey(
        Offering, 
        on_delete=models.CASCADE, 
        null=True,
        related_name='teams')


class Report(models.Model):
    
    class Meta:
        """Metadata options for the Report model."""
        db_table = 'report'

    coordinator = models.ForeignKey(
        Coordinator, 
        on_delete=models.CASCADE, 
        blank=False,
        related_name='coordinator')

    date_generated = models.DateTimeField(auto_now_add=True)

