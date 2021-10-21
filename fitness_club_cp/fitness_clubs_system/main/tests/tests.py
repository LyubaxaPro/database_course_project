from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository, \
    InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, AdministratorsRepository
from django.test import TestCase, RequestFactory, Client
from http import HTTPStatus
from django.contrib.auth.models import AnonymousUser
from fitness_clubs_system.main.dataBuilder import *
from fitness_clubs_system.api.view_funcs.simple_data import *
from fitness_clubs_system.api.view_funcs.role import *
from fitness_clubs_system.main.data.data_for_tests import *
class TestIndex(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json', 'prices.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_index_url_status_code(self):
        response = self.c.get('/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_index_render_html_page(self):
        response = self.c.get('/')

        self.assertTemplateUsed(response, 'main/index.html')

    def test_index_data(self):
        user = CustomerUser().user
        request = self.factory.get('/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user': user.id})

        response = index_func(request)

        self.assertEqual(len(customer), 1)
        self.assertEqual(response, {'title': 'Главная страница', 'role': {'is_customer': True, 'customer': customer[0], 'is_instructor': False, 'instructor': None, 'is_admin': False, 'admin': None, 'is_guest': False, 'user': user}})

class TestAddress(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json', 'prices.json', 'fitness_clubs']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.maxDiff = None

    def test_address_url_status_code(self):
        response = self.c.get('/address/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_address_render_html_page(self):
        response = self.c.get('/address/')

        self.assertTemplateUsed(response, 'main/address.html')

    def test_address_data(self):
        user = CustomerUser().user
        request = self.factory.get('/address/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user' : user.id})
        clubs = FitnessClubsRepository.read_all(user)

        response = address_func(request)

        self.assertEqual(len(customer), 1)
        self.assertEqual(len(response['clubs']), len(clubs))

        for i in range(len(response['clubs'])):
            self.assertEqual(response['clubs'][i], clubs[i])

        self.assertEqual(response['role'], {'is_customer': True, 'customer': customer[0], 'is_instructor': False,
                                            'instructor': None, 'is_admin': False, 'admin': None,
                                            'is_guest': False, 'user': user})

class TestService(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json',
                'prices.json', 'services']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_services_url_status_code(self):
        response = self.c.get('/services/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_services_render_html_page(self):
        response = self.c.get('/services/')

        self.assertTemplateUsed(response, 'main/services.html')

    def test_service_data(self):
        user = CustomerUser().user
        request = self.factory.get('/services/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user' : user.id})
        services = ServicesRepository.read_all(user)

        response = services_func(request)

        self.assertEqual(len(customer), 1)
        self.assertEqual(len(response['services']), len(services))
        for i in range(len(response['services'])):
            self.assertEqual(response['services'][i], services[i])
        self.assertEqual(response['role'],
                         {'is_customer': True, 'customer': customer[0], 'is_instructor': False, 'instructor': None,
                          'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})

class TestGetClubSchedule(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_get_club_schedule(self):
        user = CustomerUser().user
        request = self.factory.get('/get_club_schedule/?club_id=1')
        request.user = user

        response = get_club_schedule(request)

        self.assertEqual(response.content, club_1_schedule)

class TestGroupClasses(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_groupclasses_url_status_code(self):
        response = self.c.get('/groupclasses/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_groupclasses_render_html_page(self):
        response = self.c.get('/groupclasses/')

        self.assertTemplateUsed(response, 'main/group_classes.html')

    def test_groupclasses_data(self):
        user = CustomerUser().user
        request = self.factory.get('/groupclasses/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user' : user.id})
        gclasses = GroupClassesRepository.read_all(user)

        response = groupclasses_func(request)

        self.assertEqual(len(customer), 1)
        self.assertEqual(response['classes_data'], classes_data_club1)
        self.assertEqual(len(response['classes']), len(gclasses))
        for i in range(len(response['classes'])):
            self.assertEqual(response['classes'][i], gclasses[i])
        self.assertEqual(response['role'],
                         {'is_customer': True, 'customer': customer[0], 'is_instructor': False, 'instructor': None,
                          'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})

class TestInstructorsList(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_instructors_list_url_status_code(self):
        response = self.c.get('/instructors/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_instructors_list_render_html_page(self):
        response = self.c.get('/instructors/')

        self.assertTemplateUsed(response, 'main/instructors.html')

    def test_instructors_list_data(self):
        user = CustomerUser().user
        request = self.factory.get('/instructors/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user' : user.id})
        instructors = InstructorsRepository.read_all(user)

        response = instructors_list_func(request)

        self.assertEqual(len(customer), 1)
        self.assertEqual(len(response['instructors']), len(instructors))
        for i in range(len(response['instructors'])):
            self.assertEqual(response['instructors'][i], instructors[i])
        self.assertEqual(response['role'],
                         {'is_customer': True, 'customer': customer[0], 'is_instructor': False, 'instructor': None,
                          'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})

    def test_instructors_detail_url_status_code(self):
        response = self.c.get('/instructors/1/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_instructors_detail_render_html_page(self):
        response = self.c.get('/instructors/1/')

        self.assertTemplateUsed(response, 'main/instructor_detail.html')

    def test_instructors_detail_data(self):
        user = CustomerUser().user
        request = self.factory.get('/instructors/1/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user' : user.id})
        instructor = InstructorsRepository.read_by_pk(user, 1)

        response = instructor_detail_func(request, 1)

        self.assertEqual(len(customer), 1)
        self.assertEqual(response, get_instructor_1_detail_data(instructor, customer[0], user))

class TestPrices(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json',
                'specialOffers.json']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_prices_url_status_code(self):
        response = self.c.get('/prices/')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_prices_render_html_page(self):
        response = self.c.get('/prices/')

        self.assertTemplateUsed(response, 'main/prices.html')

    def test_prices_data(self):
        user = CustomerUser().user
        request = self.factory.get('/prices/')
        request.user = user
        customer = CustomersRepository.read_filtered(user, {'user' : user.id})
        special_offers = SpecialOffersRepository.read_all(user)
        prices = PricesRepository.read_all(user)

        response = prices_func(request)

        self.assertEqual(len(customer), 1)
        self.assertEqual(len(response['special_offers']), len(special_offers))
        self.assertEqual(len(response['prices']), len(prices))
        for i in range(len(response['special_offers'])):
            self.assertEqual(response['special_offers'][i], special_offers[i])
        for i in range(len(response['prices'])):
            self.assertEqual(response['prices'][i], prices[i])

        self.assertEqual(response['role'],
                         {'is_customer': True, 'customer': customer[0], 'is_instructor': False, 'instructor': None,
                          'is_admin': False, 'admin': None, 'is_guest': False, 'user': user})

class CheckRoleTest(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json', 'prices.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_get_role_superuser(self):
        user = SuperUser().user
        request = self.factory.get('/')
        request.user = user
        right_answer = (False, None, False, None, True, AdministratorsRepository.read_by_pk(user, 1), False,
                        CustomUserRepository.read_by_pk(user, 1))

        response = get_role(request)

        self.assertNotEqual(CustomUserRepository.read_by_pk(
            user, 1), None)
        self.assertEqual(len(response), len(right_answer))
        for i in range (len(response)):
            self.assertEqual(response[i], right_answer[i])

    def test_get_role_admin(self):
        user = AdminUser().user
        request = self.factory.get('/')
        request.user = user
        right_answer = (False, None, False, None, True, AdministratorsRepository.read_by_pk(user, 2), False,
                        CustomUserRepository.read_by_pk(user, 2))

        response = get_role(request)

        self.assertEqual(len(response), len(right_answer))
        for i in range (len(response)):
            self.assertEqual(response[i], right_answer[i])

    def test_get_role_instructor(self):
        user = InstructorUser().user
        request = self.factory.get('/')
        request.user = user
        right_answer = (False, None, True, InstructorsRepository.read_by_pk(user, 1), False, None, False,
                        CustomUserRepository.read_by_pk(user, 9))

        response = get_role(request)

        self.assertEqual(len(response), len(right_answer))
        for i in range (len(response)):
            self.assertEqual(response[i], right_answer[i])

    def test_get_role_customer(self):
        user = CustomerUser().user
        request = self.factory.get('/')
        request.user = user
        right_answer = (True, CustomersRepository.read_by_pk(user, 1), False, None, False, None, False,
                        CustomUserRepository.read_by_pk(user, 14))

        response = get_role(request)

        self.assertEqual(len(response), len(right_answer))
        for i in range (len(response)):
            self.assertEqual(response[i], right_answer[i])

    def test_get_role_guest(self):
        user = AnonymousUser()
        request = self.factory.get('/')
        request.user = user
        right_answer = (False, None, False, None, False, None, True, None)

        response = get_role(request)

        self.assertEqual(len(response), len(right_answer))
        for i in range (len(response)):
            self.assertEqual(response[i], right_answer[i])

