from manager.services import CustomersService, CustomUserService, PricesService, InstructorsService, AdministratorsService, GroupClassesCustomersRecordsService
from django.test import TestCase, RequestFactory, Client
from .dataBuilder import *
from .data.data_for_tests import *
from django.contrib.auth.models import AnonymousUser
import unittest
from unittest.mock import MagicMock
from users.models import CustomUser
from api.customer_views import CustomerProfileView, CustomerEditProfileView, \
    CustomerEditProfileMeasureView, CustomerTrainingRecordsView, \
    CustomerCreatePersonalTrainingRecordView, CustomerDeletePersonalTrainingRecordView, CustomerDeleteGroupTrainingRecordView, \
    CustomerAddGroupClassesRecordView, CustomerAppointmentToInstructorView

from api.serializers import ServicesSerializer, CustomersSerializer, CustomUserSerializer, AdministratorsSerializer, \
GroupClassesSerializer, GroupClassesCustomersRecordsSerializer, InstructorsSerializer, GroupClassesSheduleSerializer, \
AdminRecordsSerializer, InstructorSheduleSerializer, AInstructorSheduleCustomersSerializer, PricesSerializer, \
SpecialOffersSerializer, InstructorPersonalTrainingsLogsSerializer, AdminGroupClassesLogsSerializer, FitnessClubsSerializer

class E2ETestCustomer(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',\
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',\
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.maxDiff = None

    def test_customer_actions(self):
        # arrange
        user = CustomerUser().user
        customer = CustomersService.read_filtered(user, {'user': user.id})

        # act смотрит профиль
        view = CustomerProfileView()
        request = self.factory.get('/customer_profile/')
        request.user = user
        result_data = view.get(request).data

        # assert
        self.assertEqual(len(customer), 1)
        self.assertEqual(result_data['role'], {'is_customer': True,
                                               'customer': CustomersSerializer(customer[0]).data,
                                               'is_instructor': False, 'instructor': InstructorsSerializer().data,
                                               'is_admin': False, 'admin': AdministratorsSerializer().data,
                                               'is_guest': False, 'user': CustomUserSerializer(user).data})
        self.assertEqual(result_data['today'], datetime.datetime.today().strftime('%Y-%m-%d'))

        # act удаляет последнее измерение веса
        view = CustomerEditProfileMeasureView()
        request = self.factory.get('/delete_measure/')
        request.user = user
        view.delete(request)
        customer = CustomersService.read_filtered(user, {'user': user.id})

        # assert
        self.assertEqual(len(customer[0].measured_weights), 0)

        # act добавляет измерение веса
        request = self.factory.get('/add_measure/')
        request.user = user
        request.data = {'weight': 80, 'date': "2021-10-12"}
        view.put(request)
        customer = CustomersService.read_filtered(user, {'user': user.id})

        # assert
        self.assertEqual(len(customer[0].measured_weights), 1)
        self.assertEqual(customer[0].measured_weights[0], 80)
        self.assertEqual(customer[0].measure_dates[0], datetime.date(2021, 10, 12))


        # act запись на групповое занятие
        request = self.factory.get('/add_group_class_record/')
        request.user = user
        view = CustomerAddGroupClassesRecordView()
        request.data = {'date_raw': "2022-01-03", 'shedule_id': 1}
        view.post(request)
        group_classs = GroupClassesCustomersRecordsService.read_filtered(user, {'shedule_id': 1, "customer": customer[0].pk, "class_date":datetime.date(2022, 1, 3)})

        # assert
        self.assertEqual(len(group_classs), 1)

        # act отмена записи на групповое занятие
        request = self.factory.get('/delete_group_class_record/')
        request.user = user
        view = CustomerDeleteGroupTrainingRecordView()
        view.delete(request, **{'record_id': group_classs[0].pk})

        # assert
        self.assertEqual(len(GroupClassesCustomersRecordsService.read_filtered(user, {'shedule_id': 1, "customer": customer[0].pk, "class_date":datetime.date(2022, 1, 3)})), 0)






