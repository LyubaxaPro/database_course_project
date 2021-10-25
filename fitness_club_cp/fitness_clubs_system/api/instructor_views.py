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
    AdminGroupClassesLogsRepository, CustomersRepository, InstructorSheduleRepository

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
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=404)

        fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user']['club']})
        address = fitness_club[0].city + ", " + fitness_club[0].address
        instructor_shedule = form_instructors_shedule(request.user, role['instructor']['instructor_id'])

        exp_str = "лет"
        if role['instructor']['experience'] % 10 == 1 and role['instructor']['experience'] != 11:
            exp_str = "год"
        elif role['instructor']['experience'] % 10 in [2, 3, 4] and role['instructor']['experience'] not in [12, 13,
                                                                                                             14]:
            exp_str = "года"

        record = AdminRecordsRepository.read_filtered(request.user, {'instructor': role['instructor']['instructor_id'],
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
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        customers_data = []
        customers = CustomersRepository.read_filtered(request.user, {'instructor_id': role['instructor']['instructor_id']})
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

class InstructorEditProfileView(APIView):
    """
    get:
        get information to render page with edit form
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        data = {'role': role}

        return Response(data)
    

class InstructorEditProfilePostView(APIView):
    """
    post:
        create new record to admin_records with new information about instructor
        education, achievements, specialization with ;
    """

    def post(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        cleaned_data = kwargs
        if type(cleaned_data['education']) == str:
            cleaned_data['education'] = cleaned_data['education'].split(';')
            cleaned_data['achievements'] = cleaned_data['achievements'].split(';')
            cleaned_data['specialization'] = cleaned_data['specialization'].split(';')
        print(cleaned_data)
        admin_record = AdminRecords()
        admin_record.creation_datetime = datetime.datetime.now()
        admin_record.status = AdminRecords.PENDING
        instructor = InstructorsRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
        admin_record.instructor = instructor
        admin_record.admin = instructor.admin
        admin_record.change = {}
        old_instructor_data = InstructorsRepository.read_filtered(request.user,
                                                                  {'instructor_id': role['instructor']['instructor_id']})[0]

        admin_record.change.update({'old_name': old_instructor_data.name})
        admin_record.change.update({'old_surname': old_instructor_data.surname})
        admin_record.change.update({'old_patronymic': old_instructor_data.patronymic})
        admin_record.change.update({'old_education': old_instructor_data.education})
        admin_record.change.update({'old_experience': old_instructor_data.experience})
        admin_record.change.update({'old_achievements': old_instructor_data.achievements})
        admin_record.change.update({'old_specialization': old_instructor_data.specialization})
        admin_record.change.update({'old_photo': str(old_instructor_data.photo)})

        if (old_instructor_data.name != cleaned_data['name']):
            admin_record.change.update({'new_name': cleaned_data['name']})
        else:
            admin_record.change.update({'new_name': ''})
        if (old_instructor_data.surname != cleaned_data['surname']):
            admin_record.change.update({'new_surname': cleaned_data['surname']})
        else:
            admin_record.change.update({'new_surname': ''})
        if (old_instructor_data.patronymic != cleaned_data['patronymic']):
            admin_record.change.update({'new_patronymic': cleaned_data['patronymic']})
        else:
            admin_record.change.update({'new_patronymic': ''})
        if (old_instructor_data.education != cleaned_data['education']):
            admin_record.change.update({'new_education': cleaned_data['education']})
        else:
            admin_record.change.update({'new_education': ''})
        if (old_instructor_data.experience != cleaned_data['experience']):
            admin_record.change.update({'new_experience': cleaned_data['experience']})
        else:
            admin_record.change.update({'new_experience': ''})
        if (old_instructor_data.achievements != cleaned_data['achievements']):
            admin_record.change.update({'new_achievements': cleaned_data['achievements']})
        else:
            admin_record.change.update({'new_achievements': ''})
        if (old_instructor_data.achievements != cleaned_data['achievements']):
            admin_record.change.update({'new_achievements': cleaned_data['achievements']})
        else:
            admin_record.change.update({'new_achievements': ''})
        if (old_instructor_data.specialization != cleaned_data['specialization']):
            admin_record.change.update({'new_specialization': cleaned_data['specialization']})
        else:
            admin_record.change.update({'new_specialization': ''})

        AdminRecordsRepository.create(request.user, admin_record)

        return JsonResponse({'status': 'Ok'},
                            status=200)

class InstructorAddPersonalTrainingView(APIView):
    """
    put:
        add personal training to instructor's schedule
        day - day of week
        time from 9:00 to 20:00
    """

    def put(self, request, *args, **kwargs):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        day = kwargs["day"]
        time_raw = kwargs["time"]
        time = datetime.datetime.strptime(time_raw, '%H:%M').time()

        flag_rec = InstructorSheduleRepository.read_filtered(request.user, {"day_of_week": day,
                                                            "instructor_id": role['instructor']['instructor_id'],
                                                                            "training_time": time})
        if len(flag_rec) > 0:
            return JsonResponse({'status': 'false', 'message': 'This time is already busy'},
                                status=404)

        flag_group_classes_rec = GroupClassesSheduleRepository.read_filtered(request.user,
                                                                {"instructor": role['instructor']['instructor_id'],
                                                                 "class_time": time,
                                                                 "day_of_week": day})

        if len(flag_group_classes_rec) > 0:
            return JsonResponse({'status': 'false', 'message': 'This time is already busy'},
                                status=404)

        new_record = InstructorShedule()

        new_record.instructor_id = role['instructor']['instructor_id']
        new_record.training_time = time
        new_record.day_of_week = day

        InstructorSheduleRepository.create(request.user, new_record)

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
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        pk = kwargs["pk"]
        flag = AdminRecordsRepository.read_filtered(request.user, {"pk": pk})
        if len(flag) == 0:
            return JsonResponse({'status': 'false', 'message': "This record doesn't exist"},
                                status=404)

        AdminRecordsRepository.delete_by_pk(request.user, pk)

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
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        i_shedule_id = kwargs["i_shedule_id"]
        flag = InstructorSheduleRepository.read_filtered(request.user, {"i_shedule_id": i_shedule_id})
        if len(flag) == 0:
            return JsonResponse({'status': 'false', 'message': "This record doesn't exist"},
                                status=404)

        InstructorSheduleRepository.delete_filtered(request.user, {'i_shedule_id': i_shedule_id})

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
            return JsonResponse({'status':'false','message':'You do not have rights to get the information'}, status=405)

        week = get_week()
        selected_week = kwargs['week_num']
        if selected_week:
            week = selected_week
        instructor_shedule, day_of_week_date = form_instructors_shedule_for_week(request.user, role['instructor']['instructor_id'], week)
        fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user']['club']})
        address = fitness_club[0].city + ", " + fitness_club[0].address

        data = {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                       'day_of_week_date': day_of_week_date,
                       'current_week': week}

        return Response(data)