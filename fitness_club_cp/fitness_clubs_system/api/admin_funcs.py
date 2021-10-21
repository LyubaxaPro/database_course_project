from manager.repositories import FitnessClubsRepository, GroupClassesRepository, \
    InstructorsRepository, CustomUserRepository, AdministratorsRepository, AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository
from manager.models import AdminRecords
from .role import *
from django.utils import timezone
from .form_classes_data import *
from .instructor_schedule import *

def admin_profile_func(request):
    role = get_role_json(request)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user']['club']})
    address = fitness_club[0].city + ", " + fitness_club[0].address

    admin = AdministratorsRepository.read_filtered(request.user, {'user': role['admin']})[0]

    users_instructors = CustomUserRepository.read_filtered(request.user, {"club": role['user']['club'], 'role': 1})
    user_id_list = []
    for user in users_instructors:
        user_id_list.append(user.id)

    instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': False})

    instructors_data = []
    for instructor in instructors:
        user = CustomUserRepository.read_filtered(request.user, {'id': instructor.user_id})[0]
        instructors_data.append({'data': instructor, 'user': user})

    changes_instructors = AdminRecordsRepository.read_filtered(request.user, {'admin': role['admin']['user_id'],
                                                                              'status': AdminRecords.PENDING})

    active_instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})

    instructor_action_records = InstructorPersonalTrainingsLogsRepository.read_join_filtered(request.user, 'instructor',
                                                                             {'instructor__in': active_instructors})
    instructor_action_logs = []

    for cur in instructor_action_records:
        if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
            instructor_action_logs.append(cur)


    return {'role': role, 'address': address,
           'admin': admin, 'instructors': instructors_data,
           'changes_instructors': changes_instructors,
           'instructor_action_logs': instructor_action_logs}

def group_classes_admin_func(request):
    week = get_week()
    role = get_role_json(request)
    club_id = role['user']['club']
    classes_data, day_dates = form_admin_classes_data(request.user, club_id, week)

    club_info = FitnessClubsRepository.read_filtered(request.user, {'club_id': club_id})[0]
    address = club_info.city + ", " + club_info.address

    classes = GroupClassesRepository.read_all(request.user)

    users = CustomUserRepository.read_filtered(request.user, {"club": club_id})
    user_id_list = []
    for user in users:
        user_id_list.append(user.id)

    instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})

    return {'classes_data' : classes_data,
           'classes':classes, 'role': role,
             'address': address, 'instructors': instructors,
             'club_id': club_id}

def statistics_of_traininng_func(request):
    week = get_week()
    selected_week = request.GET.get('week_num')
    if selected_week:
        week = selected_week

    role = get_role_json(request)
    club_id = role['user']['club']
    classes_data, day_of_week_date = form_admin_classes_data(request.user, club_id, week)

    club_info = FitnessClubsRepository.read_filtered(request.user, {'club_id': club_id})[0]
    address = club_info.city + ", " + club_info.address

    classes = GroupClassesRepository.read_all(request.user)

    users = CustomUserRepository.read_filtered(request.user, {"club": club_id})
    user_id_list = []
    for user in users:
        user_id_list.append(user.id)


    return {'classes_data': classes_data,
             'classes': classes, 'role': role,
             'address': address,
             'club_id': club_id,
             'day_of_week_date': day_of_week_date,
                'current_week': week}