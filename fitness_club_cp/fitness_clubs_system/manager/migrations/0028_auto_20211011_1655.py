# Generated by Django 3.2.1 on 2021-10-11 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0027_auto_20211009_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admingroupclasseslogs',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 11, 16, 55, 19, 785527)),
        ),
        migrations.AlterField(
            model_name='adminrecords',
            name='creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 11, 16, 55, 19, 783004)),
        ),
        migrations.AlterField(
            model_name='instructorpersonaltrainingslogs',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 11, 16, 55, 19, 785178)),
        ),
        migrations.AlterModelTable(
            name='instructors',
            table=None,
        ),
    ]
