# Generated by Django 3.2.1 on 2021-05-24 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_fitnessclubs_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='club',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)'), (2, 'Москва, ул. Архитектора Власова, 22'), (3, 'Москва, Каширское шоссе, 61Г'), (4, 'Москва, ул. Климашкина, 17с2'), (5, 'Санкт-Петербург, Пулковское ш., 35, ТРК Масштаб'), (6, 'Санкт-Петербург, пл. Карла Фаберже, 8, литера Е'), (7, 'Санкт-Петербург, ул. Коллонтай, 31, литера А, корп.1'), (8, 'Казань, ул. Ю. Фучика, д. 90')], default=1, verbose_name='Фитнес клуб'),
        ),
    ]