import datetime

from django.db import models

from users.models import CustomUser, FitnessClubs

from django.contrib.postgres.fields import ArrayField
import json


class Administrators(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    patronym = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'administrators'

class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    sex = models.TextField(blank=True, null=True)
    name = models.CharField(verbose_name='Имя', max_length=50)
    surname = models.CharField(verbose_name='Фамилия', max_length=50)
    patronymic = models.CharField(verbose_name='Отчество', max_length=50)
    day_of_birth = models.DateField(verbose_name='Дата рождения')
    height = models.IntegerField(default=0, verbose_name='Рост')
    measured_weights = ArrayField(models.IntegerField(blank=True, null=True, default=0), default=list())
    measure_dates = ArrayField(models.DateField(blank=True, null=True, default=datetime.date.today), default=list())
    tariff = models.ForeignKey('Prices', on_delete=models.CASCADE, verbose_name='тариф')
    tariff_end_date = models.DateField(verbose_name='Дата окончания срока действия абонемента')
    instructor = models.ForeignKey('Instructors', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.customer_id)

    class Meta:
        db_table = 'customers'

class GroupClasses(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'group_classes'

class GroupClassesCustomersRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    shedule = models.ForeignKey('GroupClassesShedule', on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, blank=True, null=True)
    class_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.record_id)

    class Meta:
        db_table = 'group_classes_customers_records'

class Instructors(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    sex = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    education = ArrayField(models.TextField(blank=True, null=True), verbose_name='Образование')  # This field type is a guess.
    experience = models.IntegerField( verbose_name='Стаж')
    achievements = ArrayField(models.TextField(blank=True, null=True),  verbose_name='Достижения')  # This field type is a guess.
    specialization = ArrayField(models.TextField(blank=True, null=True),  verbose_name='Специализация')  # This field type is a guess.
    photo = models.ImageField(upload_to='images/', null=True, default='images/default.jpg',  verbose_name='Фото')
    is_active = models.BooleanField(default=False)
    admin = models.ForeignKey(Administrators, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.instructor_id)

    class Meta:
        db_table = 'instructors'

class GroupClassesShedule(models.Model):
    shedule_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey(GroupClasses, on_delete=models.CASCADE, db_column='class_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    club = models.ForeignKey(FitnessClubs, on_delete=models.CASCADE, db_column='club_id', blank=True, null=True)
    instructor = models.ForeignKey(Instructors, on_delete=models.CASCADE, db_column='instructor_id', blank=True, null=True)
    class_time = models.TimeField(blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)
    maximum_quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.shedule_id)

    class Meta:
        db_table = 'group_classes_shedule'

class AdminRecords(models.Model):

    PENDING = 0  # изменения ожидают обработки
    ACCEPTED = 1  # изменения разрешены
    DECLINED = 2  # изменения отклонены

    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (ACCEPTED, 'active'),
        (DECLINED, 'cancelled')
    )

    creation_datetime = models.DateTimeField(default=datetime.datetime.now())
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=PENDING)
    instructor = models.ForeignKey(Instructors,  blank=True, null=True,  on_delete=models.CASCADE)
    admin = models.ForeignKey(Administrators,  blank=True, null=True,  on_delete=models.CASCADE)
    change = models.JSONField( blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'admin_records'


class InstructorShedule(models.Model):
    i_shedule_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey('Instructors', on_delete=models.CASCADE, blank=True, null=True)
    training_time = models.TimeField(blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.i_shedule_id)


    class Meta:
        db_table = 'instructor_shedule'


class InstructorSheduleCustomers(models.Model):
    record_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, blank=True, null=True)
    i_shedule = models.ForeignKey(InstructorShedule, on_delete=models.CASCADE, blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.record_id)

    class Meta:
        db_table = 'instructor_shedule_customers'

class Prices(models.Model):
    tariff_id = models.AutoField(primary_key=True)
    tariff_name = models.TextField(unique=True, blank=True, null=True)
    tariff_description = models.TextField(unique=True, blank=True, null=True)
    price_one_month = models.IntegerField(blank=True, null=True)
    price_three_month = models.IntegerField(blank=True, null=True)
    price_six_month = models.IntegerField(blank=True, null=True)
    price_one_year = models.IntegerField(blank=True, null=True)
    is_time_restricted = models.BooleanField(blank=True, null=True)
    min_time = models.TimeField(blank=True, null=True)
    max_time = models.TimeField(blank=True, null=True)
    days_of_week = ArrayField(models.TextField(blank=True, null=True, default=""), default=[])

    def __str__(self):
        return str(self.tariff_id)

    class Meta:
        db_table = 'prices'

class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.TextField(unique=True, blank=True, null=True)
    service_description = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'services'


class SpecialOffers(models.Model):
    offer_id = models.AutoField(primary_key=True)
    offer_name = models.TextField(blank=True, null=True)
    offer_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'special_offers'

class InstructorPersonalTrainingsLogs(models.Model):

    act_date = models.DateTimeField(default=datetime.datetime.now())
    instructor = models.ForeignKey(Instructors, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(default='')

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'instructor_personal_trainings_logs'

class AdminGroupClassesLogs(models.Model):

    act_date = models.DateTimeField(default=datetime.datetime.now())
    club = models.IntegerField(blank=True, null=True)
    group_class = models.ForeignKey(GroupClasses, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(default='')

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'admin_group_classes_logs'
