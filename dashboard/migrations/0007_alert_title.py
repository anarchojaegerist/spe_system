# Generated by Django 3.2.9 on 2021-11-29 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20211129_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='title',
            field=models.CharField(max_length=60),
            preserve_default=False,
        ),
    ]
