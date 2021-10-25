from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, SpecialOffersRepository, PricesRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, CustomUserRepository
from rest_framework.response import Response
from rest_framework.views import APIView
from .role import *
from .form_classes_data import *
from .instructor_schedule import *

class IndexView(APIView):
    """
    get:
        Return home page info
    """
    def get(self, request):
        data = {
            'title': 'Главная страница',
            'role': get_role_json(request)
        }
        return Response(data)

class AddressView(APIView):
    """
    get:
        Return address of clubs
    """
    def get(self, request):
        clubs = FitnessClubsRepository()
        data = {
            'clubs': FitnessClubsSerializer(clubs.read_all(request.user), many=True).data,
            'role': get_role_json(request)
        }
        return Response(data)

class ServicesView(APIView):
    """
    get:
        Return list of services of clubs
    """
    def get(self, request):
        data = {
            'services':  ServicesSerializer(ServicesRepository.read_all(request.user), many=True).data,
            'role': get_role_json(request)
        }
        return Response(data)

class ClubGroupClassesView(APIView):
    """
    get:
        get classes data for club with club_id = 1
    """
    def get(self, request):
        classes_data = form_classes_data(request.user, 1)
        classes = GroupClassesRepository.read_all(request.user)
        data = {'classes_data': classes_data,
                'classes': GroupClassesSerializer(classes, many=True).data, 'role': get_role_json(request)}
        return Response(data)

class ClubGroupClassesScheduleForClubView(APIView):
    """
    get:
        get classes data for club with club_id
    """
    def get(self, request, *args, **kwargs):
        club_id = kwargs['club_id']
        classes_data = form_classes_data(request.user, club_id)
        return Response(classes_data)

class ClubInstructorsView(APIView):
    """
    get:
        get list of club instrutors
    """

    def get(self, request):
        instructors = InstructorsRepository.read_filtered(request.user, {'is_active': True})
        data = {'instructors': InstructorsSerializer(instructors, many=True).data, 'role': get_role_json(request)}
        return Response(data)

class ClubInstructorsForClubView(APIView):
    """
    get:
        get list of instrutors for club with club_id
    """

    def get(self, request, *args, **kwargs):
        club_id = kwargs['club_id']
        users = CustomUserRepository.read_filtered(request.user, {"club": club_id})
        user_id_list = []
        for user in users:
            user_id_list.append(user.id)
        instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})
        data = {'filtered_instructors': InstructorsSerializer(instructors, many=True).data}
        return Response(data)


class ClubInstructorsDetailView(APIView):
    """
    get:
        get detail information about instructor
    """

    def get(self, request, *args, **kwargs):
        """Информация об инструкторе"""
        pk = kwargs['pk']
        instructor = InstructorsRepository.read_by_pk(request.user, pk)
        instructor_shedule = form_instructors_shedule(request.user, instructor.instructor_id)

        exp_str = "лет"
        if instructor.experience % 10 == 1 and instructor.experience != 11:
            exp_str = "год"
        elif instructor.experience % 10 in [2, 3, 4] and instructor.experience not in [12, 13, 14]:
            exp_str = "года"

        user = CustomUserRepository.read_filtered(request.user, {'id': instructor.user_id})

        fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': user[0].club})
        address = fitness_club[0].city + ", " + fitness_club[0].address

        data = {'instructor': InstructorsSerializer(instructor).data,
                'exp_str': exp_str,
                'role': get_role_json(request),
                'shedule': instructor_shedule,
                'address': address}
        return Response(data)

class PricesView(APIView):
    """
    get:
        get prices and special offers
    """

    def get(self, request):
        special_offers = SpecialOffersRepository.read_all(request.user)
        prices = PricesRepository.read_all(request.user)
        role = get_role_json(request)

        data = {'special_offers': SpecialOffersSerializer(special_offers, many=True).data,
                'prices': PricesSerializer(prices, many=True).data, 'role': role}
        return Response(data)






