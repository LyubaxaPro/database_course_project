# Generated by Django 3.2.1 on 2021-06-06 21:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_auto_20210606_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminlogs',
            name='description',
        ),
        migrations.AddField(
            model_name='adminlogs',
            name='record_id',
            field=models.IntegerField(default=None),
        ),

        migrations.AlterField(
            model_name='adminlogs',
            name='act_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 21, 49, 22, 880861)),
        ),
        migrations.AlterField(
            model_name='adminrecords',
            name='creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 6, 21, 49, 22, 878797)),
        ),
    ]
