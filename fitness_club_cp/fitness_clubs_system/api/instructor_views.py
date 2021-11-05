from rest_framework import generics

from .role import *
from .instructor_schedule import *
from .utils import *
from .week import *

from manager.services import ServicesService, FitnessClubsService, GroupClassesService,\
    GroupClassesSheduleService, InstructorsService, SpecialOffersService, PricesService, \
    GroupClassesCustomersRecordsService, InstructorSheduleCustomersService, \
    AdminRecordsService, InstructorPersonalTrainingsLogsService, CustomUserService, \
    AdminGroupClassesLogsService, CustomersService, InstructorSheduleService

from manager.models import GroupClassesCustomersRecords, InstructorSheduleCustomers, AdminRecords, InstructorShedule

from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse

class InstructorView(APIView):
    """
    get:
        get information for instructor profile
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        fitness_club = FitnessClubsService.read_filtered(request.user, {'club_id': role['user']['club']})
        address = fitness_club[0].city + ", " + fitness_club[0].address
        instructor_shedule = form_instructors_shedule(request.user, role['instructor']['instructor_id'])

        exp_str = "лет"
        if role['instructor']['experience'] % 10 == 1 and role['instructor']['experience'] != 11:
            exp_str = "год"
        elif role['instructor']['experience'] % 10 in [2, 3, 4] and role['instructor']['experience'] not in [12, 13,
                                                                                                             14]:
            exp_str = "года"

        record = AdminRecordsService.read_filtered(request.user, {'instructor': role['instructor']['instructor_id'],
                                                                     'status': AdminRecords.PENDING})
        change_record = None
        is_already_record = False
        if record:
            is_already_record = True
            change_record = record[0]

        data = {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                'exp_str': exp_str,
                'is_already_record': is_already_record,
                'change_record': change_record}
        return Response(data)

class InstructorAttachedCustomersView(APIView):
    """
    get:
        get information for attached customers
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        customers_data = []
        customers = CustomersService.read_filtered(request.user, {'instructor_id': role['instructor']['instructor_id']})
        is_chart = True

        for customer in customers:
            x = customer.measure_dates
            y = customer.measured_weights
            if len(x) == 0:
                is_chart = False
            chart = get_plot(x, y)
            customers_data.append({'name': customer.name,
                                   'surname': customer.surname,
                                   'patronymic': customer.patronymic,
                                   'chart': chart,
                                   'is_chart': is_chart,
                                   'day_of_birth': customer.day_of_birth,
                                   'height': customer.height})

        data = {'role': role, 'customers_data': customers_data}
        return Response(data)

class InstructorEditProfileView(generics.ListCreateAPIView):
    """
    get:
        get information to render page with edit form

    put:
        edit instructor info
        education, achievements, specialization with ;

    """
    allowed_methods = ["PUT", "GET"]
    def get(self, request):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        data = {'role': role}

        return Response(data)

    serializer_class = EditInstructorProfileSerializer
    def put(self, request):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        cleaned_data = request.data
        if type(cleaned_data['education']) == str:
            cleaned_data['education'] = cleaned_data['education'].split(';')
            cleaned_data['achievements'] = cleaned_data['achievements'].split(';')
            cleaned_data['specialization'] = cleaned_data['specialization'].split(';')
        print(cleaned_data)
        InstructorsService.update_by_pk(request.user,
                                      role['instructor']['instructor_id'], cleaned_data)
        return JsonResponse({'status': 'Ok'},
                            status=200)
    

class InstructorAddPersonalTrainingView(generics.ListCreateAPIView):
    """
    post:
        add personal training to instructor's schedule
        day - day of week
        time from 9:00 to 20:00
    """
    allowed_methods = ["POST"]
    serializer_class = InstructorAddPersonalTrainingSerializer
    def post(self, request):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        day = request.data["day"]
        time_raw = request.data["time"]
        time = datetime.datetime.strptime(time_raw, '%H:%M').time()

        flag_rec = InstructorSheduleService.read_filtered(request.user, {"day_of_week": day,
                                                            "instructor_id": role['instructor']['instructor_id'],
                                                                            "training_time": time})
        if len(flag_rec) > 0:
            return JsonResponse({'status': 'false', 'message': 'This time is already busy'},
                                status=405)

        flag_group_classes_rec = GroupClassesSheduleService.read_filtered(request.user,
                                                                {"instructor": role['instructor']['instructor_id'],
                                                                 "class_time": time,
                                                                 "day_of_week": day})

        if len(flag_group_classes_rec) > 0:
            return JsonResponse({'status': 'false', 'message': 'This time is already busy'},
                                status=405)

        new_record = InstructorShedule()

        new_record.instructor_id = role['instructor']['instructor_id']
        new_record.training_time = time
        new_record.day_of_week = day

        InstructorSheduleService.create(request.user, new_record)

        return JsonResponse({'status': 'Ok', 'message': 'You add new personal training'},
                            status=200)

class InstructorDeleteProfileChangesView(APIView):
    """
    delete:
        delete changes in instructor's profile
    """

    def delete(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        pk = kwargs["pk"]
        flag = AdminRecordsService.read_filtered(request.user, {"pk": pk})
        if len(flag) == 0:
            return JsonResponse({'status': 'false', 'message': "This record doesn't exist"},
                                status=405)

        AdminRecordsService.delete_by_pk(request.user, pk)

        return JsonResponse({'status': 'Ok', 'message': 'You delete profile changes'},
                            status=200)

class InstructorDeletePersonalTrainingView(APIView):
    """
    delete:
        delete personal training from schedule
    """

    def delete(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        i_shedule_id = kwargs["i_shedule_id"]
        flag = InstructorSheduleService.read_filtered(request.user, {"i_shedule_id": i_shedule_id})
        if len(flag) == 0:
            return JsonResponse({'status': 'false', 'message': "This record doesn't exist"},
                                status=405)

        InstructorSheduleService.delete_filtered(request.user, {'i_shedule_id': i_shedule_id})

        return JsonResponse({'status': 'Ok', 'message': 'You delete personal training'},
                            status=200)

class InstructorTrainingRecordsView(APIView):
    """
    get:
        get records from customers for week
        format of week 2021-W41 ({year}-W{week num})
    """

    def get(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        week = get_week()
        selected_week = kwargs['week_num']
        if selected_week:
            week = selected_week
        instructor_shedule, day_of_week_date = form_instructors_shedule_for_week(request.user, role['instructor']['instructor_id'], week)
        fitness_club = FitnessClubsService.read_filtered(request.user, {'club_id': role['user']['club']})
        address = fitness_club[0].city + ", " + fitness_club[0].address

        data = {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                       'day_of_week_date': day_of_week_date,
                       'current_week': week}

        return Response(data)