from .models import *
from .CRUD_repository import *

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

class InstructorPersonalTrainingsLogsRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, instructor_log):
        instructor_log.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return InstructorPersonalTrainingsLogs.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)

class AdminGroupClassesLogsRepository(CRUDRepository):
    @classmethod
    def create(cls, client_user, admin_log):
        admin_log.save(
            using=cls.db_config_manager.get_connection(client_user))

    @classmethod
    def read_by_pk(cls, client_user, pk):
        return AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(client_user)).get(pk=pk)

    @classmethod
    def read_filtered(cls, client_user, filter_dict):
        return AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(client_user)).filter(**filter_dict)

    @classmethod
    def read_all(cls, client_user):
        return AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(client_user)).all()

    @classmethod
    def update_by_pk(cls, client_user, pk, update_dict):
        AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(client_user)).filter(
            pk=pk).update(**update_dict)

    @classmethod
    def update_filtered(cls, client_user, filter_dict, update_dict):
        AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).update(**update_dict)

    @classmethod
    def update_all(cls, client_user, update_dict):
        AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).all().update(**update_dict)

    @classmethod
    def delete_by_pk(cls, client_user, pk):
        AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).get(pk=pk).delete()

    @classmethod
    def delete_filtered(cls, client_user, filter_dict):
        AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(
            client_user)).filter(**filter_dict).delete()

    @classmethod
    def read_join_filtered(cls, client_user, join_field, filter_dict):
        return AdminGroupClassesLogs.objects.using(cls.db_config_manager.get_connection(client_user)).\
            select_related(join_field).filter(**filter_dict)
