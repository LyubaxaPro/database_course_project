from .models import *
from django.db import transaction
from users.models import CustomUser
from .CRUD_repository import *

class CustomUserRepository(CRUDRepository):

    @classmethod
    def create(cls, client_user, user):
        user.save(using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return CustomUser.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return CustomUser.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return CustomUser.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        CustomUser.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        CustomUser.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        CustomUser.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        CustomUser.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        CustomUser.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return CustomUser.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class CustomersRepository(CRUDRepository):

    @classmethod
    @transaction.atomic
    def create(cls, client_user, customer):

        customer.user.role = CustomUser.CUSTOMER
        customer.user.save(
            using=cls.db_config_manager.get_connection(client_user))
        customer.save(using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return Customers.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return Customers.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return Customers.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        Customers.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        Customers.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        Customers.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        Customers.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        Customers.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return Customers.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class InstructorsRepository(CRUDRepository):

    @classmethod
    @transaction.atomic
    def create(cls, client_user, instructor):
        instructor.user.role = CustomUser.INSTRUCTOR
        instructor.user.save(
            using=cls.db_config_manager.get_connection(client_user))
        instructor.save(using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return Instructors.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return Instructors.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return Instructors.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        Instructors.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        Instructors.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        Instructors.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        Instructors.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        Instructors.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return Instructors.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class AdministratorsRepository(CRUDRepository):

    @classmethod
    @transaction.atomic
    def create(cls, client_user, admin):
        admin.user.role = CustomUser.ADMIN
        admin.user.save(
            using=cls.db_config_manager.get_connection(client_user))
        admin.save(using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return Administrators.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return Administrators.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return Administrators.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        Administrators.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        Administrators.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        Administrators.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        Administrators.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        Administrators.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return Administrators.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

