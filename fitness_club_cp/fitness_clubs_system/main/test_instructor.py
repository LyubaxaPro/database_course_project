from manager.services import InstructorsService, InstructorSheduleService
from django.test import TestCase, RequestFactory, Client
from http import HTTPStatus
from .dataBuilder import *
from .data.data_for_tests import *
from .instructor_views import *
from api.instructor_views import InstructorView, InstructorAttachedCustomersView, InstructorEditProfileView,\
 InstructorAddPersonalTrainingView, InstructorDeleteProfileChangesView, \
    InstructorDeletePersonalTrainingView, InstructorTrainingRecordsView
from api.serializers import ServicesSerializer, CustomersSerializer, CustomUserSerializer, AdministratorsSerializer, \
GroupClassesSerializer, GroupClassesCustomersRecordsSerializer, InstructorsSerializer, GroupClassesSheduleSerializer, \
AdminRecordsSerializer, InstructorSheduleSerializer, AInstructorSheduleCustomersSerializer, PricesSerializer, \
SpecialOffersSerializer, InstructorPersonalTrainingsLogsSerializer, AdminGroupClassesLogsSerializer, FitnessClubsSerializer

class TestInstructor(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs', \
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',\
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json', 'specialOffers.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.maxDiff = None

    def test_instructor_profile_url_status_code(self):
        user = InstructorUser().user
        request = self.factory.get('/instructor_profile/')
        request.user = user

        result_data = instructor_profile(request)

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_instructor_profile_func_data(self):
        user = InstructorUser().user
        request = self.factory.get('/instructor_profile/')
        request.user = user
        instructor = InstructorsService.read_filtered(user, {'user' : user.id})
        view = InstructorView()

        result_data = view.get(request).data

        self.assertEqual(len(instructor), 1)
        self.assertEqual(result_data['role'], {'is_customer': False,
    'customer': CustomersSerializer().data,'is_instructor': True, 'instructor': InstructorsSerializer(instructor[0]).data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data})
        self.assertEqual(result_data['address'], 'Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)')

    def test_instructor_attached_customers_func(self):
        user = UserByPk(11).user
        request = self.factory.get('/instructor_profile/')
        request.user = user
        instructor = InstructorsService.read_filtered(user, {'user': user.id})
        view = InstructorAttachedCustomersView()

        result_data = view.get(request).data

        self.assertEqual(len(instructor), 1)
        self.assertEqual(result_data['role'],{'is_customer': False,
    'customer': CustomersSerializer().data,'is_instructor': True, 'instructor': InstructorsSerializer(instructor[0]).data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data})
        self.assertEqual(len(result_data['customers_data']), 1)
        self.assertEqual(result_data['customers_data'][0]['name'], 'Яна')
        self.assertEqual(result_data['customers_data'][0]['surname'], 'Обломова')
        self.assertEqual(result_data['customers_data'][0]['patronymic'], 'Игоревна')

    def test_instructor_add_personal_training(self):
        user = UserByPk(11).user
        request = self.factory.get('/instructor_add_personal_training/?day=Monday&time=21:00')
        request.user = user

        instructor_add_personal_training(request)

        self.assertNotEqual(InstructorSheduleService.read_filtered(user, {'day_of_week': 'Monday',
                                                                             'training_time': '21:00:00'}), None)

    def test_instructor_delete_personal_training(self):
        user = UserByPk(11).user
        prev_qs = InstructorSheduleService.read_all(user)
        request = self.factory.get('/instructor_delete_personal_training/?i_shedule_id=1')
        request.user = user

        instructor_delete_personal_training(request)

        self.assertNotEqual(prev_qs, InstructorSheduleService.read_all(user))

    def test_instructor_training_records_func(self):
        user = UserByPk(11).user
        request = self.factory.get('instructor_training_records/')
        request.user = user
        instructor = InstructorsService.read_filtered(user, {'user': user.id})
        view = InstructorTrainingRecordsView()

        result_data = view.get(request, **{"week_num": "2021-W35"}).data

        self.assertEqual(len(instructor), 1)
        self.assertEqual(result_data['role'], {'is_customer': False,
    'customer': CustomersSerializer().data,'is_instructor': True, 'instructor': InstructorsSerializer(instructor[0]).data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data})
        self.assertEqual(result_data['address'], 'Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)')
        self.assertEqual(result_data['shedule'], instructor_user_11_schedule)
