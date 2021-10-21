from .customer import *
from .utils import *
from .week import *
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, SpecialOffersRepository, PricesRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, CustomUserRepository, \
    AdminGroupClassesLogsRepository, CustomersRepository

class CustomerProfileView(APIView):
    """
    get:
        get information for customer profile
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=404)

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
            instructor_action_records = InstructorPersonalTrainingsLogsRepository.read_join_filtered(request.user,
                                                                                                      'instructor',
                                                                         {'instructor': role['customer']['instructor']})

            for cur in instructor_action_records:
                if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
                    instructor_action_logs.append(cur)

        group_classes_logs = []
        admin_action_records = AdminGroupClassesLogsRepository.read_join_filtered(request.user, 'group_class',
                                                                             {'club': role['user']['club']})
        for cur in admin_action_records:
            if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
                group_classes_logs.append(cur)

        tariff = PricesRepository.read_by_pk(request.user, role['customer']['tariff'])
        data = {'role': get_role_json(request), 'chart': chart,
                                                              'tariff': PricesSerializer(tariff).data,
                                                              'today': today,
                                                              'is_chart': is_chart,
                                                              'instructor_action_logs': instructor_action_logs,
                                                              'group_classes_logs': group_classes_logs,
                                                              'have_instructor': have_instructor}

        return Response(data)

class CustomerEditProfileView(APIView):
    """
    get:
        get information to render page with edit form
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=404)

        role = get_role_json(request)
        data = {'role': role}

        return Response(data)

class CustomerEditProfilePutView(APIView):
    """
    put:
        put new information to render page with edit form
        day_of_birth format is 1999-12-9
    """
    def put(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=404)
        cleaned_data = kwargs
        print(kwargs)
        role = get_role_json(request)
        if type(cleaned_data['day_of_birth']) == str:
            dt_string = cleaned_data['day_of_birth']
            format = "%Y-%m-%d"
            dt_object = datetime.datetime.strptime(dt_string, format)
            cleaned_data['day_of_birth'] = dt_object
        CustomersRepository.update_by_pk(request.user,
                                      role['customer']['customer_id'],
                                      cleaned_data)

        return JsonResponse({'status': 'Ok', 'message': 'You change customer profile data'},
                            status=200)

class CustomerEditProfileAddMeasureView(APIView):
    """
    put:
        add new measure to customers measures
        date format is 1999-12-9
    """
    def put(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=404)

        weight = kwargs["weight"]
        date = kwargs["date"]

        customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
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

        CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': new_weights,
                                                            'measure_dates': new_dates})

        customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]

        is_chart = 1
        if len(customer.measure_dates) == 0:
            is_chart = 0

        chart = get_plot(customer.measure_dates, customer.measured_weights)
        data = {'chart': chart, 'is_chart': is_chart}

        return Response(data)

class CustomerEditProfileDeleteMeasureView(APIView):
    """
    delete:
        delete last measure from customers measures
    """
    def delete(self, request):
        role = get_role_json(request)
        if not role['is_customer']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'},
                                status=404)

        customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
        weights = customer.measured_weights
        dates = customer.measure_dates

        if len(dates) > 0:
            dates.pop(len(dates) - 1)
            weights.pop(len(dates) - 1)

        CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': weights,
                                                            'measure_dates': dates})
        customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
        is_chart = 1
        if len(customer.measure_dates) == 0:
            is_chart = 0
        chart = get_plot(customer.measure_dates, customer.measured_weights)

        data = {'chart': chart, 'is_chart': is_chart}

        return Response(data)