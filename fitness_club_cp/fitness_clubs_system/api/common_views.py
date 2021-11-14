import jwt
from django.conf import settings
from django.http import JsonResponse
from manager.services import CustomUserService, CustomersService, InstructorsService, AdministratorsService,\
AdminRecordsService, GroupClassesService, GroupClassesCustomersRecordsService, GroupClassesSheduleService\
    ,InstructorSheduleService, InstructorSheduleCustomersService, PricesService, ServicesService, FitnessClubsService,\
    SpecialOffersService, InstructorPersonalTrainingsLogsService, AdminGroupClassesLogsService
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from .role import *
from .form_classes_data import *
from .instructor_schedule import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login, user_logged_in


class CreateUserApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = CreateUserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AuthUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            print(request.user)
            user_qs = CustomUserService.read_filtered(request.user, {'email': email, 'password': password})
            print(user_qs)
            if user_qs:
                try:
                    user = user_qs[0]
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['email'] = "%s" % (user.email)
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
                except Exception as e:
                    raise e
            else:
                res = {'error': 'can not authenticate with given credentials'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and password'}
            return Response(res)

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

class AddressInfoView(APIView):
    """
    get:
        Return address of clubs
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUserSerializer
    def get(self, request):
        data = {
            'clubs': FitnessClubsSerializer(FitnessClubsService.read_all(request.user), many=True).data,
        }
        return Response(data)

class ServicesInfoView(APIView):
    """
    get:
        Return list of services of clubs
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUserSerializer
    def get(self, request):
        data = {
            'services':  ServicesSerializer(ServicesService.read_all(request.user), many=True).data,
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

