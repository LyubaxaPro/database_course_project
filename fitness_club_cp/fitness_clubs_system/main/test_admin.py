from manager.services import GroupClassesSheduleService, SpecialOffersService, AdministratorsService
from django.test import TestCase, RequestFactory, Client
from http import HTTPStatus
from .dataBuilder import *
from api.serializers import ServicesSerializer, CustomersSerializer, CustomUserSerializer, AdministratorsSerializer, \
GroupClassesSerializer, GroupClassesCustomersRecordsSerializer, InstructorsSerializer, GroupClassesSheduleSerializer, \
AdminRecordsSerializer, InstructorSheduleSerializer, AInstructorSheduleCustomersSerializer, PricesSerializer, \
SpecialOffersSerializer, InstructorPersonalTrainingsLogsSerializer, AdminGroupClassesLogsSerializer, FitnessClubsSerializer

from .forms import *
from api.admin_views import AdminProfileView, AdminGroupClassesView,\
    AdminDeleteGroupClassesView, AdminDeleteSpecialOfferView, AdminAdminSpecialOfferView, AdminStatisticsView, \
    AdminActivateInstructorView, AdminRejectInstructorView
from .admin_views import *
class TestAdmin(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs', \
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',\
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json', 'specialOffers.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.maxDiff = None

    def test_admin_profile_url_status_code(self):
        user = SuperUser().user
        request = self.factory.get('/admin_profile/')
        request.user = user

        result_data = admin_profile(request)

        self.assertEqual(result_data.status_code, HTTPStatus.OK)

    def test_admin_profile_func_data(self):
        user = SuperUser().user
        request = self.factory.get('/admin_profile/')
        request.user = user
        admin = AdministratorsService.read_filtered(user, {'user': user.id})
        view = AdminProfileView()

        result_data = view.get(request).data

        self.assertEqual(len(admin), 1)
        self.assertEqual(result_data['role'], {'is_customer': False,
    'customer': CustomersSerializer().data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': True, 'admin': AdministratorsSerializer(admin[0]).data, 'is_guest': False, 'user': CustomUserSerializer(user).data})
        self.assertEqual(result_data['address'], '????????????, ????. ???????????????????? ????????, ????14, 4 ???????? (?????? ????????????????)')

    def test_delete_group_class_in_shedule(self):
        user = SuperUser().user
        prev_qs = GroupClassesSheduleService.read_all(user)
        request = self.factory.get('/delete_group_class_in_shedule/?shedule_id=1')
        request.user = user

        delete_group_class_in_shedule(request)

        self.assertNotEqual(prev_qs, GroupClassesSheduleService.read_all(user))

    def test_delete_special_offer_by_admin(self):
        user = SuperUser().user
        prev_qs = SpecialOffersService.read_all(user)
        request = self.factory.get('/delete_special_offer_by_admin/?offer_id=1')
        request.user = user

        delete_special_offer_by_admin(request)

        self.assertNotEqual(prev_qs, SpecialOffersService.read_all(user))

    def test_add_special_offer_by_admin(self):
        user = SuperUser().user
        request = self.factory.get('/add_special_offer_by_admin/?offer_name=Super offer!&offer_description=fffff')
        request.user = user

        add_special_offer_by_admin(request)

        self.assertNotEqual(None, SpecialOffersService.read_filtered(user, {'offer_name': 'Super offer!',
                                                                               'offer_description': 'fffff'}))