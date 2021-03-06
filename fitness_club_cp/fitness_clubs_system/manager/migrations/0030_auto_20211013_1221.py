# Generated by Django 3.2.1 on 2021-10-13 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0029_auto_20211013_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admingroupclasseslogs',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 12, 21, 28, 826290)),
        ),
        migrations.AlterField(
            model_name='adminrecords',
            name='creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 12, 21, 28, 823863)),
        ),
        migrations.AlterField(
            model_name='instructorpersonaltrainingslogs',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 12, 21, 28, 825809)),
        ),
        migrations.AlterField(
            model_name='instructors',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
