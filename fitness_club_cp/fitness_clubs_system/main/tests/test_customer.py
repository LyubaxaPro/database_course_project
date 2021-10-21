from manager.repositories import CustomersRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository
from django.test import TestCase, RequestFactory, Client
from http import HTTPStatus
from fitness_clubs_system.main.dataBuilder import *
from fitness_clubs_system.api.customer import *
from fitness_clubs_system.main.data.data_for_tests import *

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

        response = customer_profile(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_customer_profile_func_data(self):
        user = CustomerUser().user
        request = self.factory.get('/customer_profile/')
        request.user = user
        response = customer_profile_func(request)

        customer = CustomersRepository.read_filtered(user, {'user' : user.id})

        self.assertEqual(len(customer), 1)
        self.assertEqual(response['role'], {'is_customer': True, 'customer': customer[0], 'is_instructor': False,
                                            'instructor': None,'is_admin': False, 'admin': None, 'is_guest': False,
                                            'user': user})
        self.assertNotEqual(response['address'], None)
        self.assertNotEqual(response['form'], None)
        self.assertEqual(response['today'], datetime.datetime.today().strftime('%Y-%m-%d'))

    def test_edit_customer_url_status_code(self):
        response = self.c.get('/edit_customer/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_customer_render_html_page(self):
        response = self.c.get('/edit_customer/')

        self.assertTemplateUsed(response, 'main/edit_customer.html')

    def test_customer_training_records_func(self):
        user = CustomerUser().user
        request = self.factory.get('/customer_training_records/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user' : user.id})

        response = customer_training_records_func(request)

        self.assertEqual(len(customer), 1)
        self.assertEqual(response['role'], {'is_customer': True, 'customer': customer[0], 'is_instructor': False,
                        'instructor': None, 'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})
        self.assertEqual(response['pass_group_classes'], customer_pass_group_classes)
        self.assertEqual(response['future_group_classes'], [])
        self.assertEqual(response['pass_personal_trainings'], [])
        self.assertEqual(response['future_personal_trainings'], [])

    def test_delete_personal_training_record(self):
        user = UserByPk(16).user
        request = self.factory.get('/delete_personal_training_record/?record_id=1')
        request.user = user
        prev_qs = InstructorSheduleCustomersRepository.read_all(user)
        l = len(prev_qs)

        delete_personal_training_record(request)

        self.assertEqual(len(InstructorSheduleCustomersRepository.read_all(user)), l - 1)
        self.assertNotEqual(prev_qs, InstructorSheduleCustomersRepository.read_all(user))

    def test_delete_group_class_record(self):
        user = UserByPk(16).user
        request = self.factory.get('/delete_group_class_record/?record_id=1')
        request.user = user
        prev_qs = GroupClassesCustomersRecordsRepository.read_all(user)
        l = len(prev_qs)

        delete_group_class_record(request)

        self.assertEqual(len(GroupClassesCustomersRecordsRepository.read_all(user)), l - 1)
        self.assertNotEqual(prev_qs, GroupClassesCustomersRecordsRepository.read_all(user))

