from django.test import TestCase
from .models import Customers, Instructors
from .repositories import *
from users.models import CustomUser

class test_CRUD(TestCase):

    client_user = CustomUser(role=CustomUser.SUPERUSER)
    databases = frozenset({'default', 'superuser_role_connect'})

    @staticmethod
    def test_Customer():
        user = CustomUser(
            email = "1234@mail.ru",
            password = "secure_password",
            role = 0,
            club = 1,
            login = "1234qwerty"
        )

        customer = Customers(
            customer_id = 1,
            sex = "man",
            name = "Григорий",
            surname = "Владимирский",
            patronymic = "Антонович",
            day_of_birth = "1989-05-23",
            tariff_end_date = "2021-08-14",
            user = user
        )

        CustomersRepository.create(test_CRUD.client_user, customer)


        db_customer = CustomersRepository.read_by_pk(
            test_CRUD.client_user, 1)

        assert(db_customer.customer_id == 1)
        assert(db_customer.sex == "man")
        assert(db_customer.name == "Григорий")
        assert(db_customer.surname == "Владимирский")
        assert(db_customer.patronymic == "Антонович")
        assert(str(db_customer.day_of_birth) == "1989-05-23")
        assert(str(db_customer.tariff_end_date) == "2021-08-14")
        assert(db_customer.user_id == 1)

        CustomersRepository.update_by_pk(test_CRUD.client_user, 1, {'name': "Валентин", 'surname' : "Ежов"})
        db_customer = CustomersRepository.read_by_pk(test_CRUD.client_user, 1)

        assert(db_customer.name == "Валентин")
        assert(db_customer.surname == "Ежов")

        CustomersRepository.delete_by_pk(test_CRUD.client_user, 1)
        delete_flag = 0
        try:
            CustomersRepository.read_by_pk(test_CRUD.client_user, 1)
        except:
            delete_flag = 1
        assert(delete_flag == 1)

    @staticmethod
    def test_Instructors():
        user = CustomUser(
            email="12345@mail.ru",
            password="secure_password",
            role=1,
            club=1,
            login="12345qwerty"
        )

        instructor = Instructors(
            instructor_id = 1,
            user = user,
            sex = "woman",
            name = "Елизавета",
            surname = "Потапова",
            patronymic = "Николаевна",
            education = "{'КемГУ'}",
            experience = 20,
            achievements = {"МС по синхронному плаванию","Презентер российских конвенций по направлениям step и aero","Мастер спорта по дзюдо"},
            specialization = {"Подготовка к соревнованиям","Восстановление после травм и операций","Функциональный тренинг"}
        )

        InstructorsRepository.create(test_CRUD.client_user, instructor)

        db_instructor = InstructorsRepository.read_by_pk(
            test_CRUD.client_user, 1)

        assert(db_instructor.instructor_id == 1)
        assert(db_instructor.user == user)
        assert(db_instructor.sex == "woman")
        assert(db_instructor.name == "Елизавета")
        assert(db_instructor.surname == "Потапова")
        assert(db_instructor.patronymic == "Николаевна")
        assert(db_instructor.education == "{'КемГУ'}")
        assert(db_instructor.experience == 20)
        assert(str(db_instructor.achievements) == str({"МС по синхронному плаванию","Презентер российских конвенций по направлениям step и aero", "Мастер спорта по дзюдо"}))
        assert(str(db_instructor.specialization) == str({"Подготовка к соревнованиям", "Восстановление после травм и операций", "Функциональный тренинг"}))

        InstructorsRepository.update_by_pk(test_CRUD.client_user, 1, {'name': "Валентина", 'surname': "Ежова"})
        db_instructor = InstructorsRepository.read_by_pk(test_CRUD.client_user, 1)

        assert (db_instructor.name == "Валентина")
        assert (db_instructor.surname == "Ежова")

        InstructorsRepository.delete_by_pk(test_CRUD.client_user, 1)
        delete_flag = 0
        try:
            InstructorsRepository.read_by_pk(test_CRUD.client_user, 1)
        except:
            delete_flag = 1

        assert (delete_flag == 1)




