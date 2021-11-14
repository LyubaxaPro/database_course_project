from .models import *
from .CRUD_repository import *
from users.models import FitnessClubs

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