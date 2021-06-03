# Generated by Django 3.2.1 on 2021-06-02 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='customer_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='instructors',
            name='instructor_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]