# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminRecords(models.Model):
    update_instructor = models.TextField(blank=True, null=True)  # This field type is a guess.
    add_instructor = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'admin_records'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Customers(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING, blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    patronymic = models.TextField(blank=True, null=True)
    day_of_birth = models.DateField(blank=True, null=True)
    measure = models.JSONField(blank=True, null=True)
    tariff = models.ForeignKey('Prices', models.DO_NOTHING, blank=True, null=True)
    tariff_end_date = models.DateField(blank=True, null=True)
    instructor = models.ForeignKey('Instructors', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FitnessClubs(models.Model):
    club_id = models.IntegerField(primary_key=True)
    address = models.TextField(unique=True, blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    phone = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fitness_clubs'


class GroupClasses(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_classes'


class GroupClassesCustomersRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    shedule = models.ForeignKey('GroupClassesShedule', models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    class_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_classes_customers_records'


class GroupClassesShedule(models.Model):
    shedule_id = models.IntegerField(primary_key=True)
    class_field = models.ForeignKey(GroupClasses, models.DO_NOTHING, db_column='class_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    club = models.ForeignKey(FitnessClubs, models.DO_NOTHING, blank=True, null=True)
    instructor = models.ForeignKey('Instructors', models.DO_NOTHING, blank=True, null=True)
    class_time = models.TimeField(blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)
    maximum_quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_classes_shedule'


class InstructorShedule(models.Model):
    i_shedule_id = models.IntegerField(primary_key=True)
    instructor = models.ForeignKey('Instructors', models.DO_NOTHING, blank=True, null=True)
    training_time = models.TimeField(blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor_shedule'


class InstructorSheduleCustomers(models.Model):
    record_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    i_shedule = models.ForeignKey(InstructorShedule, models.DO_NOTHING, blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor_shedule_customers'


class Instructors(models.Model):
    instructor_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING, blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    surname = models.TextField(blank=True, null=True)
    patronymic = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)  # This field type is a guess.
    experience = models.IntegerField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)  # This field type is a guess.
    specialization = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'instructors'


class Prices(models.Model):
    tariff_id = models.IntegerField(primary_key=True)
    tariff_name = models.TextField(unique=True, blank=True, null=True)
    tariff_description = models.TextField(unique=True, blank=True, null=True)
    price_one_month = models.IntegerField(blank=True, null=True)
    price_three_month = models.IntegerField(blank=True, null=True)
    price_six_month = models.IntegerField(blank=True, null=True)
    price_one_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prices'


class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.TextField(unique=True, blank=True, null=True)
    service_description = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class SpecialOffers(models.Model):
    offer_id = models.IntegerField(primary_key=True)
    offer_name = models.TextField(blank=True, null=True)
    offer_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'special_offers'


class UsersCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=254)
    login = models.CharField(unique=True, max_length=40)
    role = models.SmallIntegerField()
    club = models.SmallIntegerField()
    phone = models.CharField(max_length=40)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    is_superuser = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users_customuser'


class UsersCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UsersCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)
