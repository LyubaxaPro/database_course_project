# Generated by Django 3.2.1 on 2021-06-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20210602_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupclassescustomersrecords',
            name='record_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='instructorshedule',
            name='i_shedule_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='instructorshedulecustomers',
            name='record_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='specialoffers',
            name='offer_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
