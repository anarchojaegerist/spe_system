import csv, io
from django.core.management import BaseCommand
from django.db.models.fields import AutoField
from django.utils import timezone
from user.models import User, Student
from dashboard.models import Offering, Team, Student_Team

class Command(BaseCommand):
    help = "Loads students from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]
        with io.open(file_path, "r", encoding = "utf-8") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            next(data)
            for row in data:
                student = Student.objects.create(
                    id_number = row[0],
                )
                user = User.objects.create(
                    
                    last_name = row[1],
                    title = row[2],
                    given_names = row[3],
                    email = row[0] + "@student.murdoch.edu.au",
                )
                offering = Offering.objects.get_or_create(
                    teaching_period = row[4],
                    unit_code = row[5],
                )
                team = Team.objects.get_or_create(
                    team_name = row[6],
                )
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )