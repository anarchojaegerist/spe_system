from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, date, time
from decimal import Decimal, getcontext

from accounts.models import Coordinator, User, Student
from dashboard.models import Campus, Report, Team, File, Offering
from survey.models import Question, Rating, Survey, Submission, Evaluation
from .forms import CsvForm
import csv

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


@login_required
def campus_view(request):

    # Retrieve all campuses to display on page
    campuses = Campus.objects.all()
    return render(request, 'campus_view.html', {'campuses': campuses})


@login_required
def team_view(request, pk):

    # Lists to store SPE submissions
    spe1 = []
    spe2 = []

    c = Campus.objects.get(id = pk)
    # Retrieve all teams that belong to the given campus
    teams = Team.objects.all().filter(campus = c)

    # Retrieve SPE submissions for students in each team
    for t in teams:
        for s in t.students.all():
            # Check if student has submitted SPE1 
            try:
                spe1.append(
                    Submission.objects.get(spe_number = 1,
                    student = s)
                )
                print('SPE added')
            except ObjectDoesNotExist:
                pass

            # Check if student has submitted SPE2 
            try:
                spe2.append(
                    Submission.objects.get(spe_number = 2,
                    student = s)
                )
            except ObjectDoesNotExist:
                pass
    
    context = {
        'teams': teams,
        'spe1': spe1,
        'spe2': spe2,
    }

    return render(request, 'team_view.html', context)


@login_required
def student_view(request, pk):

    # List of dictionaries containing: 1) Student object 2) SPE Submissions, if any
    student_data = []
    spe_closed = False # Boolean representing whether at least one SPE has been closed (usually the first one)

    t = Team.objects.get(id = pk)
    
    for s in t.students.all():
        # Student dictionary containing student details and SPE submissions
        add_student = {
            'student': s,
            'user': User.objects.get(id = s.user_id)}
        
        # Check if student has submitted SPE 1
        if Submission.objects.all().filter(spe_number = 1, student_id = s.id).exists():
                add_student['spe_1'] = True
                # Check if SPE 1 has closed

                submission = Submission.objects.get(
                    spe_number = 1,
                    student_id = s.id
                )

                survey = Survey.objects.get(id = submission.survey_id)

                if survey.date_closed is not None and survey.date_closed < timezone.make_aware(datetime.utcnow()):
                    spe_closed = True

        else:
            add_student['spe_1'] = False

        # Check if student has submitted SPE 2
        if Submission.objects.all().filter(
            spe_number = 2,
            student_id = s.id
        ).exists():
            add_student['spe_2'] = True
        else:
            add_student['spe_2'] = False

        student_data.append(add_student)

        context = {
            'student_data': student_data,
            'spe_closed': spe_closed,
            'team': t
        }

    return render(request, 'student_view.html', context)

def report_directory_path(request, pk):
    # The given report csv will be stored at MEDIA_ROOT/user_<id>/<filename>
    coordinator = Coordinator.objects.get(user_id = request.user.id)
    count = Report.objects.filter(coordinator_id = coordinator.id).count()
    return 'user_{0}/Report{1}'.format(request.user.id, count+1)

def create_team_report(request, pk):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="{}.csv"'.format(report_directory_path(request, pk))},
    )

    t = Team.objects.get(id = pk)

    writer = csv.writer(response)
    writer.writerow(['Person ID', 'Surname', 'Title', 'Given Names', 
    'Teach Period', 'Unit Code', 'Team ID', 'Team Name', 'SPE1', 'SPE2'])
    for s in t.students.all():
        getcontext().prec = 2
        spe1 = 0
        spe2 = 0
        spe_sum = 0
        rating_count = 0
        evaluation_count = 0

        u = User.objects.get(id = s.user_id)
        # Check if Student has submitted SPE1
        if Submission.objects.filter(student_id=s.id, spe_number=1).exists():
            # If student has submitted SPE1, loop through evaluations of student (including self-evaluation) to calculate SPE1 mark
            evaluations = Evaluation.objects.filter(evaluatee_id=s.id)
            for e in evaluations:
                evaluation_count += 1
                ratings = Rating.objects.filter(evaluation_id = e.id)
                for r in ratings:
                    q = Question.objects.get(id = r.question_id)
                    weighting = q.weighting

                    rating_count += 1
                    spe_sum += float(r.answer * weighting)
                    print(f"SPE SUM {spe_sum} ANSWER {r.answer * weighting}")
            
            spe1 = ((spe_sum) / (rating_count))
            # print(f"SPE Sum: {spe_sum} Rating count: {rating_count}")
            print(spe1)
        else:
            spe1 = 0
        
        spe_sum = 0
        rating_count = 0

        # Check if Student has submitted SPE2
        if Submission.objects.filter(student_id=s.id, spe_number=2).exists():
            # If student has submitted SPE2, loop through evaluations of student (including self-evaluation) to calculate SPE2 mark
            evaluations = Evaluation.objects.filter(evaluatee_id=s.id)
            for e in evaluations:
                ratings = Rating.objects.filter(evaluation_id = e.id)
                for r in ratings:
                    q = Question.objects.get(id = r.question_id)
                    weighting = q.weighting
                    rating_count += 1
                    spe_sum += Decimal(r.answer) * Decimal(weighting)
            spe2 = Decimal(spe_sum) / Decimal(rating_count)
        else:
            spe2 = 0

        writer.writerow([s.id_number, u.last_name, u.title, u.given_names, 
        t.offering.teaching_period, t.offering.unit_code, 
        t.team_number, t.team_name, spe1, spe2])

    report_csv = Report.objects.create(
        coordinator_id = Coordinator.objects.get(user_id = request.user.id).id
        )

    return response

class AllStudentsListView(ListView):
    def get(request):
        print()

@login_required
def student_list(request):

    teaching = [] # List of offerings the coordinator is assigned to

    # List of dictionaries - each dictionary contains data for a given
    # student from both the Student and User models.
    student_data = [{}] 

    # Get coordinator ID using current user's ID
    coordinator_object = Coordinator.objects.get(user_id = request.user.id)

    # Check if coordinator has students. If so, retrieve those student objects from database
    teaching = Offering.objects.all().filter(coordinator = coordinator_object)

    if teaching:
        for t in teaching:
            # Each offering is tied to multiple students. Therefore, loop over the students an offering has, and add to dictionary
            for s in t.students.all():
                student_user = User.objects.get(id = s.user_id)
                student_data.append(
                    {
                        'id_number': s.id_number,
                        'title': student_user.title,
                        'given_names': student_user.given_names,
                        'last_name': student_user.last_name,
                        'email': student_user.email
                    }
                )

    form = CsvForm(request.POST, request.FILES)
    form.instance.user = request.user
    if form.is_valid():
        obj = File(
            user = request.user,
            file_name = request.FILES['file_name'],
        )
        obj.save()
        form = CsvForm()
        

        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f, delimiter=',')

            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    
                    # Get data from each column
                    csv_id_number = row[0]
                    csv_last_name = row[1]
                    csv_title = row[2]
                    csv_given_names = row[3]
                    csv_teaching_period = row[4]
                    csv_unit_code = row[5]
                    csv_team_number = row[6]
                    csv_team_name = row[7]

                    # Create User object
                    u, create = User.objects.get_or_create(
                            # Concatenate student ID with Murdoch's current student email scheme
                            email = f"{csv_id_number}@student.murdoch.edu.au",
                            last_name = csv_last_name,
                            title = csv_title,
                            given_names = csv_given_names,
                    )

                    # Create Student object
                    s, create = Student.objects.get_or_create(
                        user = u,
                        id_number = csv_id_number,
                    )

                    # Create Campus and Offering units before Team object, as they are required as FKs
                    # Split teaching period and year from column 4 of the csv, which has combined the two

                    split_teaching_period = csv_teaching_period.split()
                    tp = split_teaching_period[0] # E.g. TSD, TSA, S1
                    y = split_teaching_period[1] # E.g. 2021

                    # Get University campus from teaching period
                    tp_name = ''
                    tp_city = ''
                    tp_country = ''

                    if tp == "TJA" or tp == "TMA" or tp == "TSA":
                        tp_name = 'Murdoch University International Study Centre Singapore'
                        tp_city = 'Singapore'
                        tp_country = 'Singapore'
                    elif tp == "TJD" or tp == "TMD" or tp == "TSD":
                        tp_name = 'Murdoch University Dubai'
                        tp_city = 'Dubai'
                        tp_country = 'United Arab Emirates'
                    elif tp == "S1" or tp == "S2":
                        tp_name = 'Murdoch University'
                        tp_city = 'Perth'
                        tp_country = 'Australia'

                    c, create = Campus.objects.get_or_create(
                        name = tp_name,
                        city = tp_city,
                        country = tp_country,
                    )

                    # Assumes an Offering with the given combination of attributes has already been entered into the database
                    o, create = Offering.objects.get_or_create(
                        unit_code = csv_unit_code,
                        coordinator = coordinator_object,
                        teaching_period = tp,
                        year = y,
                        campus = c,
                    )
                    o.students.add(s)

                    # Add student object to (already created) Team's list of students
                    t, create = Team.objects.get_or_create(
                        team_number = csv_team_number,
                        team_name = csv_team_name,
                        campus = c,
                        offering = o,)
                    t.students.add(s)

            obj.save()
    
    return render(request, 'student_list.html', {'form': form, 'student_data': student_data})



