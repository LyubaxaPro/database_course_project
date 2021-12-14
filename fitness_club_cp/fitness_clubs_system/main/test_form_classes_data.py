from django.test import TestCase, RequestFactory, Client
from manager.services import ServicesService, FitnessClubsService, GroupClassesService,\
    GroupClassesSheduleService, InstructorsService, CustomUserService, SpecialOffersService, PricesService,\
    CustomersService, InstructorSheduleService, GroupClassesCustomersRecordsService, InstructorSheduleCustomersService,\
    AdministratorsService, AdminRecordsService, InstructorPersonalTrainingsLogsService, AdminGroupClassesLogsService
from .dataBuilder import *
from api.form_classes_data import form_classes_data, form_admin_classes_data, form_data_for_tarif
from api.instructor_schedule import form_instructors_shedule, form_instructors_shedule_for_week
from .data.data_for_tests import *

class CheckFormData(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',\
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',\
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        datetime_object = datetime.datetime.strptime('May 29 2021', '%b %d %Y')
        my_week_raw = datetime_object.isocalendar()
        self.week = str(my_week_raw[0]) + '-W' + str(my_week_raw[1])

    def test_form_classes_data(self):
        user = UserByPk(14).user

        result_data = form_classes_data(user, 1)

        self.assertEqual(result_data, classes_data_for_user_14)

    def test_form_admin_classes_data(self):
        user = SuperUser().user

        result_data = form_admin_classes_data(user, 1, self.week)

        self.assertEqual(result_data, admin_classes_data_for_superuser)

    def test_form_data_for_tarif(self):
        user = UserByPk(14).user
        tarifs = PricesService.read_all(user)

        result_data1 = form_data_for_tarif(tarifs[0], self.week)
        result_data2 = form_data_for_tarif(tarifs[1], self.week)
        result_data3 = form_data_for_tarif(tarifs[2], self.week)
        result_data4 = form_data_for_tarif(tarifs[3], self.week)

        self.assertEqual(result_data1, data_for_tarif0_user14)
        self.assertEqual(result_data2, data_for_tarif1_user14)
        self.assertEqual(result_data3, data_for_tarif2_user14)
        self.assertEqual(result_data4, data_for_tarif3_user14)

        self.assertEqual(len(tarifs), 4)
class CheckFormInstructorsSchedule(TestCase):
    fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs',\
    'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',\
    'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json']
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

        datetime_object = datetime.datetime.strptime('May 29 2021', '%b %d %Y')
        my_week_raw = datetime_object.isocalendar()

        self.pass_week = str(my_week_raw[0]) + '-W' + str(my_week_raw[1])
        self.user = UserByPk(18).user

    def test_form_instructors_shedule(self):
        result_data = form_instructors_shedule(self.user, instructor_id=1)

        self.assertEqual(result_data, instructor_schedule_for_user18)

    def test_form_instructors_shedule_for_week(self):
        result_data = form_instructors_shedule_for_week(self.user, 1, self.pass_week)

        self.assertEqual(result_data, instructors_shedule_for_week_for_user18)