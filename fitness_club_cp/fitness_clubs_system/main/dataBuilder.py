from users.models import CustomUser
from manager.services import CustomUserService
from manager.models import Customers, Prices, Instructors, Administrators
import random

class UserBuilder:
    def __init__(self):
        self.customuser = CustomUser(
            pk=1,
            email="l1234@mail.ru",
            password="secure_password",
            role=3,
            club=1,
            login="LyubaxaPro"
        )
        self.user = None
        self.get_user()

    def get_user(self):
        raise NotImplementedError

class SuperUser(UserBuilder):
    def get_user(self):
        user = CustomUserService.read_filtered(self.customuser, {'role' : 3})
        if len(user) > 0:
            self.user = user[0]

class CustomerUser(UserBuilder):
    def get_user(self):
        user = CustomUserService.read_filtered(self.customuser, {'role' : 0})
        if len(user) > 0:
            self.user = user[0]

class AdminUser(UserBuilder):
    def get_user(self):
        user = CustomUserService.read_filtered(self.customuser, {'role' : 2})
        if len(user) > 0:
            self.user = user[0]

class InstructorUser(UserBuilder):
    def get_user(self):
        user = CustomUserService.read_filtered(self.customuser, {'role' : 1})
        if len(user) > 0:
            self.user = user[0]

class UserBuilderByPk:
    def __init__(self, pk):
        self.customuser = CustomUser(
            pk=1,
            email="l1234@mail.ru",
            password="secure_password",
            role=3,
            club=1,
            login="LyubaxaPro"
        )
        self.user = None
        self.pk = pk
        self.get_user()

    def get_user(self):
        raise NotImplementedError

class UserByPk(UserBuilderByPk):

    def get_user(self):
        self.user = CustomUserService.read_by_pk(self.customuser, self.pk)

class PricesBuilder:
    def build(self):
        tarif = Prices(
            tariff_name="Day",
            tariff_description="Description",
            price_one_month=10000,
            price_three_month=30000,
            price_six_month=60000,
            price_one_year=90000,
            is_time_restricted=False,
            min_time=None,
            max_time=None,
            days_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        )
        return tarif

class UserWithInfoBuilder:
    def build(self, pk, email, login, role):
        customuser = CustomUser(
            pk=pk,
            email=email,
            password="password",
            role=role,
            club=0,
            login=login
        )
        return customuser


class CustomerBuilder:
    def build(self, user, tarif, instructor):

        customer = Customers(
            user=user,
            sex='man',
            name='Егор',
            surname='Давлетов',
            patronymic='Сергеевич',
            day_of_birth='1990-08-12',
            height=190,
            measured_weights=[],
            measure_dates=[],
            tariff=tarif,
            tariff_end_date='2023-08-12',
            instructor=instructor
        )
        return customer

class InstructorBuilder:
    def build(self, user, admin):

        instructor = Instructors(
            user=user,
            sex="woman",
            name="Елизавета",
            surname="Потапова",
            patronymic="Николаевна",
            education=["МГТУ"],
            experience=20,
            achievements=['Список', 'Достижений'],
            specialization=['Плавание'],
            photo=None,
            is_active=True,
            admin=admin
        )
        return instructor

class AdminBuilder:
    def build(self, user):
        admin = Administrators(
        user=user,
        name="Анна",
        surname="Голубева",
        patronym="Сергеевна"
        )

        return admin

def get_data_for_user_mock(pk, email, login, role):
    return CustomUser(
            pk=pk,
            email=email,
            password="password",
            role=role,
            club=0,
            login=login
        )

def get_data_for_prices_mock():
    return Prices(
            tariff_name="Day",
            tariff_description="Description",
            price_one_month=10000,
            price_three_month=30000,
            price_six_month=60000,
            price_one_year=90000,
            is_time_restricted=False,
            min_time=None,
            max_time=None,
            days_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        )