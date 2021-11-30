# Generated by Django 3.2.9 on 2021-11-30 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20211119_1321'),
        ('dashboard', '0009_rename_alert_alert_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offering',
            name='students',
            field=models.ManyToManyField(related_name='offerings', to='accounts.Student'),
        ),
        migrations.AlterField(
            model_name='team',
            name='students',
            field=models.ManyToManyField(related_name='teams', to='accounts.Student'),
        ),
    ]