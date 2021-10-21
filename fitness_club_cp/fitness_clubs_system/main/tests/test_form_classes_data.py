from django.test import TestCase, RequestFactory, Client
from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository,\
    AdministratorsRepository, AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, AdminGroupClassesLogsRepository
from fitness_clubs_system.main.dataBuilder import *
from fitness_clubs_system.main.view_funcs.form_classes_data import *
from fitness_clubs_system.main.view_funcs.instructor_schedule import *
from fitness_clubs_system.main.data.data_for_tests import *

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

        response = form_classes_data(user, 1)

        self.assertEqual(response, classes_data_for_user_14)

    def test_form_admin_classes_data(self):
        user = SuperUser().user

        response = form_admin_classes_data(user, 1, self.week)

        self.assertEqual(response, admin_classes_data_for_superuser)

    def test_form_data_for_tarif(self):
        user = UserByPk(14).user
        tarifs = PricesRepository.read_all(user)

        response1 = form_data_for_tarif(tarifs[0], self.week)
        response2 = form_data_for_tarif(tarifs[1], self.week)
        response3 = form_data_for_tarif(tarifs[2], self.week)
        response4 = form_data_for_tarif(tarifs[3], self.week)

        self.assertEqual(response1, data_for_tarif0_user14)
        self.assertEqual(response2, data_for_tarif1_user14)
        self.assertEqual(response3, data_for_tarif2_user14)
        self.assertEqual(response4, data_for_tarif3_user14)

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
        response = form_instructors_shedule(self.user, instructor_id=1)

        self.assertEqual(response, instructor_schedule_for_user18)

    def test_form_instructors_shedule_for_week(self):
        response = form_instructors_shedule_for_week(self.user, 1, self.pass_week)

        self.assertEqual(response, instructors_shedule_for_week_for_user18)