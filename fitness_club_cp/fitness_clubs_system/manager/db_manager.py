from django.contrib.auth.models import AnonymousUser
from django.http import request
from users.models import CustomUser
from fitness_clubs_system.settings import DATABASES
import sys

# singleton decorator for DBConfig Manager
def singleton(cls):
    all_instances = {}

    def get_instance():
        if cls not in all_instances:
            all_instances[cls] = cls()
        return all_instances[cls]

    return get_instance


@singleton
class DBConfigManager():
    connections = None

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, *args, **kwargs):
        self.connections = list(filter(lambda x: x, DATABASES))

    def get_connection(self, user=None):
        ROLE_CHOICES = (
            (0, 'customer_role_connect'),
            (1, 'instructor_role_connect'),
            (2, 'admin_role_connect'),
            (3, 'superuser_role_connect')
        )

        if 'test' in sys.argv:
            return list(filter(lambda x: 'default' in x.lower(), self.connections))[0]

        if user.is_anonymous or user is None:
            return list(filter(lambda x: 'guest' in x.lower(), self.connections))[0]
        elif user.role is None or user.role == CustomUser.GUEST:
            return list(filter(lambda x: 'guest' in x.lower(), self.connections))[0]
        return list(filter(lambda x: ROLE_CHOICES[user.role][1].lower() in x.lower(), self.connections))[0]
