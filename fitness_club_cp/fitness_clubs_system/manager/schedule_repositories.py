from .models import *
from .CRUD_repository import *

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


