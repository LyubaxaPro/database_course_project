from django.http import JsonResponse
from manager.services import CustomUserService, CustomersService, InstructorsService, AdministratorsService,\
AdminRecordsService, GroupClassesService, GroupClassesCustomersRecordsService, GroupClassesSheduleService\
    ,InstructorSheduleService, InstructorSheduleCustomersService, PricesService, ServicesService, FitnessClubsService,\
    SpecialOffersService, InstructorPersonalTrainingsLogsService, AdminGroupClassesLogsService

from rest_framework.response import Response
from rest_framework.views import APIView
from .role import *
from .form_classes_data import *
from .instructor_schedule import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login

class AuthAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer

    def post(self, request):
        user = request.data.get('user', {})
        #
        # email = request.POST['email']
        # password = request.POST['password']
        #
        # # authenticate user then login
        # user = authenticate(email=email, password=password)
        # login(request, user)

        # # Паттерн создания сериализатора, валидации и сохранения - довольно
        # # стандартный, и его можно часто увидеть в реальных проектах.
        print("AAAAAAAAAAAA")
        serializer = self.serializer_class(data=user)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        print("AAA")
        serializer.save()
        print(serializer.data['email'])
        #
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'status': 'Ok', 'message': 'Ok'},
                            status=200)

class IndexView(APIView):
    """
    get:
        Return home page info
    """

    # permission_classes = (IsAuthenticated)
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
        data = {
            'clubs': FitnessClubsSerializer(FitnessClubsService.read_all(request.user), many=True).data,
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
            'services':  ServicesSerializer(ServicesService.read_all(request.user), many=True).data,
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
        classes = GroupClassesService.read_all(request.user)
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
        instructors = InstructorsService.read_filtered(request.user, {'is_active': True})
        data = {'instructors': InstructorsSerializer(instructors, many=True).data, 'role': get_role_json(request)}
        return Response(data)

class ClubInstructorsForClubView(APIView):
    """
    get:
        get list of instrutors for club with club_id
    """

    def get(self, request, *args, **kwargs):
        club_id = kwargs['club_id']
        users = CustomUserService.read_filtered(request.user, {"club": club_id})
        user_id_list = []
        for user in users:
            user_id_list.append(user.id)
        instructors = InstructorsService.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})
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
        instructor = InstructorsService.read_by_pk(request.user, pk)
        instructor_shedule = form_instructors_shedule(request.user, instructor.instructor_id)

        exp_str = "лет"
        if instructor.experience % 10 == 1 and instructor.experience != 11:
            exp_str = "год"
        elif instructor.experience % 10 in [2, 3, 4] and instructor.experience not in [12, 13, 14]:
            exp_str = "года"

        user = CustomUserService.read_filtered(request.user, {'id': instructor.user_id})

        fitness_club = FitnessClubsService.read_filtered(request.user, {'club_id': user[0].club})
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
        special_offers = SpecialOffersService.read_all(request.user)
        prices = PricesService.read_all(request.user)
        role = get_role_json(request)

        data = {'special_offers': SpecialOffersSerializer(special_offers, many=True).data,
                'prices': PricesSerializer(prices, many=True).data, 'role': role}
        return Response(data)

def prices_f(request):
    special_offers = SpecialOffersService.read_all(request.user)
    prices = PricesService.read_all(request.user)
    return {'special_offers': special_offers, 'prices': prices}

def get_qs_role(request):
    customer = None
    is_customer = False
    instructor = None
    is_instructor = False
    is_admin = False
    admin = None
    is_guest = True
    user = None

    if request.user.pk:
        user = CustomUserService.read_filtered(request.user, {'email': CustomUserService.read_by_pk(request.user, request.user.pk)})[0]
        if user.role == 0:
            customer = CustomersService.read_filtered(request.user, {'user_id': request.user.pk})[0]
            is_customer = True
            is_guest = False
        elif user.role == 1:
            instructor = InstructorsService.read_filtered(request.user, {'user_id': request.user.pk})[0]
            is_instructor = True
            is_guest = False
        elif user.role == 2 or user.role == 3:
            is_admin = True
            admin = AdministratorsService.read_filtered(request.user, {'user': request.user.pk})[0]
            is_guest = False

    return is_customer, customer, is_instructor,\
           instructor, is_admin,\
           admin, is_guest, \
           user




