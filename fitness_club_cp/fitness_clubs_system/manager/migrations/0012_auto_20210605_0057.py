# Generated by Django 3.2.1 on 2021-06-05 00:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_auto_20210604_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminrecords',
            name='is_new',
        ),

    ]