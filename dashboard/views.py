from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from accounts.models import Coordinator, User, Student
from dashboard.models import Campus, Team, File, Offering
from .forms import CsvForm
import csv

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


@login_required
def student_list(request):

    teaching = [] # List of offerings the coordinator is assigned to
    student_data = [{}] # List of students (each student is a dictionary) being taught by a coordinator

    # Get coordinator ID from current user's ID
    coordinator_object = Coordinator.objects.get(user_id = request.user.id)

    # Check if coordinator has students. If so, fetch from database
    teaching = Offering.objects.all().filter(coordinator = coordinator_object)

    for t in teaching:
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
                    # Create User object
                    u, create = User.objects.get_or_create(
                            # Concatenate student ID with Murdoch's current student email scheme
                            email = f"{row[0]}@student.murdoch.edu.au",
                            last_name = row[1],
                            title = row[2],
                            given_names = row[3],
                    )

                    # Create Student object
                    s, create = Student.objects.get_or_create(
                        user = u,
                        id_number = row[0],
                    )

                    # Add student object to (already created) Team's list of students
                    t, create = Team.objects.get_or_create(team_number = row[6])
                    t.students.add(s)

                    # Split teaching period and year from column 4 of the csv
                    offered = row[4].split()
                    tp = offered[0]
                    y = offered[1]

                    # Get University campus from teaching period
                    tp_name = ''
                    tp_city = ''
                    tp_country = ''

                    print(tp)
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
                        country = tp_country
                    )

                    # Assumes an Offering with the given combination of attributes has already been entered into the database
                    o, create = Offering.objects.get_or_create(
                        unit_code = row[5],
                        coordinator = coordinator_object,
                        teaching_period = tp,
                        year = y,
                        campus = c
                    )
                    o.students.add(s)
            
            obj.save()


    return render(request, 'student_list.html', {'form': form, 'student_data': student_data})



