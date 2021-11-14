from gunicorn.http import body
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.schemas import AutoSchema, coreapi

from .role import *
from .form_classes_data import *
from .instructor_schedule import *
from .utils import *
from .week import *
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from manager.services import ServicesService, FitnessClubsService, GroupClassesService,\
    GroupClassesSheduleService, InstructorsService, SpecialOffersService, PricesService, \
    GroupClassesCustomersRecordsService, InstructorSheduleCustomersService, \
    AdminRecordsService, InstructorPersonalTrainingsLogsService, CustomUserService, \
    AdminGroupClassesLogsService, CustomersService, InstructorSheduleService

from manager.models import GroupClassesCustomersRecords, InstructorSheduleCustomers
class CustomerProfileView(APIView):
    """
    get:
        get information for customer profile
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        role = get_role_json(request)
        is_chart = True

        x = role['customer']['measure_dates']
        y = role['customer']['measured_weights']
        if len(x) == 0:
            is_chart = False

        chart = get_plot(x, y)

        today = datetime.datetime.today().strftime('%Y-%m-%d')

        instructor_action_logs = []
        have_instructor = False
        if role['customer']['instructor']:
            have_instructor = True
            instructor_action_records = InstructorPersonalTrainingsLogsService.read_join_filtered(request.user,
                                                                                                      'instructor',
                                                                         {'instructor': role['customer']['instructor']})

            for cur in instructor_action_records:
                if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
                    instructor_action_logs.append(cur)

        group_classes_logs = []
        admin_action_records = AdminGroupClassesLogsService.read_join_filtered(request.user, 'group_class',
                                                                             {'club': role['user']['club']})
        for cur in admin_action_records:
            if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
                group_classes_logs.append(cur)

        tariff = PricesService.read_by_pk(request.user, role['customer']['tariff'])
        data = {'role': get_role_json(request), 'chart': chart,
                                                              'tariff': PricesSerializer(tariff).data,
                                                              'today': today,
                                                              'is_chart': is_chart,
                                                              'instructor_action_logs': instructor_action_logs,
                                                              'group_classes_logs': group_classes_logs,
                                                              'have_instructor': have_instructor}

        return Response(data)

class CustomerEditProfileView(generics.ListCreateAPIView):
    """
    get:
        get information to render page with edit form

    put:
        put new information to render page with edit form
        day_of_birth format is 1999-12-9
    """
    allowed_methods = ["PUT", "GET"]
    def get(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        role = get_role_json(request)
        data = {'role': role}

        return Response(data)

    serializer_class = EditInstructorProfileSerializer
    def put(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        cleaned_data = request.data
        if type(cleaned_data['day_of_birth']) == str:
            dt_string = cleaned_data['day_of_birth']
            format = "%Y-%m-%d"
            dt_object = datetime.datetime.strptime(dt_string, format)
            cleaned_data['day_of_birth'] = dt_object
        CustomersService.update_by_pk(request.user,
                                      role['customer']['customer_id'],
                                      cleaned_data)

        return JsonResponse({'status': 'Ok', 'message': 'You change customer profile data'},
                            status=200)

class CustomerEditProfileMeasureView(generics.ListCreateAPIView):
    """
    put:
        add new measure to customers measures
        date format is 1999-12-9
    delete:
        delete last measure from customers measures
    """
    allowed_methods = ["PUT", "DELETE"]
    serializer_class = CustomerMeasureSerializer
    def put(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        weight = request.data["weight"]
        date = request.data["date"]

        customer = CustomersService.read_filtered(request.user, {'user_id': request.user.pk})[0]
        old_weights = customer.measured_weights
        old_dates = customer.measure_dates

        old_weights.append(int(weight))
        old_dates.append(datetime.datetime.strptime(date, "%Y-%m-%d").date())

        measure = []
        for i in range(len(old_dates)):
            measure.append((old_dates[i], old_weights[i]))

        sorted_measure = sorted(measure)

        new_weights = []
        new_dates = []
        for i in range(len(sorted_measure)):
            new_dates.append(sorted_measure[i][0])
            new_weights.append(sorted_measure[i][1])

        CustomersService.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': new_weights,
                                                            'measure_dates': new_dates})

        customer = CustomersService.read_filtered(request.user, {'user_id': request.user.pk})[0]

        is_chart = 1
        if len(customer.measure_dates) == 0:
            is_chart = 0

        chart = get_plot(customer.measure_dates, customer.measured_weights)
        data = {'chart': chart, 'is_chart': is_chart}

        return Response(data)

    def delete(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        customer = CustomersService.read_filtered(request.user, {'user_id': request.user.pk})[0]
        weights = customer.measured_weights
        dates = customer.measure_dates

        if len(dates) > 0:
            dates.pop(len(dates) - 1)
            weights.pop(len(dates) - 1)

        CustomersService.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': weights,
                                                            'measure_dates': dates})
        customer = CustomersService.read_filtered(request.user, {'user_id': request.user.pk})[0]
        is_chart = 1
        if len(customer.measure_dates) == 0:
            is_chart = 0
        chart = get_plot(customer.measure_dates, customer.measured_weights)

        data = {'chart': chart, 'is_chart': is_chart}

        return Response(data)

def pass_future_group(request, date_today, time_today, customer_id):
    group_classes_records = GroupClassesCustomersRecordsService.read_join_filtered(request.user, "shedule",
                                                                                      {'customer_id': customer_id})
    pass_classes = []
    future_classes = []

    for group_class in group_classes_records:

        data = {'date': group_class.class_date, 'day_of_week': days[group_class.shedule.day_of_week],
                'time': group_class.shedule.class_time,
                'class_name': group_class.shedule.class_field.class_name,
                'record_id': group_class.record_id}

        if date_today > data['date']:
            pass_classes.append(data)
        elif date_today == data['date'] and time_today >= data['time']:
            pass_classes.append(data)
        else:
            future_classes.append(data)

    return pass_classes, future_classes

def pass_future_personal(request, date_today, time_today, customer_id):
    personal_records = InstructorSheduleCustomersService.read_join_filtered(request.user, "i_shedule",
                                                                               {'customer_id': customer_id})
    pass_personal_trainings = []
    future_personal_trainings = []

    for train in personal_records:
        instructor = \
            InstructorsService.read_filtered(request.user, {'instructor_id': train.i_shedule.instructor_id})[0]
        name = instructor.surname + " " + instructor.name + " " + instructor.patronymic
        data = {'date': train.training_date, 'day_of_week': days[train.i_shedule.day_of_week],
                'time': train.i_shedule.training_time, 'instructor_name': name, 'instructor_pk': instructor.pk,
                'record_id': train.record_id}

        if date_today > data['date']:
            pass_personal_trainings.append(data)
        elif date_today > data['date'] and time_today >= data['time']:
            pass_personal_trainings.append(data)
        else:
            future_personal_trainings.append(data)

    return pass_personal_trainings, future_personal_trainings


class CustomerTrainingRecordsView(APIView):
    """
    get:
        get customer training records
    """
    def get(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        week = get_week()
        selected_week = request.GET.get('week_num')
        if selected_week:
            week = selected_week

        date_today = datetime.date.today()
        time_today = datetime.datetime.now().time()

        pass_classes, future_classes = pass_future_group(request, date_today, time_today,
                                                         role['customer']['customer_id'])

        pass_personal_trainings, future_personal_trainings = pass_future_personal(request, date_today, time_today,
                                                                                  role['customer']['customer_id'])



        tarif = PricesService.read_filtered(request.user, {'tariff_id': role['customer']['tariff']})[0]
        classes_data, dates = form_classes_data_for_tarif_group_classes(request.user,
                                                                        role['customer']['customer_id'],
                                                                        role['user']['club'], tarif, week)

        trainings_data = []
        instructor_data = {}
        have_instructor = False
        if role['customer']['instructor']:
            trainings_data, dates = form_instructors_shedule_for_tarif(request.user,
                                                                       role['customer']['instructor'], tarif,
                                                                       week, role['customer']['customer_id'])
            have_instructor = True
            customers_instructor = \
            InstructorsService.read_filtered(request.user, {'instructor_id': role['customer']['instructor']})[
                0]
            instructor_data = {'instructor_name': customers_instructor.name,
                               'instructor_surname': customers_instructor.surname,
                               'instructor_patronymic': customers_instructor.patronymic,
                               'instructor_pk': customers_instructor.pk}

        day_of_week_date = {}
        for i in range(len(tarif.days_of_week)):
            day_of_week_date.update({days[tarif.days_of_week[i]]: dates[i]})

        club_id = role['user']['club']
        users_instructors = CustomUserService.read_filtered(request.user, {"club": club_id, 'role': 1})
        user_id_list = []
        for user in users_instructors:
            user_id_list.append(user.id)
        club_instructors = InstructorsService.read_filtered(request.user,
                                                               {'user__in': user_id_list, 'is_active': True})
        club_instructors_data = []
        for instr in club_instructors:
            data = {'name': instr.name, 'surname': instr.surname, 'patronimyc': instr.patronymic,
                    'instructor_id': instr.instructor_id,
                    'instructor_pk': instr.pk
                    }
            club_instructors_data.append(data)
        data = {'role': get_role_json(request), 'pass_group_classes': pass_classes,
                   'future_group_classes': future_classes,
                   'pass_personal_trainings': pass_personal_trainings,
                   'future_personal_trainings': future_personal_trainings,
                   'classes_data': classes_data,
                   'day_of_week_date': day_of_week_date,
                   'current_week': week,
                   'trainings_data': trainings_data,
                   'have_instructor': have_instructor,
                   'instructor_data': instructor_data,
                   'club_instructors_data': club_instructors_data
                   }

        return Response(data)

class CustomerCreatePersonalTrainingRecordView(generics.ListCreateAPIView):
    """
    post:
        create new record for personal training
    """
    allowed_methods = ["POST"]
    serializer_class = CustomerPersonalTrainingSerializer
    def post(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        i_shedule_id = request.data["i_shedule_id"]
        date_raw = request.data["date_raw"]

        date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()
        new_record = InstructorSheduleCustomers()
        role = get_role_json(request)
        new_record.customer_id = role['customer']['customer_id']
        new_record.training_date = date
        new_record.i_shedule_id = i_shedule_id

        if role['customer']['instructor'] == None:
            return JsonResponse({'status': 'Ok', 'message': "User don't have instructor"}, status=400)

        club_schedule = InstructorSheduleService.read_filtered(request.user,
                                                                    {'i_shedule_id': i_shedule_id,
                                                                     'instructor': role['customer']['instructor']})

        if len(club_schedule) > 0:
            InstructorSheduleCustomersService.create(request.user, new_record)
            return JsonResponse({'status': 'Ok', 'message': 'New record created'}, status=200)

        return JsonResponse({'status': 'false', 'message': 'Wrong i_schedule_id'}, status=400)

class CustomerDeletePersonalTrainingRecordView(APIView):
    """
    delete:
        delete record for personal training by record_id
    """
    def delete(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        record_id = kwargs["record_id"]

        date_today = datetime.date.today()
        time_today = datetime.datetime.now().time()

        pass_personal_trainings, future_personal_trainings = pass_future_personal(request, date_today, time_today,
                                                                                  role['customer']['customer_id'])

        for trainig in future_personal_trainings:
            if int(record_id) == trainig['record_id']:
                InstructorSheduleCustomersService.delete_filtered(request.user, {'record_id': record_id})
                return JsonResponse({'status': 'Ok', 'message': 'You delete personal training'}, status=200)

        return JsonResponse({'status': 'false', 'message': 'Wrong record_id!'}, status=400)


class CustomerAddGroupClassesRecordView(generics.ListCreateAPIView):
    """
    post:
        create new record for group classes
    """
    allowed_methods = ["POST"]
    serializer_class = CustomerGroupTrainingSerializer
    def post(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        new_record = GroupClassesCustomersRecords()
        date_raw = request.data["date_raw"]
        date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()
        new_record.class_date = date
        shedule_id = request.data["shedule_id"]

        club_id = role['user']['club']
        club_schedule = GroupClassesSheduleService.read_filtered(request.user, {'shedule_id': shedule_id, "club_id": club_id})

        if len(club_schedule) > 0:
            new_record.shedule_id = request.data["shedule_id"]
            new_record.customer_id = role['customer']['customer_id']

            GroupClassesCustomersRecordsService.create(request.user, new_record)
            return JsonResponse({'status': 'Ok', 'message': 'New record created'}, status=200)

        return JsonResponse({'status': 'false', 'message': 'Wrong schedule_id'}, status=400)

class CustomerDeleteGroupTrainingRecordView(APIView):
    """
    delete:
        delete record for group training by record_id
    """
    def delete(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        record_id = kwargs["record_id"]

        date_today = datetime.date.today()
        time_today = datetime.datetime.now().time()

        pass_classes, future_classes = pass_future_group(request, date_today, time_today,
                                                         role['customer']['customer_id'])

        for trainig in future_classes:
            if int(record_id) == trainig['record_id']:
                GroupClassesCustomersRecordsService.delete_filtered(request.user, {'record_id': record_id})
                return JsonResponse({'status': 'Ok', 'message': 'You delete personal training'}, status=200)

        return JsonResponse({'status': 'false', 'message': 'Wrong record_id!'}, status=400)

class CustomerAppointmentToInstructorView(generics.ListCreateAPIView):
    """
    post:
        appoint customer to instructor
    put:
        change appoint customer to instructor
    delete:
        delete appoint customer to instructor
    """
    allowed_methods = ["PUT", "POST", "DELETE"]
    serializer_class = CustomerAppointSerializer
    def post(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)
        instructor_id = request.data["instructor_id"]
        instructor = InstructorsService.read_filtered(request.user, {'instructor_id': instructor_id})
        if len(instructor) == 0:
            return JsonResponse({'status': 'false', 'message': 'Wrong instructor_id'}, status=400)
        instructor_club = CustomUserService.read_filtered(request.user, {'email' : instructor[0].user})[0].club

        club_id = role['user']['club']

        if (club_id == instructor_club):
            CustomersService.update_filtered(request.user, {'user_id': request.user.pk},
                                                {'instructor_id': instructor_id})
            return JsonResponse({'status': 'Ok', 'message': 'Success'}, status=200)

        return JsonResponse({'status': 'false', 'message': 'Instructor work in other club!'}, status=400)

    def put(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        instructor_id = request.data["instructor_id"]
        instructor = InstructorsService.read_filtered(request.user, {'instructor_id': instructor_id})
        if len(instructor) == 0:
            return JsonResponse({'status': 'false', 'message': 'Wrong instructor_id'}, status=400)
        instructor_club = CustomUserService.read_filtered(request.user, {'email' : instructor[0].user})[0].club

        club_id = role['user']['club']

        if (club_id == instructor_club):
            delete_future_records_for_personal_trainings(request)
            CustomersService.update_filtered(request.user, {'user_id': request.user.pk},
                                                {'instructor_id': instructor_id})
            return JsonResponse({'status': 'Ok', 'message': 'Success'}, status=200)

        return JsonResponse({'status': 'false', 'message': 'Instructor work in other club!'}, status=400)

    def delete(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=403)

        delete_future_records_for_personal_trainings(request)
        CustomersService.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': None})

        return JsonResponse({'status': 'Ok', 'message': 'Success'}, status=200)

def delete_future_records_for_personal_trainings(request):
    role = get_role_json(request)
    instructors_shedule = InstructorSheduleService.read_filtered(request.user,
                                                                    {'instructor_id': role['customer']['instructor']})
    shedule_id_list = []
    for sh in instructors_shedule:
        shedule_id_list.append(sh.i_shedule_id)

    records = InstructorSheduleCustomersService.read_filtered(request.user, {'i_shedule_id__in': shedule_id_list,
                                                                                'customer_id': role['customer']['customer_id']})

    date_today = datetime.date.today()
    time_today = datetime.datetime.now().time()

    for record in records:
        if record.training_date > date_today:
            InstructorSheduleCustomersService.delete_filtered(request.user, {'record_id': record.record_id})
        if record.training_date == date_today:
            shedule_time = InstructorSheduleService.read_filtered(request.user,
                                                                     {'i_shedule_id': record.i_shedule_id})
            if len(shedule_time) != 0 and shedule_time[0].training_time > time_today:
                InstructorSheduleCustomersService.delete_filtered(request.user, {'record_id': record.record_id})
