# Generated by Django 3.2.9 on 2021-11-18 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20211118_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='date_closed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='date_opened',
            field=models.DateTimeField(null=True),
        ),
    ]