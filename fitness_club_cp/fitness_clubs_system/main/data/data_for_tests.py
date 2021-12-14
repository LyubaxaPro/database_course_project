from manager.services import ServicesService, FitnessClubsService, GroupClassesService,\
    GroupClassesSheduleService, InstructorsService, CustomUserService, SpecialOffersService, PricesService,\
    CustomersService, InstructorSheduleService, GroupClassesCustomersRecordsService, InstructorSheduleCustomersService,\
    AdministratorsService, AdminRecordsService, InstructorPersonalTrainingsLogsService, AdminGroupClassesLogsService
from main.dataBuilder import CustomerUser
import datetime
import time
from collections import OrderedDict
from api.serializers import ServicesSerializer, CustomersSerializer, CustomUserSerializer, AdministratorsSerializer, \
GroupClassesSerializer, GroupClassesCustomersRecordsSerializer, InstructorsSerializer, GroupClassesSheduleSerializer, \
AdminRecordsSerializer, InstructorSheduleSerializer, AInstructorSheduleCustomersSerializer, PricesSerializer, \
SpecialOffersSerializer, InstructorPersonalTrainingsLogsSerializer, AdminGroupClassesLogsSerializer, FitnessClubsSerializer

# 'role': {'is_customer': True,
#     'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
#     'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data}

def get_customer_user_index_data(user):
    customer = CustomersService.read_filtered(user, {'user': user.id})[0]
    customer_user_index_data = {'title': 'Главная страница', 'role': {'is_customer': True,
    'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data}}
    return customer_user_index_data

def get_customer_user_adress(user):
    customer = CustomersService.read_filtered(user, {'user': user.id})[0]
    clubs = FitnessClubsService.read_all(user)
    customer_user_adress = {'clubs': FitnessClubsSerializer(clubs, many=True).data,
            'role': {'is_customer': True,
    'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data}}
    return customer_user_adress

def get_service_customer_user_data(user):
    customer = CustomersService.read_filtered(user, {'user': user.id})[0]
    services = ServicesService.read_all(user)
    services_customer_user_data = {'services': ServicesSerializer(services, many=True).data, 'role': {'is_customer': True,
    'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data}}
    return services_customer_user_data

club_1_schedule = b'{"classes_data": {"09:00": {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": [{"instructor_name": "\\u0412\\u0435\\u0440\\u043e\\u043d\\u0438\\u043a\\u0430", "class_name": "POSTURAL", "shedule_id": 13}]}, "10:00": {"Monday": [], "Tuesday": [{"instructor_name": "\\u0410\\u0440\\u0441\\u0435\\u043d", "class_name": "LEGS&BUTTS", "shedule_id": 4}], "Wednesday": [], "Thursday": [], "Friday": [{"instructor_name": "\\u0414\\u0435\\u043c\\u0438\\u0434", "class_name": "Upper body", "shedule_id": 11}], "Saturday": [], "Sunday": []}, "11:00": {"Monday": [{"instructor_name": "\\u0410\\u0440\\u0441\\u0435\\u043d", "class_name": "CORE", "shedule_id": 1}], "Tuesday": [{"instructor_name": "\\u0410\\u0440\\u0441\\u0435\\u043d", "class_name": "ABS", "shedule_id": 3}], "Wednesday": [], "Thursday": [{"instructor_name": "\\u0410\\u043d\\u0442\\u043e\\u043d", "class_name": "POSTURAL", "shedule_id": 7}], "Friday": [], "Saturday": [], "Sunday": []}, "12:00": {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": [{"instructor_name": "\\u0410\\u043d\\u0442\\u043e\\u043d", "class_name": "MAKE BODY", "shedule_id": 14}]}, "13:00": {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}, "14:00": {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}, "15:00": {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [{"instructor_name": "\\u0410\\u0440\\u0441\\u0435\\u043d", "class_name": "ICG Color Cycle", "shedule_id": 10}], "Saturday": [], "Sunday": []}, "16:00": {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}, "17:00": {"Monday": [], "Tuesday": [], "Wednesday": [{"instructor_name": "\\u0412\\u0435\\u0440\\u043e\\u043d\\u0438\\u043a\\u0430", "class_name": "LEGS&BUTTS", "shedule_id": 6}], "Thursday": [], "Friday": [{"instructor_name": "\\u0415\\u043b\\u0438\\u0437\\u0430\\u0432\\u0435\\u0442\\u0430", "class_name": "LEGS&BUTTS", "shedule_id": 9}], "Saturday": [], "Sunday": []}, "18:00": {"Monday": [], "Tuesday": [], "Wednesday": [{"instructor_name": "\\u0410\\u043d\\u0442\\u043e\\u043d", "class_name": "CORE", "shedule_id": 5}], "Thursday": [{"instructor_name": "\\u0410\\u043d\\u0442\\u043e\\u043d", "class_name": "CORE", "shedule_id": 8}], "Friday": [], "Saturday": [], "Sunday": []}, "19:00": {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [], "Sunday": []}, "20:00": {"Monday": [{"instructor_name": "\\u0414\\u0435\\u043c\\u0438\\u0434", "class_name": "ABS", "shedule_id": 2}], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": [{"instructor_name": "\\u0414\\u0435\\u043c\\u0438\\u0434", "class_name": "LEGS&BUTTS", "shedule_id": 12}], "Sunday": []}}}'

classes_data_club1 = { '09:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [],
              'Sunday': [{'instructor_name': 'Вероника', 'class_name': 'POSTURAL', 'shedule_id': 13}]},
    '10:00': {'Monday': [], 'Tuesday': [{'instructor_name': 'Арсен', 'class_name': 'LEGS&BUTTS', 'shedule_id': 4}],
              'Wednesday': [], 'Thursday': [],
              'Friday': [{'instructor_name': 'Демид', 'class_name': 'Upper body', 'shedule_id': 11}], 'Saturday': [],
              'Sunday': []}, '11:00': {'Monday': [{'instructor_name': 'Арсен', 'class_name': 'CORE', 'shedule_id': 1}],
                                       'Tuesday': [{'instructor_name': 'Арсен', 'class_name': 'ABS', 'shedule_id': 3}],
                                       'Wednesday': [], 'Thursday': [
            {'instructor_name': 'Антон', 'class_name': 'POSTURAL', 'shedule_id': 7}], 'Friday': [], 'Saturday': [],
                                       'Sunday': []},
    '12:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [],
              'Sunday': [{'instructor_name': 'Антон', 'class_name': 'MAKE BODY', 'shedule_id': 14}]},
    '13:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
    '14:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
    '15:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [],
              'Friday': [{'instructor_name': 'Арсен', 'class_name': 'ICG Color Cycle', 'shedule_id': 10}],
              'Saturday': [], 'Sunday': []},
    '16:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
    '17:00': {'Monday': [], 'Tuesday': [],
              'Wednesday': [{'instructor_name': 'Вероника', 'class_name': 'LEGS&BUTTS', 'shedule_id': 6}],
              'Thursday': [], 'Friday': [{'instructor_name': 'Елизавета', 'class_name': 'LEGS&BUTTS', 'shedule_id': 9}],
              'Saturday': [], 'Sunday': []}, '18:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [
        {'instructor_name': 'Антон', 'class_name': 'CORE', 'shedule_id': 5}], 'Thursday': [
        {'instructor_name': 'Антон', 'class_name': 'CORE', 'shedule_id': 8}], 'Friday': [], 'Saturday': [],
                                                       'Sunday': []},
    '19:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
    '20:00': {'Monday': [{'instructor_name': 'Демид', 'class_name': 'ABS', 'shedule_id': 2}], 'Tuesday': [],
              'Wednesday': [], 'Thursday': [], 'Friday': [],
              'Saturday': [{'instructor_name': 'Демид', 'class_name': 'LEGS&BUTTS', 'shedule_id': 12}], 'Sunday': []}}

def get_groupclasses_customer_user_data(user):
    customer = CustomersService.read_filtered(user, {'user' : user.id})[0]
    gclasses = GroupClassesService.read_all(user)
    data = {'classes_data': classes_data_club1, 'classes': GroupClassesSerializer(gclasses, many=True).data, 'role': {'is_customer': True,
    'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data}}
    return data

def get_instructors_list_data(user):
    customer = CustomersService.read_filtered(user, {'user': user.id})[0]
    instructors = InstructorsService.read_filtered(user, {'is_active': True})
    data = {'instructors': InstructorsSerializer(instructors, many=True).data, 'role': {'is_customer': True,
    'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data}}
    return data

def get_instructor_1_detail_data(user):
    customer = CustomersService.read_filtered(user, {'user': user.id})[0]
    instructor = InstructorsService.read_by_pk(user, 1)
    return {'instructor': InstructorsSerializer(instructor).data, 'exp_str': 'лет', 'role': {'is_customer': True,
    'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data},
    'shedule': {'09:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 33}, 'Saturday': {}, 'Sunday': {}}, '10:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 31}, 'Saturday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 45}, 'Sunday': {}}, '11:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {}}, '12:00': {'Monday': {}, 'Tuesday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 8}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {}}, '13:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 18}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 57}}, '14:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {}}, '15:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 46}, 'Sunday': {}}, '16:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 56}}, '17:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {'name': 'LEGS&BUTTS', 'is_editable': False}, 'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 54}}, '18:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {}}, '19:00': {'Monday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 1}, 'Tuesday': {}, 'Wednesday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 16}, 'Thursday': {}, 'Friday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 32}, 'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 55}}, '20:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 17}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {}}}, 'address': 'Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)'}

def get_prices_customer_user_data(user):
    customer = CustomersService.read_filtered(user, {'user': user.id})[0]
    special_offers = SpecialOffersService.read_all(user)
    prices = PricesService.read_all(user)

    data = {'special_offers': SpecialOffersSerializer(special_offers, many=True).data,
                'prices': PricesSerializer(prices, many=True).data, 'role': {'is_customer': True,
    'customer': CustomersSerializer(customer).data,'is_instructor': False, 'instructor': InstructorsSerializer().data,
    'is_admin': False, 'admin': AdministratorsSerializer().data, 'is_guest': False, 'user': CustomUserSerializer(user).data}}
    return data

def get_role_superuser(user):
    return (False, CustomersSerializer().data, False, InstructorsSerializer().data, True,
            AdministratorsSerializer(AdministratorsService.read_by_pk(user, 1)).data, False,
    CustomUserSerializer(CustomUserService.read_by_pk(user, 1)).data)

def get_role_admin(user):
    return (False, CustomersSerializer().data, False, InstructorsSerializer().data, True,
            AdministratorsSerializer(AdministratorsService.read_by_pk(user, 2)).data, False,
                    CustomUserSerializer(CustomUserService.read_by_pk(user, 2)).data)

def get_role_instructor(user):
    return (False, CustomersSerializer().data, True, InstructorsSerializer(InstructorsService.read_by_pk(user, 1)).data,
            False, AdministratorsSerializer().data, False, CustomUserSerializer(CustomUserService.read_by_pk(user, 9)).data)

def get_role_customer(user):
    return (True, CustomersSerializer(CustomersService.read_by_pk(user, 1)).data, False,
            InstructorsSerializer().data, False, AdministratorsSerializer().data, False,
            CustomUserSerializer(CustomUserService.read_by_pk(user, 14)).data)

def get_role_anon():
    return (False, CustomersSerializer().data, False, InstructorsSerializer().data, False, AdministratorsSerializer().data, True, CustomUserSerializer().data)

instructor_user_11_schedule = {'09:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Friday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Saturday': {}, 'Sunday': {}}, '10:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {'name': 'Upper body', 'is_personal': False, 'count': 0}, 'Saturday': {}, 'Sunday': {}}, '11:00': {'Monday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Sunday': {}}, '12:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Thursday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Friday': {}, 'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}}, '13:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Saturday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Sunday': {}}, '14:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}}, '15:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}}, '16:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Saturday': {}, 'Sunday': {}}, '17:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Sunday': {}}, '18:00': {'Monday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Tuesday': {}, 'Wednesday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {}}, '19:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Saturday': {}, 'Sunday': {}}, '20:00': {'Monday': {'name': 'ABS', 'is_personal': False, 'count': 0}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Friday': {}, 'Saturday': {'name': 'LEGS&BUTTS', 'is_personal': False, 'count': 0}, 'Sunday': {}}}

classes_data_for_user_14 = {'09:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': [{'instructor_name': 'Вероника', 'class_name': 'POSTURAL', 'shedule_id': 13}]}, '10:00': {'Monday': [], 'Tuesday': [{'instructor_name': 'Арсен', 'class_name': 'LEGS&BUTTS', 'shedule_id': 4}], 'Wednesday': [], 'Thursday': [], 'Friday': [{'instructor_name': 'Демид', 'class_name': 'Upper body', 'shedule_id': 11}], 'Saturday': [], 'Sunday': []}, '11:00': {'Monday': [{'instructor_name': 'Арсен', 'class_name': 'CORE', 'shedule_id': 1}], 'Tuesday': [{'instructor_name': 'Арсен', 'class_name': 'ABS', 'shedule_id': 3}], 'Wednesday': [], 'Thursday': [{'instructor_name': 'Антон', 'class_name': 'POSTURAL', 'shedule_id': 7}], 'Friday': [], 'Saturday': [], 'Sunday': []}, '12:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': [{'instructor_name': 'Антон', 'class_name': 'MAKE BODY', 'shedule_id': 14}]}, '13:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}, '14:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}, '15:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [{'instructor_name': 'Арсен', 'class_name': 'ICG Color Cycle', 'shedule_id': 10}], 'Saturday': [], 'Sunday': []}, '16:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}, '17:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [{'instructor_name': 'Вероника', 'class_name': 'LEGS&BUTTS', 'shedule_id': 6}], 'Thursday': [], 'Friday': [{'instructor_name': 'Елизавета', 'class_name': 'LEGS&BUTTS', 'shedule_id': 9}], 'Saturday': [], 'Sunday': []}, '18:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [{'instructor_name': 'Антон', 'class_name': 'CORE', 'shedule_id': 5}], 'Thursday': [{'instructor_name': 'Антон', 'class_name': 'CORE', 'shedule_id': 8}], 'Friday': [], 'Saturday': [], 'Sunday': []}, '19:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}, '20:00': {'Monday': [{'instructor_name': 'Демид', 'class_name': 'ABS', 'shedule_id': 2}], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [{'instructor_name': 'Демид', 'class_name': 'LEGS&BUTTS', 'shedule_id': 12}], 'Sunday': []}}

admin_classes_data_for_superuser = ({'09:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [{'instructor_name': 'Вероника', 'class_name': 'POSTURAL', 'shedule_id': 13, 'class_date': datetime.date(2021, 5, 30), 'count': 0}], 'busy_instructors': '[4]'}}, '10:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [{'instructor_name': 'Арсен', 'class_name': 'LEGS&BUTTS', 'shedule_id': 4, 'class_date': datetime.date(2021, 5, 25), 'count': 0}], 'busy_instructors': '[2]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [{'instructor_name': 'Демид', 'class_name': 'Upper body', 'shedule_id': 11, 'class_date': datetime.date(2021, 5, 28), 'count': 0}], 'busy_instructors': '[3]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '11:00': {'Monday': {'data': [{'instructor_name': 'Арсен', 'class_name': 'CORE', 'shedule_id': 1, 'class_date': datetime.date(2021, 5, 24), 'count': 0}], 'busy_instructors': '[2]'}, 'Tuesday': {'data': [{'instructor_name': 'Арсен', 'class_name': 'ABS', 'shedule_id': 3, 'class_date': datetime.date(2021, 5, 25), 'count': 0}], 'busy_instructors': '[2]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [{'instructor_name': 'Антон', 'class_name': 'POSTURAL', 'shedule_id': 7, 'class_date': datetime.date(2021, 5, 27), 'count': 1}], 'busy_instructors': '[5]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '12:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [{'instructor_name': 'Антон', 'class_name': 'MAKE BODY', 'shedule_id': 14, 'class_date': datetime.date(2021, 5, 30), 'count': 0}], 'busy_instructors': '[5]'}}, '13:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '14:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '15:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [{'instructor_name': 'Арсен', 'class_name': 'ICG Color Cycle', 'shedule_id': 10, 'class_date': datetime.date(2021, 5, 28), 'count': 0}], 'busy_instructors': '[2]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '16:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '17:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [{'instructor_name': 'Вероника', 'class_name': 'LEGS&BUTTS', 'shedule_id': 6, 'class_date': datetime.date(2021, 5, 26), 'count': 0}], 'busy_instructors': '[4]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [{'instructor_name': 'Елизавета', 'class_name': 'LEGS&BUTTS', 'shedule_id': 9, 'class_date': datetime.date(2021, 5, 28), 'count': 0}], 'busy_instructors': '[1]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '18:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [{'instructor_name': 'Антон', 'class_name': 'CORE', 'shedule_id': 5, 'class_date': datetime.date(2021, 5, 26), 'count': 0}], 'busy_instructors': '[5]'}, 'Thursday': {'data': [{'instructor_name': 'Антон', 'class_name': 'CORE', 'shedule_id': 8, 'class_date': datetime.date(2021, 5, 27), 'count': 0}], 'busy_instructors': '[5]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '19:00': {'Monday': {'data': [], 'busy_instructors': '[]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [], 'busy_instructors': '[]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}, '20:00': {'Monday': {'data': [{'instructor_name': 'Демид', 'class_name': 'ABS', 'shedule_id': 2, 'class_date': datetime.date(2021, 5, 24), 'count': 1}], 'busy_instructors': '[3]'}, 'Tuesday': {'data': [], 'busy_instructors': '[]'}, 'Wednesday': {'data': [], 'busy_instructors': '[]'}, 'Thursday': {'data': [], 'busy_instructors': '[]'}, 'Friday': {'data': [], 'busy_instructors': '[]'}, 'Saturday': {'data': [{'instructor_name': 'Демид', 'class_name': 'LEGS&BUTTS', 'shedule_id': 12, 'class_date': datetime.date(2021, 5, 29), 'count': 0}], 'busy_instructors': '[3]'}, 'Sunday': {'data': [], 'busy_instructors': '[]'}}}, {'Понедельник': datetime.date(2021, 5, 24), 'Вторник': datetime.date(2021, 5, 25), 'Среда': datetime.date(2021, 5, 26), 'Четверг': datetime.date(2021, 5, 27), 'Пятница': datetime.date(2021, 5, 28), 'Суббота': datetime.date(2021, 5, 29), 'Воскресенье': datetime.date(2021, 5, 30)})

data_for_tarif0_user14 = ({'09:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '10:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '11:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '12:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '13:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '14:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '15:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '16:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '17:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}},
                             64800, {'Monday': datetime.date(2021, 5, 24), 'Tuesday': datetime.date(2021, 5, 25),
                                     'Wednesday': datetime.date(2021, 5, 26), 'Thursday': datetime.date(2021, 5, 27),
                                     'Friday': datetime.date(2021, 5, 28), 'Saturday': datetime.date(2021, 5, 29),
                                     'Sunday': datetime.date(2021, 5, 30)},
                             ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                             [datetime.date(2021, 5, 24), datetime.date(2021, 5, 25), datetime.date(2021, 5, 26),
                              datetime.date(2021, 5, 27), datetime.date(2021, 5, 28)], [9, 18])

data_for_tarif1_user14 = ({'09:00': {'Saturday': [], 'Sunday': []}, '10:00': {'Saturday': [], 'Sunday': []},
                              '11:00': {'Saturday': [], 'Sunday': []}, '12:00': {'Saturday': [], 'Sunday': []},
                              '13:00': {'Saturday': [], 'Sunday': []}, '14:00': {'Saturday': [], 'Sunday': []},
                              '15:00': {'Saturday': [], 'Sunday': []}, '16:00': {'Saturday': [], 'Sunday': []},
                              '17:00': {'Saturday': [], 'Sunday': []}, '18:00': {'Saturday': [], 'Sunday': []},
                              '19:00': {'Saturday': [], 'Sunday': []}, '20:00': {'Saturday': [], 'Sunday': []}}, 75600,
                             {'Monday': datetime.date(2021, 5, 24), 'Tuesday': datetime.date(2021, 5, 25),
                              'Wednesday': datetime.date(2021, 5, 26), 'Thursday': datetime.date(2021, 5, 27),
                              'Friday': datetime.date(2021, 5, 28), 'Saturday': datetime.date(2021, 5, 29),
                              'Sunday': datetime.date(2021, 5, 30)}, ['Saturday', 'Sunday'],
                             [datetime.date(2021, 5, 29), datetime.date(2021, 5, 30)], [9, 21])

data_for_tarif2_user14 = ({'09:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '10:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '11:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '12:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '13:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '14:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '15:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '16:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '17:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '18:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '19:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []},
 '20:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}},
75600,
{'Monday': datetime.date(2021, 5, 24), 'Tuesday': datetime.date(2021, 5, 25), 'Wednesday': datetime.date(2021, 5, 26),
 'Thursday': datetime.date(2021, 5, 27), 'Friday': datetime.date(2021, 5, 28), 'Saturday': datetime.date(2021, 5, 29),
 'Sunday': datetime.date(2021, 5, 30)}, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
[datetime.date(2021, 5, 24), datetime.date(2021, 5, 25), datetime.date(2021, 5, 26), datetime.date(2021, 5, 27),
 datetime.date(2021, 5, 28), datetime.date(2021, 5, 29), datetime.date(2021, 5, 30)], [9, 21])

data_for_tarif3_user14 = ({'15:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '16:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '17:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '18:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '19:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []},
                              '20:00': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}},
                             75600, {'Monday': datetime.date(2021, 5, 24), 'Tuesday': datetime.date(2021, 5, 25),
                                     'Wednesday': datetime.date(2021, 5, 26), 'Thursday': datetime.date(2021, 5, 27),
                                     'Friday': datetime.date(2021, 5, 28), 'Saturday': datetime.date(2021, 5, 29),
                                     'Sunday': datetime.date(2021, 5, 30)},
                             ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                             [datetime.date(2021, 5, 24), datetime.date(2021, 5, 25), datetime.date(2021, 5, 26),
                              datetime.date(2021, 5, 27), datetime.date(2021, 5, 28)], [15, 21])

instructor_schedule_for_user18 = {'09:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {},
                                      'Friday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                 'i_shedule_id': 33}, 'Saturday': {}, 'Sunday': {}},
                            '10:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {},
                                      'Friday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                 'i_shedule_id': 31},
                                      'Saturday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                   'i_shedule_id': 45}, 'Sunday': {}},
                            '11:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                      'Saturday': {}, 'Sunday': {}}, '12:00': {'Monday': {}, 'Tuesday': {
        'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 8}, 'Wednesday': {}, 'Thursday': {},
                                                                               'Friday': {}, 'Saturday': {},
                                                                               'Sunday': {}},
                            '13:00': {'Monday': {}, 'Tuesday': {},
                                      'Wednesday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                    'i_shedule_id': 18}, 'Thursday': {}, 'Friday': {}, 'Saturday': {},
                                      'Sunday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                 'i_shedule_id': 57}},
                            '14:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                      'Saturday': {}, 'Sunday': {}},
                            '15:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                      'Saturday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                   'i_shedule_id': 46}, 'Sunday': {}},
                            '16:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                      'Saturday': {}, 'Sunday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                                 'i_shedule_id': 56}},
                            '17:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {},
                                      'Friday': {'name': 'LEGS&BUTTS', 'is_editable': False}, 'Saturday': {},
                                      'Sunday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                 'i_shedule_id': 54}},
                            '18:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                      'Saturday': {}, 'Sunday': {}}, '19:00': {
        'Monday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 1}, 'Tuesday': {},
        'Wednesday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 16}, 'Thursday': {},
        'Friday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 32}, 'Saturday': {},
        'Sunday': {'name': 'Персональная тренировка', 'is_editable': True, 'i_shedule_id': 55}},
                            '20:00': {'Monday': {}, 'Tuesday': {},
                                      'Wednesday': {'name': 'Персональная тренировка', 'is_editable': True,
                                                    'i_shedule_id': 17}, 'Thursday': {}, 'Friday': {}, 'Saturday': {},
                                      'Sunday': {}}}

instructors_shedule_for_week_for_user18 = ({'09:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {},
                                       'Friday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                  'customer': None}, 'Saturday': {}, 'Sunday': {}},
                             '10:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {},
                                       'Friday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                  'customer': None},
                                       'Saturday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                    'customer': None}, 'Sunday': {}},
                             '11:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                       'Saturday': {}, 'Sunday': {}}, '12:00': {'Monday': {}, 'Tuesday': {
        'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Wednesday': {}, 'Thursday': {},
                                                                                'Friday': {}, 'Saturday': {},
                                                                                'Sunday': {}},
                             '13:00': {'Monday': {}, 'Tuesday': {},
                                       'Wednesday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                     'customer': None}, 'Thursday': {}, 'Friday': {}, 'Saturday': {},
                                       'Sunday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                  'customer': None}},
                             '14:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                       'Saturday': {}, 'Sunday': {}},
                             '15:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                       'Saturday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                    'customer': None}, 'Sunday': {}},
                             '16:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                       'Saturday': {},
                                       'Sunday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                  'customer': None}},
                             '17:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {},
                                       'Friday': {'name': 'LEGS&BUTTS', 'is_personal': False, 'count': 0},
                                       'Saturday': {},
                                       'Sunday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                  'customer': None}},
                             '18:00': {'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {},
                                       'Saturday': {}, 'Sunday': {}}, '19:00': {
        'Monday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Tuesday': {},
        'Wednesday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Thursday': {},
        'Friday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}, 'Saturday': {},
        'Sunday': {'name': 'Персональная тренировка', 'is_personal': True, 'customer': None}},
                             '20:00': {'Monday': {}, 'Tuesday': {},
                                       'Wednesday': {'name': 'Персональная тренировка', 'is_personal': True,
                                                     'customer': None}, 'Thursday': {}, 'Friday': {}, 'Saturday': {},
                                       'Sunday': {}}},
                            {'Понедельник': datetime.date(2021, 5, 24), 'Вторник': datetime.date(2021, 5, 25),
                             'Среда': datetime.date(2021, 5, 26), 'Четверг': datetime.date(2021, 5, 27),
                             'Пятница': datetime.date(2021, 5, 28), 'Суббота': datetime.date(2021, 5, 29),
                             'Воскресенье': datetime.date(2021, 5, 30)})

customer_pass_group_classes = [
    {'date': datetime.date(2021, 5, 10), 'day_of_week': 'Понедельник', 'time': datetime.time(11, 0),
     'class_name': 'CORE', 'record_id': 1},
    {'date': datetime.date(2021, 6, 22), 'day_of_week': 'Вторник', 'time': datetime.time(11, 0), 'class_name': 'ABS',
     'record_id': 7}, {'date': datetime.date(2021, 6, 29), 'day_of_week': 'Вторник', 'time': datetime.time(10, 0),
                       'class_name': 'LEGS&BUTTS', 'record_id': 10},
    {'date': datetime.date(2021, 6, 9), 'day_of_week': 'Среда', 'time': datetime.time(17, 0),
     'class_name': 'LEGS&BUTTS', 'record_id': 16},
    {'date': datetime.date(2021, 5, 20), 'day_of_week': 'Четверг', 'time': datetime.time(11, 0),
     'class_name': 'POSTURAL', 'record_id': 20},
    {'date': datetime.date(2021, 6, 25), 'day_of_week': 'Пятница', 'time': datetime.time(17, 0),
     'class_name': 'LEGS&BUTTS', 'record_id': 26},
    {'date': datetime.date(2021, 6, 18), 'day_of_week': 'Пятница', 'time': datetime.time(15, 0),
     'class_name': 'ICG Color Cycle', 'record_id': 30},
    {'date': datetime.date(2021, 5, 21), 'day_of_week': 'Пятница', 'time': datetime.time(10, 0),
     'class_name': 'Upper body', 'record_id': 34}]
