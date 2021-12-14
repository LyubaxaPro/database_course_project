from manager.services import CustomersService, GroupClassesCustomersRecordsService, InstructorSheduleCustomersService
from django.test import TestCase, RequestFactory, Client
from http import HTTPStatus
from .dataBuilder import *
from .data.data_for_tests import *
from .customer_views import *
from api.customer_views import CustomerProfileView, CustomerEditProfileView, \
    CustomerEditProfileMeasureView, CustomerTrainingRecordsView, \
    CustomerCreatePersonalTrainingRecordView, CustomerDeletePersonalTrainingRecordView, CustomerDeleteGroupTrainingRecordView, \
    CustomerAddGroupClassesRecordView, CustomerAppointmentToInstructorView
from api.serializers import ServicesSerializer, CustomersSerializer, CustomUserSerializer, AdministratorsSerializer, \
GroupClassesSerializer, GroupClassesCustomersRecordsSerializer, InstructorsSerializer, GroupClassesSheduleSerializer, \
AdminRecordsSerializer, InstructorSheduleSerializer, AInstructorSheduleCustomersSerializer, PricesSerializer, \
SpecialOffersSerializer, InstructorPersonalTrainingsLogsSerializer, AdminGroupClassesLogsSerializer, FitnessClubsSerializer

class TestCustomer(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs', \
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',\
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json', 'specialOffers.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.maxDiff = None

    def test_customer_profile_url_status_code(self):
        user = CustomerUser().user
        request = self.factory.get('/customer_profile/')
        request.user = user

        result_data = customer_profile(request)

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_customer_profile_func_data(self):
        user = CustomerUser().user
        request = self.factory.get('/customer_profile/')
        request.user = user
        view = CustomerProfileView()
        customer = CustomersService.read_filtered(user, {'user': user.id})

        result_data = view.get(request).data

        self.assertEqual(len(customer), 1)
        self.assertEqual(result_data['role'], {'is_customer': True,
    'customer': CustomersSerializer(customer[0]).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data})
        self.assertEqual(result_data['today'], datetime.datetime.today().strftime('%Y-%m-%d'))

    def test_edit_customer_url_status_code(self):
        user = CustomerUser().user
        request = self.factory.get('/customer_profile/')
        request.user = user

        result_data = edit_customer_profile(request)

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_customer_training_records_func(self):
        user = CustomerUser().user
        request = self.factory.get('/customer_training_records/')
        request.user = user
        customer = CustomersService.read_filtered(user, {'user' : user.id})
        view = CustomerTrainingRecordsView()

        result_data = view.get(request).data

        self.assertEqual(len(customer), 1)
        self.assertEqual(result_data['role'], {'is_customer': True,
    'customer': CustomersSerializer(customer[0]).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data})
        self.assertEqual(result_data['pass_group_classes'], customer_pass_group_classes)
        self.assertEqual(result_data['future_group_classes'], [])
        self.assertEqual(result_data['pass_personal_trainings'], [])
        self.assertEqual(result_data['future_personal_trainings'], [])

    def test_delete_personal_training_record(self):
        user = UserByPk(16).user
        request = self.factory.get('/delete_personal_training_record/?record_id=13')
        request.user = user
        prev_qs = InstructorSheduleCustomersService.read_all(user)
        l = len(prev_qs)

        delete_personal_training_record(request)

        self.assertNotEqual(prev_qs, InstructorSheduleCustomersService.read_all(user))

    def test_delete_group_class_record(self):
        user = UserByPk(16).user
        request = self.factory.get('/delete_group_class_record/?record_id=46')
        request.user = user
        prev_qs = GroupClassesCustomersRecordsService.read_all(user)
        l = len(prev_qs)

        delete_group_class_record(request)

        self.assertEqual(len(GroupClassesCustomersRecordsService.read_all(user)), l - 1)
        self.assertNotEqual(prev_qs, GroupClassesCustomersRecordsService.read_all(user))

