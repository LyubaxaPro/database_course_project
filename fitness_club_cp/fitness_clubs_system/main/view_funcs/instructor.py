from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository,\
    AdministratorsRepository, AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, AdminGroupClassesLogsRepository
from manager.models import Instructors, GroupClassesCustomersRecords, InstructorSheduleCustomers, InstructorShedule,\
    GroupClassesShedule, SpecialOffers, AdminRecords
from .role import *
from .instructor_schedule import *

def instructor_profile_func(request):
    """Профиль инструктора"""
    role = get_role_json(request)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user'].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address
    instructor_shedule = form_instructors_shedule(request.user, role['instructor'].instructor_id)

    exp_str = "лет"
    if role['instructor'].experience % 10 == 1 and role['instructor'].experience != 11:
        exp_str = "год"
    elif role['instructor'].experience % 10 in [2, 3, 4] and role['instructor'].experience not in [12, 13, 14]:
        exp_str = "года"

    record = AdminRecordsRepository.read_filtered(request.user, {'instructor': role['instructor'],
                                                                 'status': AdminRecords.PENDING})
    change_record = None
    is_already_record = False
    if record:
        is_already_record = True
        change_record = record[0]

    return {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                   'exp_str': exp_str,
                   'is_already_record': is_already_record,
                   'change_record': change_record}

def instructor_training_records_func(request):
    role = get_role_json(request)
    week = get_week()
    selected_week = request.GET.get('week_num')
    if selected_week:
        week = selected_week
    instructor_shedule, day_of_week_date = form_instructors_shedule_for_week(request.user, role['instructor'].instructor_id, week)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user'].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address


    return {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                   'day_of_week_date': day_of_week_date,
                   'current_week': week}