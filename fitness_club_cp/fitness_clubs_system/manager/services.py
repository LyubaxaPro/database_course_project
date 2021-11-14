from .common_repositories import *
from .logs_repositories import *
from .schedule_repositories import *
from .users_repositories import *

class CustomService():

    def __init__(self, repository):
        self.repository = repository

    def create(self, client_user, user):
        self.repository.create(client_user, user)

    def read_by_pk(self, client_user, pk):
        return self.repository.read_by_pk(client_user, pk)

    def read_filtered(self, client_user, filter_dict):
        return self.repository.read_filtered(client_user, filter_dict)

    def read_all(self, client_user):
        return self.repository.read_all(client_user)

    def update_by_pk(self, client_user, pk, update_dict):
        self.repository.update_by_pk(client_user, pk, update_dict)

    def update_filtered(self, client_user, filter_dict, update_dict):
        self.repository.update_filtered(client_user, filter_dict, update_dict)

    def update_all(self, client_user, update_dict):
        self.repository.update_all(client_user, update_dict)

    def delete_by_pk(self, client_user, pk):
        self.repository.delete_by_pk(client_user, pk)

    def delete_filtered(self, client_user, filter_dict):
        self.repository.delete_filtered(client_user, filter_dict)

    def read_join_filtered(self, client_user, join_field, filter_dict):
        return self.repository.read_join_filtered(client_user, join_field, filter_dict)


CustomUserService = CustomService(CustomUserRepository)
CustomersService = CustomService(CustomersRepository)
InstructorsService = CustomService(InstructorsRepository)
AdministratorsService = CustomService(AdministratorsRepository)
AdminRecordsService = CustomService(AdminRecordsRepository)
GroupClassesService = CustomService(GroupClassesRepository)
GroupClassesCustomersRecordsService = CustomService(GroupClassesCustomersRecordsRepository)
GroupClassesSheduleService = CustomService(GroupClassesSheduleRepository)
InstructorSheduleService = CustomService(InstructorSheduleRepository)
InstructorSheduleCustomersService = CustomService(InstructorSheduleCustomersRepository)
PricesService = CustomService(PricesRepository)
ServicesService = CustomService(ServicesRepository)
FitnessClubsService = CustomService(FitnessClubsRepository)
SpecialOffersService = CustomService(SpecialOffersRepository)
InstructorPersonalTrainingsLogsService = CustomService(InstructorPersonalTrainingsLogsRepository)
AdminGroupClassesLogsService = CustomService(AdminGroupClassesLogsRepository)

