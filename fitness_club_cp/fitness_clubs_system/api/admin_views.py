from rest_framework import generics

from .role import *
from .form_classes_data import *
from django.utils import timezone

from manager.services import ServicesService, FitnessClubsService, GroupClassesService, \
    GroupClassesSheduleService, InstructorsService, SpecialOffersService, PricesService, \
    GroupClassesCustomersRecordsService, InstructorSheduleCustomersService, \
    AdminRecordsService, InstructorPersonalTrainingsLogsService, CustomUserService, \
    AdminGroupClassesLogsService, CustomersService, InstructorSheduleService, AdministratorsService

from manager.models import AdminRecords, GroupClassesShedule, SpecialOffers

from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse


class AdminProfileView(APIView):
    """
    get:
        get information for admin profile
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        fitness_club = FitnessClubsService.read_filtered(request.user, {'club_id': role['user']['club']})
        address = fitness_club[0].city + ", " + fitness_club[0].address

        admin = AdministratorsService.read_filtered(request.user, {'user': role['admin']['user']})[0]

        users_instructors = CustomUserService.read_filtered(request.user, {"club": role['user']['club'], 'role': 1})
        user_id_list = []
        for user in users_instructors:
            user_id_list.append(user.id)

        instructors = InstructorsService.read_filtered(request.user, {'user__in': user_id_list, 'is_active': False})

        instructors_data = []
        for instructor in instructors:
            user = CustomUserService.read_filtered(request.user, {'id': instructor.user_id})[0]
            instructors_data.append({'data': instructor, 'user': user})

        changes_instructors = AdminRecordsService.read_filtered(request.user, {'admin': role['admin']['user'],
                                                                                  'status': AdminRecords.PENDING})

        active_instructors = InstructorsService.read_filtered(request.user,
                                                                 {'user__in': user_id_list, 'is_active': True})

        instructor_action_records = InstructorPersonalTrainingsLogsService.read_join_filtered(request.user,
                                                                                                 'instructor',
                                                                                                 {
                                                                                                     'instructor__in': active_instructors})
        instructor_action_logs = []

        for cur in instructor_action_records:
            if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
                instructor_action_logs.append(cur)

        data = {'role': role, 'address': address,
                'admin': admin, 'instructors': instructors_data,
                'changes_instructors': AdminRecordsSerializer(changes_instructors, many=True).data,
                'instructor_action_logs': instructor_action_logs}

        return Response(data)

class AdminGroupClassesView(generics.ListCreateAPIView):
    """
    get:
        get group classes schedule

    post:
        create group class
    """
    allowed_methods = ["GET", "POST"]
    serializer_class = AdminGroupClassesViewSerializer
    def get(self, request):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        week = get_week()
        club_id = role['user']['club']
        classes_data, day_dates = form_admin_classes_data(request.user, club_id, week)

        club_info = FitnessClubsService.read_filtered(request.user, {'club_id': club_id})[0]
        address = club_info.city + ", " + club_info.address

        classes = GroupClassesService.read_all(request.user)

        users = CustomUserService.read_filtered(request.user, {"club": club_id})
        user_id_list = []
        for user in users:
            user_id_list.append(user.id)

        instructors = InstructorsService.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})

        data = {'classes_data': classes_data,
                'classes': GroupClassesSerializer(classes, many=True).data, 'role': role,
                'address': address, 'instructors': InstructorsSerializer(instructors, many=True).data,
                'club_id': club_id}

        return Response(data)

    def post(self, request):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        day = request.data["day"]
        time_raw = request.data["time"]
        time = datetime.datetime.strptime(time_raw, '%H:%M').time()
        club_id = role['user']['club']
        class_id = request.data["class_id"]
        maximum_quantity = request.data["maximum_quantity"]

        flag_class = GroupClassesService.read_filtered(request.user, {'class_id': class_id})
        if len(flag_class) == 0:
            return JsonResponse({'status': 'false', 'message': 'Wrong class_id'}, status=400)

        instructor_id = request.data["instructor_id"]
        instructor = InstructorsService.read_filtered(request.user, {'instructor_id': instructor_id})
        if len(instructor) == 0:
            return JsonResponse({'status': 'false', 'message': 'Wrong instructor_id'}, status=400)

        instructor_club = CustomUserService.read_filtered(request.user, {'email': instructor[0].user})[0].club
        if instructor_club != club_id:
            return JsonResponse({'status': 'false', 'message': "This instructor don't work in this club"}, status=400)

        busy_instructors = GroupClassesSheduleService.read_filtered(request.user, {'class_time': time, 'day_of_week': day})
        for i in busy_instructors:

            if int(instructor_id) == i.instructor.instructor_id:
                return JsonResponse({'status': 'false', 'message': "This instructor already busy"},
                                    status=400)

        new_record = GroupClassesShedule()
        new_record.class_field = GroupClassesService.read_filtered(request.user, {'class_id': class_id})[0]
        new_record.club = FitnessClubsService.read_filtered(request.user, {'club_id': club_id})[0]
        new_record.instructor = InstructorsService.read_filtered(request.user, {'instructor_id': instructor_id})[0]
        new_record.class_time = time
        new_record.day_of_week = day
        new_record.maximum_quantity = int(maximum_quantity)

        GroupClassesSheduleService.create(request.user, new_record)

        return JsonResponse({'status': 'Ok', 'message': 'You add new group training'},
                            status=200)


class AdminDeleteGroupClassesView(APIView):
    """
    delete:
        delete group class
    """

    def delete(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        shedule_id = kwargs["shedule_id"]
        flag = GroupClassesSheduleService.read_filtered(request.user, {'shedule_id': shedule_id})
        if len(flag) == 0:
            return JsonResponse({'status': 'false', 'message': "Don't have this record"},
                                status=400)

        GroupClassesSheduleService.delete_filtered(request.user, {'shedule_id': shedule_id})

        return JsonResponse({'status': 'Ok', 'message': 'You delete group training'},
                            status=200)


class AdminDeleteSpecialOfferView(APIView):
    """
    delete:
        delete special offer
    """

    def delete(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        offer_id = kwargs["offer_id"]
        flag = SpecialOffersService.read_filtered(request.user, {'offer_id': offer_id})
        if len(flag) == 0:
            return JsonResponse({'status': 'false', 'message': "Don't have this record"},
                                status=400)
        SpecialOffersService.delete_filtered(request.user, {'offer_id': offer_id})

        return JsonResponse({'status': 'Ok', 'message': 'You delete special offer'},
                            status=200)

class AdminAdminSpecialOfferView(generics.ListCreateAPIView):
    """
    post:
        create special offer
    """
    allowed_methods = ["POST"]
    serializer_class = AdminSpecialOfferSerializer
    def post(self, request):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        offer_name = request.data["offer_name"]
        offer_description = request.data["offer_description"]

        new_record = SpecialOffers()
        new_record.offer_name = offer_name
        new_record.offer_description = offer_description

        SpecialOffersService.create(request.user, new_record)

        return JsonResponse({'status': 'Ok', 'message': 'You create special offer'},
                            status=200)

class AdminStatisticsView(APIView):
    """
    get:
        get trainings statistics
        week_num format 2021-W30
    """

    def get(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        week = get_week()
        selected_week = kwargs['week_num']
        if selected_week:
            week = selected_week

        role = get_role_json(request)
        club_id = role['user']['club']
        classes_data, day_of_week_date = form_admin_classes_data(request.user, club_id, week)

        club_info = FitnessClubsService.read_filtered(request.user, {'club_id': club_id})[0]
        address = club_info.city + ", " + club_info.address

        classes = GroupClassesService.read_all(request.user)

        users = CustomUserService.read_filtered(request.user, {"club": club_id})
        user_id_list = []
        for user in users:
            user_id_list.append(user.id)

        data = {'classes_data': classes_data,
                'classes': GroupClassesSerializer(classes, many=True).data, 'role': role,
                'address': address,
                'club_id': club_id,
                'day_of_week_date': day_of_week_date,
                'current_week': week}
        return Response(data)

class AdminActivateInstructorView(generics.ListCreateAPIView):
    """
    patch:
        activate new instructor
    """
    allowed_methods = ["PATCH"]
    serializer_class = AdminActivateInstructorsSerializer
    def patch(self, request):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)

        instructor_id = request.data["instructor_id"]
        InstructorsService.update_filtered(request.user, {'instructor_id': instructor_id}, {'is_active': True})

        return JsonResponse({'status': 'Ok', 'message': 'You activate new instructor'},
                            status=200)


class AdminRejectInstructorView(APIView):
    """
    delete:
        reject new instructor
    """

    def delete(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_admin']:
            return JsonResponse({'status': 'false', 'message': 'You do not have rights to get the information'},
                                status=403)
        user_id = kwargs["user_id"]
        flag = InstructorsService.read_filtered(request.user, {"user": user_id, "is_active": False})
        if len(flag) == 0:
            return JsonResponse({'status': 'false', 'message': 'Wrong id'},
                                status=400)

        CustomUserService.delete_filtered(request.user, {'id': user_id})

        return JsonResponse({'status': 'Ok', 'message': 'You delete new instructor'},
                            status=200)
