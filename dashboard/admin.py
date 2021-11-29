from django.contrib import admin
from .models import Alert, Campus, File, Offering, Report, Team

# Register your models here.

admin.site.register(Alert)
admin.site.register(File)
admin.site.register(Campus)
admin.site.register(Offering)
admin.site.register(Team)
admin.site.register(Report)

