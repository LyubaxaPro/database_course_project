from manager.repositories import InstructorsRepository, InstructorSheduleRepository
from django.test import TestCase, RequestFactory, Client
from http import HTTPStatus
from fitness_clubs_system.main.dataBuilder import *
from fitness_clubs_system.main.view_funcs.instructor import *
from fitness_clubs_system.main.data.data_for_tests import *

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

        response = instructor_profile(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_instructor_profile_func_data(self):
        user = InstructorUser().user
        request = self.factory.get('/instructor_profile/')
        request.user = user
        instructor = InstructorsRepository.read_filtered(user, {'user' : user.id})

        response = instructor_profile_func(request)

        self.assertEqual(len(instructor), 1)
        self.assertEqual(response['role'], {'is_customer': False, 'customer': None, 'is_instructor': True,
            'instructor': instructor[0], 'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})
        self.assertEqual(response['address'], 'Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)')

    def test_instructor_attached_customers_func(self):
        user = UserByPk(11).user
        request = self.factory.get('/instructor_profile/')
        request.user = user
        instructor = InstructorsRepository.read_filtered(user, {'user': user.id})

        response = instructor_attached_customers_func(request)

        self.assertEqual(len(instructor), 1)
        self.assertEqual(response['role'],
                         {'is_customer': False, 'customer': None, 'is_instructor': True, 'instructor': instructor[0],
                          'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})
        self.assertEqual(len(response['customers_data']), 1)
        self.assertEqual(response['customers_data'][0]['name'], 'Яна')
        self.assertEqual(response['customers_data'][0]['surname'], 'Обломова')
        self.assertEqual(response['customers_data'][0]['patronymic'], 'Игоревна')

    def test_instructor_add_personal_training(self):
        user = UserByPk(11).user
        request = self.factory.get('/instructor_add_personal_training/?day=Monday&time=21:00')
        request.user = user

        instructor_add_personal_training(request)

        self.assertNotEqual(InstructorSheduleRepository.read_filtered(user, {'day_of_week': 'Monday',
                                                                             'training_time': '21:00:00'}), None)

    def test_instructor_delete_personal_training(self):
        user = UserByPk(11).user
        prev_qs = InstructorSheduleRepository.read_all(user)
        request = self.factory.get('/instructor_delete_personal_training/?i_shedule_id=1')
        request.user = user

        instructor_delete_personal_training(request)

        self.assertNotEqual(prev_qs, InstructorSheduleRepository.read_all(user))

    def test_instructor_training_records_func(self):
        user = UserByPk(11).user
        request = self.factory.get('instructor_training_records/')
        request.user = user
        instructor = InstructorsRepository.read_filtered(user, {'user': user.id})

        response = instructor_training_records_func(request)

        self.assertEqual(len(instructor), 1)

        self.assertEqual(response['role'],
                         {'is_customer': False, 'customer': None, 'is_instructor': True, 'instructor': instructor[0],
                          'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})
        self.assertEqual(response['address'], 'Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)')
        self.assertEqual(response['shedule'], instructor_user_11_schedule)
        self.assertEqual(response['day_of_week_date'], {'Понедельник': datetime.date(2021, 10, 11),
                                                        'Вторник': datetime.date(2021, 10, 12),
                                                        'Среда': datetime.date(2021, 10, 13),
                                                        'Четверг': datetime.date(2021, 10, 14),
                                                        'Пятница': datetime.date(2021, 10, 15),
                                                        'Суббота': datetime.date(2021, 10, 16),
                                                        'Воскресенье': datetime.date(2021, 10, 17)})
