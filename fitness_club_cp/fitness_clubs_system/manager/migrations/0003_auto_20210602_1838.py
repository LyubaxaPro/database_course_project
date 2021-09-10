# Generated by Django 3.2.1 on 2021-06-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20210602_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='customer_id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='instructors',
            name='instructor_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
