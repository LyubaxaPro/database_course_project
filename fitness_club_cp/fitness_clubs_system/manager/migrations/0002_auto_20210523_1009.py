# Generated by Django 3.2.1 on 2021-05-23 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_fitnessclubs_address'),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupclassesshedule',
            name='club',
            field=models.ForeignKey(blank=True, db_column='club_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.fitnessclubs'),
        ),
        migrations.AlterField(
            model_name='groupclassesshedule',
            name='instructor',
            field=models.ForeignKey(blank=True, db_column='instructor_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='manager.instructors'),
        ),
    ]
