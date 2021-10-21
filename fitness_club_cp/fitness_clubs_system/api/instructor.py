from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository,\
    AdministratorsRepository, AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, AdminGroupClassesLogsRepository
from manager.models import Instructors, GroupClassesCustomersRecords, InstructorSheduleCustomers, InstructorShedule,\
    GroupClassesShedule, SpecialOffers, AdminRecords
from .role import *
from .instructor_schedule import *

def instructor_training_records_func(request):
    role = get_role_json(request)
    week = get_week()
    selected_week = request.GET.get('week_num')
    if selected_week:
        week = selected_week
    instructor_shedule, day_of_week_date = form_instructors_shedule_for_week(request.user, role['instructor']['instructor_id'], week)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user']['club']})
    address = fitness_club[0].city + ", " + fitness_club[0].address


    return {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                   'day_of_week_date': day_of_week_date,
                   'current_week': week}