from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository,\
    AdministratorsRepository, AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, AdminGroupClassesLogsRepository

from .role import *
from .form_classes_data import *
from .instructor_schedule import *
def prices_f(request):
    special_offers = SpecialOffersRepository.read_all(request.user)
    prices = PricesRepository.read_all(request.user)
    return {'special_offers': special_offers, 'prices': prices}

def index_func(request):
    data = {
        'title': 'Главная страница',
        'role': get_role_json(request)
    }
    return  data

def address_func(request):
    clubs = FitnessClubsRepository()
    data = {
        'clubs' : clubs.read_all(request.user),
        'role': get_role_json(request)
    }
    return data

def services_func(request):
    services = ServicesRepository()
    data = {
        'services': services.read_all(request.user),
        'role': get_role_json(request)
    }
    return data

def instructor_detail_func(request, pk):
    """Информация об инструкторе"""
    instructor =  InstructorsRepository.read_by_pk(request.user, pk)
    instructor_shedule = form_instructors_shedule(request.user, instructor.instructor_id)

    exp_str = "лет"
    if instructor.experience % 10 == 1 and instructor.experience != 11:
        exp_str = "год"
    elif instructor.experience % 10 in [2, 3, 4] and instructor.experience not in [12, 13, 14]:
        exp_str = "года"

    user = CustomUserRepository.read_filtered(request.user, {'id': instructor.user_id})

    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': user[0].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address

    return {'instructor' : instructor,
            'exp_str' : exp_str,
           'role': get_role_json(request),
           'shedule': instructor_shedule,
           'address': address}

def prices_func(request):
    special_offers = SpecialOffersRepository.read_all(request.user)
    prices = PricesRepository.read_all(request.user)
    role = get_role_json(request)

    return {'special_offers': special_offers, 'prices': prices,
                                                'role': role}
