from manager.services import CustomersService, CustomUserService, PricesService, InstructorsService, AdministratorsService
from django.test import TestCase
from .dataBuilder import *
from django.contrib.auth.models import AnonymousUser
from unittest.mock import MagicMock


class TestUserAndCustomer(TestCase):
    def test_create_user_and_customer(self):
        user = UserWithInfoBuilder().build(1, "aaa@mail.ru", "AAAA", 0)
        tarif = PricesBuilder().build()
        customer = CustomerBuilder().build(user, tarif, None)

        CustomUserService.create(AnonymousUser, user)
        PricesService.create(user, tarif)
        CustomersService.create(user, customer)
        created_user = CustomUserService.read_by_pk(user, user.pk)
        created_tarif = PricesService.read_by_pk(user, tarif.pk)
        created_customer = CustomersService.read_by_pk(user, customer.pk)

        self.assertEqual(created_user, user)
        self.assertEqual(created_tarif, tarif)
        self.assertEqual(created_customer, customer)

    def test_create_user_and_customer_with_instructor(self):
        user_customer = UserWithInfoBuilder().build(1, "aaa@mail.ru", "AAAA", 0)
        user_instructor = UserWithInfoBuilder().build(2, "aaa1@mail.ru", "BBBB", 1)
        user_admin = UserWithInfoBuilder().build(3, "aaa2@mail.ru", "CCCC", 2)
        tarif = PricesBuilder().build()
        admin = AdminBuilder().build(user_admin)
        instructor = InstructorBuilder().build(user_instructor, admin)
        customer = CustomerBuilder().build(user_customer, tarif, instructor)

        CustomUserService.create(AnonymousUser, user_customer)
        CustomUserService.create(AnonymousUser, user_instructor)
        CustomUserService.create(AnonymousUser, user_admin)
        PricesService.create(user_admin, tarif)
        AdministratorsService.create(user_admin, admin)
        InstructorsService.create(user_instructor, instructor)
        CustomersService.create(user_customer, customer)
        created_customer_user = CustomUserService.read_by_pk(user_customer, user_customer.pk)
        created_instructor_user = CustomUserService.read_by_pk(user_instructor, user_instructor.pk)
        created_admin_user = CustomUserService.read_by_pk(user_admin, user_admin.pk)
        created_tarif = PricesService.read_by_pk(user_admin, tarif.pk)
        created_customer = CustomersService.read_by_pk(user_customer, customer.pk)
        created_istructor = InstructorsService.read_by_pk(user_instructor, instructor.pk)
        created_admin = AdministratorsService.read_by_pk(user_admin, admin.pk)

        self.assertEqual(created_customer_user, user_customer)
        self.assertEqual(created_instructor_user, user_instructor)
        self.assertEqual(created_admin_user, user_admin)
        self.assertEqual(created_tarif, tarif)
        self.assertEqual(created_customer, customer)
        self.assertEqual(created_admin, admin)
        self.assertEqual(created_istructor, instructor)

class TestUserAndCustomerMock(TestCase):
    def setUp(self):
        self.customUserBuilder = UserWithInfoBuilder()
        self.customUserBuilder.build = MagicMock(return_value=get_data_for_user_mock(1, "aaa@mail.ru", "AAAA", 0))

        self.instructorUserBuilder = UserWithInfoBuilder()
        self.instructorUserBuilder.build = MagicMock(return_value=get_data_for_user_mock(2, "aaa1@mail.ru", "BBBB", 1))

        self.adminUserBuilder = UserWithInfoBuilder()
        self.adminUserBuilder.build = MagicMock(return_value=get_data_for_user_mock(3, "aaa2@mail.ru", "CCCC", 2))

        self.tarifBuilder = PricesBuilder()
        self.tarifBuilder.build = MagicMock(return_value=get_data_for_prices_mock())

    def test_create_user_and_customer_mock(self):
        user = self.customUserBuilder.build()
        tarif = PricesBuilder().build()
        customer = CustomerBuilder().build(user, tarif, None)

        PricesService.create(user, tarif)
        CustomersService.create(user, customer)
        created_tarif = PricesService.read_by_pk(user, tarif.pk)
        created_customer = CustomersService.read_by_pk(user, customer.pk)

        self.assertEqual(created_tarif, tarif)
        self.assertEqual(created_customer, customer)

    def test_create_user_and_customer_with_instructor(self):
        user_customer = self.customUserBuilder.build()
        user_instructor = self.instructorUserBuilder.build()
        user_admin = self.adminUserBuilder.build()
        tarif = self.tarifBuilder.build()
        admin = AdminBuilder().build(user_admin)
        instructor = InstructorBuilder().build(user_instructor, admin)
        customer = CustomerBuilder().build(user_customer, tarif, instructor)

        PricesService.create(user_admin, tarif)
        AdministratorsService.create(user_admin, admin)
        InstructorsService.create(user_instructor, instructor)
        CustomersService.create(user_customer, customer)
        created_customer = CustomersService.read_by_pk(user_customer, customer.pk)
        created_istructor = InstructorsService.read_by_pk(user_instructor, instructor.pk)
        created_admin = AdministratorsService.read_by_pk(user_admin, admin.pk)

        self.assertEqual(created_customer, customer)
        self.assertEqual(created_admin, admin)
        self.assertEqual(created_istructor, instructor)
