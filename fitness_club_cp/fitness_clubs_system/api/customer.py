from manager.repositories import InstructorsRepository, CustomUserRepository, PricesRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository

from .role import *
from .form_classes_data import *
from .instructor_schedule import *


# def customer_training_records_func(request):
#     role = get_role_json(request)
#     week = get_week()
#     selected_week = request.GET.get('week_num')
#     if selected_week:
#         week = selected_week
#     group_classes_records = GroupClassesCustomersRecordsRepository.read_join_filtered(request.user, "shedule",
#                                                                                      {'customer_id': role['customer']['customer_id']})
#     pass_classes = []
#     future_classes = []
#     date_today = datetime.date.today()
#     time_today = datetime.datetime.now().time()
#
#     for group_class in group_classes_records:
#
#         data = {'date': group_class.class_date, 'day_of_week': days[group_class.shedule.day_of_week],
#         'time': group_class.shedule.class_time, 'class_name': group_class.shedule.class_field.class_name,
#                 'record_id': group_class.record_id}
#
#         if date_today > data['date']:
#             pass_classes.append(data)
#         elif date_today == data['date'] and time_today >= data['time']:
#             pass_classes.append(data)
#         else:
#             future_classes.append(data)
#
#     personal_records = InstructorSheduleCustomersRepository.read_join_filtered(request.user, "i_shedule",
#                                                                                {'customer_id': role['customer']['customer_id']})
#
#     pass_personal_trainings = []
#     future_personal_trainings = []
#
#     for train in personal_records:
#         instructor = InstructorsRepository.read_filtered(request.user, {'instructor_id': train.i_shedule.instructor_id})[0]
#         name = instructor.surname + " " + instructor.name + " " + instructor.patronymic
#         data = {'date': train.training_date, 'day_of_week': days[train.i_shedule.day_of_week],
#         'time': train.i_shedule.training_time, 'instructor_name': name, 'instructor_pk': instructor.pk, 'record_id': train.record_id}
#
#         if date_today > data['date']:
#             pass_personal_trainings.append(data)
#         elif date_today > data['date'] and time_today >= data['time']:
#             pass_personal_trainings.append(data)
#         else:
#             future_personal_trainings.append(data)
#
#     tarif = PricesRepository.read_filtered(request.user, {'tariff_id': role['customer']['tariff_id']})[0]
#     classes_data, dates = form_classes_data_for_tarif_group_classes(request.user, role['customer']['customer_id'], role['user']['club'], tarif, week)
#
#     trainings_data = []
#     instructor_data = {}
#     have_instructor = False
#     if role['customer']['instructor_id']:
#         trainings_data, dates = form_instructors_shedule_for_tarif(request.user, role['customer']['instructor_id'], tarif, week, role['customer']['customer_id'])
#         have_instructor = True
#         customers_instructor = InstructorsRepository.read_filtered(request.user, {'instructor_id': role['customer']['instructor_id']})[0]
#         instructor_data = {'instructor_name': customers_instructor.name, 'instructor_surname': customers_instructor.surname,
#                             'instructor_patronymic': customers_instructor.patronymic,
#                             'instructor_pk': customers_instructor.pk}
#
#
#     day_of_week_date = {}
#     for i in range(len(tarif.days_of_week)):
#         day_of_week_date.update({days[tarif.days_of_week[i]]: dates[i]})
#
#     club_id = role['user']['club']
#     users_instructors = CustomUserRepository.read_filtered(request.user, {"club": club_id, 'role': 1})
#     user_id_list = []
#     for user in users_instructors:
#         user_id_list.append(user.id)
#     club_instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})
#     club_instructors_data = []
#     for instr in club_instructors:
#         data = {'name': instr.name, 'surname': instr.surname, 'patronimyc': instr.patronymic,
#                 'instructor_id': instr.instructor_id,
#                 'instructor_pk': instr.pk
#                 }
#         club_instructors_data.append(data)
#     context = {'role': get_role_json(request), 'pass_group_classes': pass_classes,
#      'future_group_classes': future_classes,
#      'pass_personal_trainings': pass_personal_trainings,
#      'future_personal_trainings': future_personal_trainings,
#      'classes_data': classes_data,
#      'day_of_week_date': day_of_week_date,
#     'current_week': week,
#     'trainings_data': trainings_data,
#     'have_instructor': have_instructor,
#     'instructor_data': instructor_data,
#     'club_instructors_data': club_instructors_data
#      }
#
#     return context