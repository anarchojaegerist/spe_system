# Generated by Django 3.2.9 on 2021-11-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20211127_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='date_submitted',
            field=models.DateTimeField(null=True),
        ),
    ]
