from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository,\
    AdministratorsRepository, AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, AdminGroupClassesLogsRepository
from users.models import CustomUser

class UserBuilder:
    def __init__(self):
        self.customuser = CustomUser(
            pk=1,
            email="l1234@mail.ru",
            password="secure_password",
            role=3,
            club=1,
            login="LyubaxaPro"
        )
        self.user = None
        self.get_user()

    def get_user(self):
        raise NotImplementedError

class SuperUser(UserBuilder):
    def get_user(self):
        user = CustomUserRepository.read_filtered(self.customuser, {'role' : 3})
        if len(user) > 0:
            self.user = user[0]

class CustomerUser(UserBuilder):
    def get_user(self):
        user = CustomUserRepository.read_filtered(self.customuser, {'role' : 0})
        if len(user) > 0:
            self.user = user[0]

class AdminUser(UserBuilder):
    def get_user(self):
        user = CustomUserRepository.read_filtered(self.customuser, {'role' : 2})
        if len(user) > 0:
            self.user = user[0]

class InstructorUser(UserBuilder):
    def get_user(self):
        user = CustomUserRepository.read_filtered(self.customuser, {'role' : 1})
        if len(user) > 0:
            self.user = user[0]

class UserBuilderByPk:
    def __init__(self, pk):
        self.customuser = CustomUser(
            pk=1,
            email="l1234@mail.ru",
            password="secure_password",
            role=3,
            club=1,
            login="LyubaxaPro"
        )
        self.user = None
        self.pk = pk
        self.get_user()

    def get_user(self):
        raise NotImplementedError

class UserByPk(UserBuilderByPk):
    def get_user(self):
        self.user = CustomUserRepository.read_by_pk(self.customuser, self.pk)



