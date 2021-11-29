# Generated by Django 3.2.9 on 2021-11-26 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_submission_survey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='introductory_text',
            field=models.CharField(max_length=1600, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='spe_number',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
