# Generated by Django 3.2.1 on 2021-06-01 15:40

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20210525_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructorshedule',
            name='i_shedule_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
