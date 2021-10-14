from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository,\
    AdministratorsRepository, AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, AdminGroupClassesLogsRepository
from manager.models import Instructors, GroupClassesCustomersRecords, InstructorSheduleCustomers, InstructorShedule,\
    GroupClassesShedule, SpecialOffers, AdminRecords, Prices, Customers, Instructors, Administrators
from django.test import TestCase
from users.models import CustomUser, FitnessClubs
import unittest.mock as mock
from main.view_funcs.simple_data import *
from itertools import chain

offers_list = [SpecialOffers(pk=1, offer_name='nklkml', offer_description='jnknjk'), \
               SpecialOffers(pk=2, offer_name='aaaa', offer_description='bbbb')]
none_qs_offers = SpecialOffers.objects.none()
offers_qs = list(chain(none_qs_offers, offers_list))

prices_list = [Prices(pk=1, tariff_name="Студенческий", tariff_description="Описание тарифа", price_one_month=4500, \
                      price_three_month=9000, price_six_month=16000, price_one_year=28000, is_time_restricted=True, \
                      min_time="08:00:00", max_time="18:00:00", days_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]
none_qs_price = Prices.objects.none()
prices_qs = list(chain(none_qs_price, prices_list))

super_user = CustomUser(pk=1, login='aaa', email='bbb@mail.ru', password='password', role=3, club=1)
admin_user = CustomUser(pk=2, login='aaas', email='ccc@mail.ru', password='password', role=2, club=1)
instructor_user = CustomUser(pk=3, login='bbb', email='ttb@mail.ru', password='password', role=1, club=1)
customer_user = CustomUser(pk=4, login='lll', email='rrr@mail.ru', password='password', role=0, club=1)

super_users_list_for_read_filtered = [super_user]
none_qs_users = CustomUser.objects.none()
super_users_qs_for_read_filtered = list(chain(none_qs_users, super_users_list_for_read_filtered))

admin_users_list_for_read_filtered = [admin_user]
none_qs_admin_users = CustomUser.objects.none()
admin_users_qs_for_read_filtered = list(chain(none_qs_admin_users, admin_users_list_for_read_filtered))

instructor_users_list_for_read_filtered = [instructor_user]
none_qs_instructor_users = CustomUser.objects.none()
instructor_users_qs_for_read_filtered = list(chain(none_qs_instructor_users, instructor_users_list_for_read_filtered))

customer_users_list_for_read_filtered = [customer_user]
none_qs_customer_users = CustomUser.objects.none()
customer_users_qs_for_read_filtered = list(chain(none_qs_customer_users, customer_users_list_for_read_filtered))

customer = Customers(pk=1, user=customer_user, sex="man", name="Григорий", surname="Владимирский", patronymic="Антонович",
                     day_of_birth="1989-05-23", height=177, measured_weights="[\"106\"]",
            measure_dates="[\"2019-01-01\"]", tariff=prices_list[0], tariff_end_date="2021-08-14", instructor=None)

customer_list_for_read_filtered = [customer]
none_qs_customer = Customers.objects.none()
customer_qs_for_read_filtered = list(chain(none_qs_customer, customer_list_for_read_filtered))

admin = Administrators(pk=1, name="Валерия", surname="Филатова", patronym="Анатольевна")

admin_list_for_read_filtered = [admin]
none_qs_admin = Administrators.objects.none()
admin_qs_for_read_filtered = list(chain(none_qs_admin, admin_list_for_read_filtered))

instructor = Instructors(pk=1, user=instructor_user, sex="woman", name="Елизавета", surname="Потапова",
                         patronymic="Николаевна", education=["Education"], experience=20, achievements=["a", "b", "c"],
                         specialization=["ssss"], photo="images/1.jpg", is_active=True, admin=admin)

instructor_list_for_read_filtered = [instructor]
none_qs_instructor = Instructors.objects.none()
instructor_qs_for_read_filtered = list(chain(none_qs_instructor, instructor_list_for_read_filtered))