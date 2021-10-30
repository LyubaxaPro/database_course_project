from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository, \
    InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, AdministratorsRepository
from django.test import TestCase, RequestFactory, Client
from http import HTTPStatus
from django.contrib.auth.models import AnonymousUser
from .dataBuilder import *
from .data.data_for_tests import *
from api.common_views import IndexView, AddressView, ServicesView, ClubGroupClassesView, ClubInstructorsView, \
    ClubInstructorsDetailView, ClubGroupClassesScheduleForClubView, ClubInstructorsForClubView, PricesView
from .common_views import *
from api.role import get_role

class TestIndex(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json', 'prices.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_index_url_status_code(self):
        result_data = self.c.get('/')

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_index_render_html_page(self):
        result_data = self.c.get('/')

        self.assertTemplateUsed(result_data, 'main/index.html')

    def test_index_data(self):
        user = CustomerUser().user
        request = self.factory.get('/')
        request.user = user
        indexView = IndexView()

        result_data = indexView.get(request)

        self.assertEqual(result_data.data, get_customer_user_index_data(user))

class TestAddress(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json', 'prices.json', 'fitness_clubs']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.maxDiff = None

    def test_address_url_status_code(self):
        result_data = self.c.get('/address/')

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_address_render_html_page(self):
        result_data = self.c.get('/address/')

        self.assertTemplateUsed(result_data, 'main/address.html')

    def test_address_data(self):
        user = CustomerUser().user
        request = self.factory.get('/address/')
        request.user = user
        view = AddressView()

        result_data = view.get(request)

        self.assertEqual(result_data.data, get_customer_user_adress(user))

class TestService(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json',
                'prices.json', 'services']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_services_url_status_code(self):
        result_data = self.c.get('/services/')

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_services_render_html_page(self):
        result_data = self.c.get('/services/')

        self.assertTemplateUsed(result_data, 'main/services.html')

    def test_service_data(self):
        user = CustomerUser().user
        request = self.factory.get('/services/')
        request.user = user
        view = ServicesView()

        result_data = view.get(request)

        self.assertEqual(result_data.data, get_service_customer_user_data(user))

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

        result_data = get_club_schedule(request)

        self.assertEqual(result_data.content, club_1_schedule)

class TestGroupClasses(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_groupclasses_url_status_code(self):
        result_data = self.c.get('/groupclasses/')

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_groupclasses_render_html_page(self):
        result_data = self.c.get('/groupclasses/')

        self.assertTemplateUsed(result_data, 'main/group_classes.html')

    def test_groupclasses_data(self):
        user = CustomerUser().user
        request = self.factory.get('/groupclasses/')
        request.user = user
        view = ClubGroupClassesView()

        result_data = view.get(request).data

        self.assertEqual(result_data, get_groupclasses_customer_user_data(user))

class TestInstructorsList(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_instructors_list_url_status_code(self):
        result_data = self.c.get('/instructors/')

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_instructors_list_render_html_page(self):
        result_data = self.c.get('/instructors/')

        self.assertTemplateUsed(result_data, 'main/instructors.html')

    def test_instructors_list_data(self):
        user = CustomerUser().user
        request = self.factory.get('/instructors/')
        request.user = user
        view = ClubInstructorsView()

        result_data = view.get(request).data

        self.assertEqual(result_data, get_instructors_list_data(user))

    def test_instructors_detail_url_status_code(self):
        result_data = self.c.get('/instructors/1/')

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_instructors_detail_render_html_page(self):
        result_data = self.c.get('/instructors/1/')

        self.assertTemplateUsed(result_data, 'main/instructor_detail.html')

    def test_instructors_detail_data(self):
        user = CustomerUser().user
        request = self.factory.get('/instructors/1/')
        request.user = user
        view = ClubInstructorsDetailView()

        result_data = view.get(request, **{'pk': 1}).data

        self.assertEqual(result_data, get_instructor_1_detail_data(user))

class TestPrices(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json',
                'specialOffers.json']

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_prices_url_status_code(self):
        result_data = self.c.get('/prices/')

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_prices_render_html_page(self):
        result_data = self.c.get('/prices/')

        self.assertTemplateUsed(result_data, 'main/prices.html')

    def test_prices_data(self):
        user = CustomerUser().user
        request = self.factory.get('/prices/')
        request.user = user
        view = PricesView()

        result_data = view.get(request).data

        self.assertEqual(result_data, get_prices_customer_user_data(user))

class CheckRoleTest(TestCase):
    fixtures = ['myCustomUsers.json', 'administrators.json', 'instructors.json', 'customers.json', 'prices.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_get_role_superuser(self):
        user = SuperUser().user
        request = self.factory.get('/')
        request.user = user

        result_data = get_role(request)

        self.assertEqual(result_data, get_role_superuser(user))

    def test_get_role_admin(self):
        user = AdminUser().user
        request = self.factory.get('/')
        request.user = user

        result_data = get_role(request)

        self.assertEqual(result_data, get_role_admin(user))

    def test_get_role_instructor(self):
        user = InstructorUser().user
        request = self.factory.get('/')
        request.user = user

        result_data = get_role(request)

        self.assertEqual(result_data, get_role_instructor(user))

    def test_get_role_customer(self):
        user = CustomerUser().user
        request = self.factory.get('/')
        request.user = user

        result_data = get_role(request)

        self.assertEqual(result_data, get_role_customer(user))

    def test_get_role_guest(self):
        user = AnonymousUser()
        request = self.factory.get('/')
        request.user = user

        result_data = get_role(request)

        self.assertEqual(result_data, get_role_anon())

