# Generated by Django 3.2.9 on 2021-11-28 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_team_offering'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='students',
        ),
    ]