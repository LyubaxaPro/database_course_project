# Generated by Django 3.2.1 on 2021-06-09 15:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0024_auto_20210609_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructors',
            name='new_photo',
        ),
        migrations.AlterField(
            model_name='admingroupclasseslogs',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 9, 15, 44, 13, 105709)),
        ),
        migrations.AlterField(
            model_name='adminrecords',
            name='creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 9, 15, 44, 13, 103344)),
        ),
        migrations.AlterField(
            model_name='instructorpersonaltrainingslogs',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 9, 15, 44, 13, 105382)),
        ),
    ]