from django.db import models

from users.models import CustomUser, FitnessClubs

from django.contrib.postgres.fields import ArrayField

class AdminRecords(models.Model):
    update_instructor = models.TextField(blank=True, null=True)  # This field type is a guess.
    add_instructor = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'admin_records'

class Customers(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    sex = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    patronymic = models.TextField(blank=True, null=True)
    day_of_birth = models.DateField(blank=True, null=True)
    measure = models.JSONField(blank=True, null=True)
    tariff = models.ForeignKey('Prices', models.DO_NOTHING, blank=True, null=True)
    tariff_end_date = models.DateField(blank=True, null=True)
    instructor = models.ForeignKey('Instructors', models.DO_NOTHING, blank=True, null=True)

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
    shedule = models.ForeignKey('GroupClassesShedule', models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    class_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'group_classes_customers_records'

class Instructors(models.Model):
    instructor_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    sex = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    patronymic = models.TextField(blank=True, null=True)
    education = ArrayField(models.TextField(blank=True, null=True))  # This field type is a guess.
    experience = models.IntegerField(blank=True, null=True)
    achievements = ArrayField(models.TextField(blank=True, null=True))  # This field type is a guess.
    specialization = ArrayField(models.TextField(blank=True, null=True))  # This field type is a guess.
    photo = models.ImageField(upload_to='images/', null=True,  default= 'main/img/trener.jpg')

    def __str__(self):
        return str(self.instructor_id)

    class Meta:
        db_table = 'instructors'

class GroupClassesShedule(models.Model):
    shedule_id = models.IntegerField(primary_key=True)
    class_field = models.ForeignKey(GroupClasses, models.DO_NOTHING, db_column='class_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    club = models.ForeignKey(FitnessClubs, models.DO_NOTHING, db_column='club_id', blank=True, null=True)
    instructor = models.ForeignKey(Instructors, models.DO_NOTHING, db_column='instructor_id', blank=True, null=True)
    class_time = models.TimeField(blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)
    maximum_quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'group_classes_shedule'


class InstructorShedule(models.Model):
    i_shedule_id = models.IntegerField(primary_key=True)
    instructor = models.ForeignKey('Instructors', models.DO_NOTHING, blank=True, null=True)
    training_time = models.TimeField(blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'instructor_shedule'


class InstructorSheduleCustomers(models.Model):
    record_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    i_shedule = models.ForeignKey(InstructorShedule, models.DO_NOTHING, blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'instructor_shedule_customers'




class Prices(models.Model):
    tariff_id = models.IntegerField(primary_key=True)
    tariff_name = models.TextField(unique=True, blank=True, null=True)
    tariff_description = models.TextField(unique=True, blank=True, null=True)
    price_one_month = models.IntegerField(blank=True, null=True)
    price_three_month = models.IntegerField(blank=True, null=True)
    price_six_month = models.IntegerField(blank=True, null=True)
    price_one_year = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'prices'


class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.TextField(unique=True, blank=True, null=True)
    service_description = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'services'


class SpecialOffers(models.Model):
    offer_id = models.IntegerField(primary_key=True)
    offer_name = models.TextField(blank=True, null=True)
    offer_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'special_offers'


