# Generated by Django 3.2.1 on 2021-06-03 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_alter_groupclassesshedule_shedule_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prices',
            name='tariff_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]