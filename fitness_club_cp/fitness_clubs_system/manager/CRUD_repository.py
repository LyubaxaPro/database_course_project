from abc import ABCMeta, abstractmethod
from .db_manager import DBConfigManager

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
