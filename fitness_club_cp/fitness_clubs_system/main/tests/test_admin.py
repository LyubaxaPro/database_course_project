# from manager.repositories import GroupClassesSheduleRepository, SpecialOffersRepository, AdministratorsRepository
# from django.test import TestCase, RequestFactory, Client
# from http import HTTPStatus
# from fitness_clubs_system.main.dataBuilder import *
#
#
# class TestAdmin(TestCase):
#     fixtures = ['groupClassesShedule.json', 'instructors.json', 'groupclasses.json', 'fitness_clubs', \
#     'myCustomUsers.json', 'administrators', 'prices.json', 'customers', 'fitness_clubs',\
#     'groupClassesCustomersRecords.json', 'instructorShedule.json', 'instructorSheduleCustomers.json', 'specialOffers.json']
#     def setUp(self):
#         self.c = Client()
#         self.factory = RequestFactory()
#         self.maxDiff = None
#
#     def test_admin_profile_url_status_code(self):
#         user = SuperUser().user
#         request = self.factory.get('/admin_profile/')
#         request.user = user
#
#         response = admin_profile(request)
#
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#
#     def test_admin_profile_func_data(self):
#         user = SuperUser().user
#         request = self.factory.get('/admin_profile/')
#         request.user = user
#         admin = AdministratorsRepository.read_filtered(user, {'user': user.id})
#
#         response = admin_profile_func(request)
#
#         self.assertEqual(len(admin), 1)
#         self.assertEqual(response['role'], {'is_customer': False, 'customer': None, 'is_instructor': False,
#                             'instructor': None, 'is_admin': True, 'admin': admin[0], 'is_guest': False, 'user': user})
#         self.assertEqual(response['address'], 'Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)')
#
#     def test_delete_group_class_in_shedule(self):
#         user = SuperUser().user
#         prev_qs = GroupClassesSheduleRepository.read_all(user)
#         request = self.factory.get('/delete_group_class_in_shedule/?shedule_id=1')
#         request.user = user
#
#         delete_group_class_in_shedule(request)
#
#         self.assertNotEqual(prev_qs, GroupClassesSheduleRepository.read_all(user))
#
#     def test_delete_special_offer_by_admin(self):
#         user = SuperUser().user
#         prev_qs = SpecialOffersRepository.read_all(user)
#         request = self.factory.get('/delete_special_offer_by_admin/?offer_id=1')
#         request.user = user
#
#         delete_special_offer_by_admin(request)
#
#         self.assertNotEqual(prev_qs, SpecialOffersRepository.read_all(user))
#
#     def test_add_special_offer_by_admin(self):
#         user = SuperUser().user
#         request = self.factory.get('/add_special_offer_by_admin/?offer_name=Super offer!&offer_description=fffff')
#         request.user = user
#
#         add_special_offer_by_admin(request)
#
#         self.assertNotEqual(None, SpecialOffersRepository.read_filtered(user, {'offer_name' : 'Super offer!',
#                                                                                'offer_description' : 'fffff'}))