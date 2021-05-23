# class test_CRUD(TestCase):
#     databases = frozenset({'default', 'superuser_role_connect'})
#     client_user = CustomUser(role=CustomUser.SUPERUSER)
#
#     def test(self):
#         print(self.databases)
#         print(DBConfigManager().get_connection(self.client_user))
#
#     @staticmethod
#     def test_CRUD_user_OK_case():
#         instructor = Instructors(
#             instructor_id = 1,
#             user_id = 9,
#             sex = "woman",
#             name = "Елизавета",
#             surname = "Потапова",
#             patronymic = "Николаевна",
#             education = {'КемГУ'},
#             experience = 20,
#             achivments = {"'МС по синхронному плаванию'","'Презентер российских конвенций по направлениям step и aero'","'Мастер спорта по дзюдо'"},
#             specialization = {"'Подготовка к соревнованиям'","'Восстановление после травм и операций'","'Функциональный тренинг'"}
#         )
#
#         InstructorsRepository.create(test_CRUD.client_user, instructor)
#
#         read_instructor = InstructorsRepository.read_bypk(
#             test_CRUD.client_user, instructor)
#         assert (read_instructor.instructor_id == 1)
#         assert (read_instructor.user_id == 9)
#         assert (read_instructor.sex == "woman")
#         assert (read_instructor.name == "Елизавета")
#         assert (read_instructor.surname == "Потапова")
#         assert (read_instructor.patronymic == "Николаевна")
#         assert (read_instructor. education == {'КемГУ'})
#         assert (read_instructor.experience == 20)
#         assert (read_instructor.achivments == {"'МС по синхронному плаванию'","'Презентер российских конвенций по направлениям step и aero'","'Мастер спорта по дзюдо'"})
#         assert (read_instructor.specialization == {"'Подготовка к соревнованиям'","'Восстановление после травм и операций'","'Функциональный тренинг'"})