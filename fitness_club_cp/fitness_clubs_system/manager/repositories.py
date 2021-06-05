from .models import *
from django.db import transaction
from abc import ABCMeta, abstractmethod
from .db_manager import DBConfigManager
from users.models import CustomUser

from users.models import FitnessClubs


class abstractclassmethod(classmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractclassmethod, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True

class CRUDRepository:

    __metaclass__ = ABCMeta
    db_config_manager = DBConfigManager()

    #Подключиться к базе данных с конкретной ролью
    @staticmethod
    def connect(user):
        return user

    #Создать и добавить в таблицу новый объект модели
    @classmethod
    @abstractmethod
    def create(cls, client_user, model):
        pass

    # Получить объект по первичному ключу
    @classmethod
    @abstractmethod
    def read_by_pk(cls, client_user, pk):
        pass

    #Получить объект по фильтру
    @classmethod
    @abstractmethod
    def read_filtered(cls, client_user, filter_dict):
        pass

    #Получить все объекты
    @classmethod
    @abstractmethod
    def read_all(cls, client_user):
        pass

    # Обновить по первичному ключу
    @classmethod
    @abstractmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        pass

    # Обновить по фильтру
    @classmethod
    @abstractmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        pass

    # Обновить все объекты
    @classmethod
    @abstractmethod
    def update_all(cls, client_user, update_dict):
        pass

    # Удалить по первичному ключу
    @classmethod
    @abstractmethod
    def delete_by_pk(cls, client_user, pk):
        pass

    # Удалить объекты подходящие под фильтр
    @classmethod
    @abstractmethod
    def delete_filtered(cls, client_user, filter_dict):
        pass

    @classmethod
    @abstractmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        pass

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


class AdminRecordsRepository(CRUDRepository):

    @classmethod
    def create(cls, client_user, admin_records):
        admin_records.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return AdminRecords.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return AdminRecords.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return AdminRecords.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        AdminRecords.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        AdminRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        AdminRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        AdminRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        AdminRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return AdminRecords.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class GroupClassesRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, group_classes):
        group_classes.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return GroupClasses.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return GroupClasses.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return GroupClasses.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        GroupClasses.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        GroupClasses.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        GroupClasses.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        GroupClasses.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        GroupClasses.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return GroupClasses.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class GroupClassesCustomersRecordsRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, group_classes_customer_rec):
        group_classes_customer_rec.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return GroupClassesCustomersRecords.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)


class GroupClassesSheduleRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, group_classes_shed):
        group_classes_shed.save(using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class InstructorSheduleRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, instructor_shed):
        instructor_shed.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return InstructorShedule.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return InstructorShedule.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return InstructorShedule.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        InstructorShedule.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        GroupClassesShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        InstructorShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        InstructorShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        InstructorShedule.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return InstructorShedule.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class InstructorSheduleCustomersRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, instructor_shed_customers):
        instructor_shed_customers.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return InstructorSheduleCustomers.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class PricesRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, price):
        price.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return Prices.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return Prices.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return Prices.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        Prices.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        Prices.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        Prices.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        Prices.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        Prices.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return Prices.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class ServicesRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, service):
        service.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return Services.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return Services.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return Services.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        Services.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        Services.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        Services.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        Services.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        Services.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return Services.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class FitnessClubsRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, fitness_club):
        fitness_club.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return FitnessClubs.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return FitnessClubs.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return FitnessClubs.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        FitnessClubs.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        FitnessClubs.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        FitnessClubs.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        FitnessClubs.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        FitnessClubs.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return FitnessClubs.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class SpecialOffersRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, special_offer):
        special_offer.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return SpecialOffers.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return SpecialOffers.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return SpecialOffers.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        FitnessClubs.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        SpecialOffers.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        SpecialOffers.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        SpecialOffers.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        SpecialOffers.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return SpecialOffers.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)
