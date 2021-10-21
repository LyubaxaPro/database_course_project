from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers

from manager.repositories import GroupClassesRepository, \
    InstructorsRepository, SpecialOffersRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, CustomUserRepository, FitnessClubsRepository


# from fitness_clubs_system.api.utils import get_plot
# from fitness_clubs_system.api.view_funcs.simple_data import *
# from fitness_clubs_system.api.view_funcs.customer import *
# from fitness_clubs_system.main.view_funcs.instructor import *
# from fitness_clubs_system.api.view_funcs.admin import *
from .forms import *
from api.form_classes_data import form_classes_data
from api.instructor_schedule import form_instructors_shedule
from api.role import get_role_json
from api.admin_funcs import statistics_of_traininng_func
# def customer_profile(request):
#     return render(request, "main/customer_profile.html", customer_profile_func(request))
#
# def customer_profile_func(request):
#     role = get_role_json(request)
#     is_chart = True
#
#     x = role['customer']['measure_dates']
#     y = role['customer']['measured_weights']
#     if len(x) == 0:
#         is_chart = False
#
#     chart = get_plot(x, y)
#
#     today = datetime.datetime.today().strftime('%Y-%m-%d')
#
#     instructor_action_logs = []
#     have_instructor = False
#     if role['customer']['instructor_id']:
#         have_instructor = True
#         instructor_action_records = InstructorPersonalTrainingsLogsRepository.read_join_filtered(request.user,
#                                                                                                   'instructor',
#                                                                      {'instructor': role['customer']['instructor_id']})
#
#         for cur in instructor_action_records:
#             if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
#                 instructor_action_logs.append(cur)
#
#     group_classes_logs = []
#     admin_action_records = AdminGroupClassesLogsRepository.read_join_filtered(request.user, 'group_class',
#                                                                          {'club': role['user']['club']})
#     for cur in admin_action_records:
#         if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
#             group_classes_logs.append(cur)
#
#     return {'role': get_role_json(request), 'address': address, 'chart': chart,
#                                                           'form':AddMeasureForm(),
#                                                           'today': today,
#                                                           'is_chart': is_chart,
#                                                           'instructor_action_logs': instructor_action_logs,
#                                                           'group_classes_logs': group_classes_logs,
#                                                           'have_instructor': have_instructor}
#
# def edit_customer_profile(request):
#     role = get_role_json(request)
#
#     if request.method == 'POST':
#
#         customer_form = CustomerEditProfileForm(request.POST, instance=role['customer'])
#         customer_form.actual_user = request.user
#
#
#         if customer_form.is_valid():
#
#             CustomersRepository.update_by_pk(request.user,
#                                           role['customer']['pk'],
#                                           customer_form.cleaned_data)
#
#             return redirect('customer_profile')
#     else:
#         customer_form = CustomerEditProfileForm(instance=role['customer'])
#
#     return render(request, 'main/edit_customer.html', {'customer_form': customer_form, 'role': role})
#
# def add_measure(request):
#     weight = request.GET.get("weight")
#     date = request.GET.get("date")
#
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#     old_weights = customer.measured_weights
#     old_dates = customer.measure_dates
#
#     old_weights.append(int(weight))
#     old_dates.append(datetime.datetime.strptime(date, "%Y-%m-%d").date())
#
#     measure = []
#     for i in range(len(old_dates)):
#         measure.append((old_dates[i], old_weights[i]))
#
#     sorted_measure = sorted(measure)
#
#     new_weights = []
#     new_dates = []
#     for i in range(len(sorted_measure)):
#         new_dates.append(sorted_measure[i][0])
#         new_weights.append(sorted_measure[i][1])
#
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': new_weights,
#                                                         'measure_dates': new_dates})
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#
#     is_chart = 1
#     if len(customer.measure_dates) == 0:
#         is_chart = 0
#
#     chart = get_plot(customer.measure_dates, customer.measured_weights)
#     return JsonResponse({'chart': chart, 'is_chart': is_chart}, safe=False)
#
# def delete_measure(request):
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#     weights = customer.measured_weights
#     dates = customer.measure_dates
#
#     if len(dates) > 0:
#         dates.pop(len(dates) - 1)
#         weights.pop(len(dates) - 1)
#
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': weights,
#                                                         'measure_dates': dates})
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#     is_chart = 1
#     if len(customer.measure_dates) == 0:
#         is_chart = 0
#     chart = get_plot(customer.measure_dates, customer.measured_weights)
#
#     return JsonResponse({'chart': chart, 'is_chart': is_chart}, safe=False)
#
# def customer_training_records(request):
#     return render(request, "main/customer_training_records.html", customer_training_records_func(request))
#
# def delete_personal_training_record(request):
#     record_id = request.GET.get("record_id")
#     InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record_id})
#
#     return JsonResponse({'delete_data': []}, safe=False)
#
# def delete_group_class_record(request):
#     record_id = request.GET.get("record_id")
#     GroupClassesCustomersRecordsRepository.delete_filtered(request.user, {'record_id': record_id})
#
#     return JsonResponse({'delete_data': []}, safe=False)
#
# def add_group_class_record(request):
#     role = get_role_json(request)
#     new_record = GroupClassesCustomersRecords()
#     date_raw = request.GET.get("date")
#     date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()
#     new_record.class_date = date
#     new_record.shedule_id = request.GET.get("shedule_id")
#     new_record.customer_id=role['customer']['customer_id']
#
#
#     GroupClassesCustomersRecordsRepository.create(request.user, new_record)
#     return JsonResponse({'q': []}, safe=False)
#
# def add_personal_training_record(request):
#     i_shedule_id = request.GET.get("i_shedule_id")
#     date_raw = request.GET.get("date")
#     date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()
#
#     new_record = InstructorSheduleCustomers()
#     role = get_role_json(request)
#     new_record.customer_id = role['customer']['customer_id']
#     new_record.training_date = date
#     new_record.i_shedule_id = i_shedule_id
#
#     InstructorSheduleCustomersRepository.create(request.user, new_record)
#     return JsonResponse({'q': []}, safe=False)
#
# def appointment_to_instructor(request):
#     instructor_id = request.GET.get("instructor_id")
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': instructor_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_future_records_for_personal_trainings(request):
#     role = get_role_json(request)
#     instructors_shedule = InstructorSheduleRepository.read_filtered(request.user,
#                                                                     {'instructor_id': role['customer']['instructor_id']})
#     shedule_id_list = []
#     for sh in instructors_shedule:
#         shedule_id_list.append(sh.i_shedule_id)
#
#     records = InstructorSheduleCustomersRepository.read_filtered(request.user, {'i_shedule_id__in': shedule_id_list,
#                                                                                 'customer_id': role['customer']['customer_id']})
#
#     date_today = datetime.date.today()
#     time_today = datetime.datetime.now().time()
#
#     for record in records:
#         if record.training_date > date_today:
#             InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record.record_id})
#         if record.training_date == date_today:
#             shedule_time = InstructorSheduleRepository.read_filtered(request.user,
#                                                                      {'i_shedule_id': record.i_shedule_id})
#             if len(shedule_time) != 0 and shedule_time[0].training_time > time_today:
#                 InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record.record_id})
#
# def delete_appointment_to_instructor(request):
#     delete_future_records_for_personal_trainings(request)
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': None})
#     return JsonResponse({'q': []}, safe=False)
#
# def replace_appointment_to_instructor(request):
#     selected_instructor_id = request.GET.get("instructor_id")
#     delete_future_records_for_personal_trainings(request)
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': selected_instructor_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
def instructor_profile(request):
    view = AddressView()
    data = view.get(request)
    return render(request, "main/instructor_profile.html", data.data)
#
# def instructor_attached_customers_func(request):
#     role = get_role_json(request)
#     customers_data = []
#     customers = CustomersRepository.read_filtered(request.user, {'instructor_id': role['instructor']['instructor_id']})
#     is_chart = True
#
#     for customer in customers:
#         x = customer.measure_dates
#         y = customer.measured_weights
#         if len(x) == 0:
#             is_chart = False
#         chart = get_plot(x, y)
#         customers_data.append({'name': customer.name,
#                                'surname': customer.surname,
#                                'patronymic': customer.patronymic,
#                                'chart': chart,
#                                'is_chart': is_chart,
#                                'day_of_birth': customer.day_of_birth,
#                                'height': customer.height})
#
#     return {'role': role, 'customers_data': customers_data}
#
# def edit_instructor(request):
#     role = get_role_json(request)
#
#     if request.method == 'POST':
#
#         instructor_form = InstructorEditProfileForm(request.POST, request.FILES)
#         instructor_form.actual_user = request.user
#
#         if instructor_form.is_valid():
#
#             admin_record = AdminRecords()
#             admin_record.creation_datetime = datetime.datetime.now()
#             admin_record.status = AdminRecords.PENDING
#             admin_record.instructor = role['instructor']
#             admin_record.admin = role['instructor']['admin']
#             admin_record.change = {}
#
#             new_instructor_data = instructor_form.cleaned_data
#
#
#             old_instructor_data = InstructorsRepository.read_filtered(request.user,
#                                                                       {'instructor_id': role['instructor']['instructor_id']})[0]
#
#             admin_record.change.update({'old_name': old_instructor_data.name})
#             admin_record.change.update({'old_surname': old_instructor_data.surname})
#             admin_record.change.update({'old_patronymic': old_instructor_data.patronymic})
#             admin_record.change.update({'old_education': old_instructor_data.education})
#             admin_record.change.update({'old_experience': old_instructor_data.experience})
#             admin_record.change.update({'old_achievements': old_instructor_data.achievements})
#             admin_record.change.update({'old_specialization': old_instructor_data.specialization})
#             admin_record.change.update({'old_photo': str(old_instructor_data.photo)})
#
#             if (old_instructor_data.name != new_instructor_data['name']):
#                 admin_record.change.update({'new_name': new_instructor_data['name']})
#             else:
#                 admin_record.change.update({'new_name': ''})
#             if (old_instructor_data.surname != new_instructor_data['surname']):
#                 admin_record.change.update({'new_surname': new_instructor_data['surname']})
#             else:
#                 admin_record.change.update({'new_surname': ''})
#             if (old_instructor_data.patronymic != new_instructor_data['patronymic']):
#                 admin_record.change.update({'new_patronymic': new_instructor_data['patronymic']})
#             else:
#                 admin_record.change.update({'new_patronymic': ''})
#             if (old_instructor_data.education != new_instructor_data['education']):
#                 admin_record.change.update({'new_education': new_instructor_data['education']})
#             else:
#                 admin_record.change.update({'new_education': ''})
#             if (old_instructor_data.experience != new_instructor_data['experience']):
#                 admin_record.change.update({'new_experience': new_instructor_data['experience']})
#             else:
#                 admin_record.change.update({'new_experience': ''})
#             if (old_instructor_data.achievements != new_instructor_data['achievements']):
#                 admin_record.change.update({'new_achievements': new_instructor_data['achievements']})
#             else:
#                 admin_record.change.update({'new_achievements': ''})
#             if (old_instructor_data.achievements != new_instructor_data['achievements']):
#                 admin_record.change.update({'new_achievements': new_instructor_data['achievements']})
#             else:
#                 admin_record.change.update({'new_achievements': ''})
#             if (old_instructor_data.specialization != new_instructor_data['specialization']):
#                 admin_record.change.update({'new_specialization': new_instructor_data['specialization']})
#             else:
#                 admin_record.change.update({'new_specialization': ''})
#
#             AdminRecordsRepository.create(request.user, admin_record)
#
#             return redirect('instructor_profile')
#     else:
#         instructor_form = InstructorEditProfileForm(instance=role['instructor'])
#
#     return render(request, 'main/edit_instructor.html', {'instructor_form': instructor_form, 'role': role})
#
# def instructor_add_personal_training(request):
#     day = request.GET.get("day")
#     time_raw = request.GET.get("time")
#     time = datetime.datetime.strptime(time_raw, '%H:%M').time()
#
#     role = get_role_json(request)
#
#     new_record = InstructorShedule()
#
#     new_record.instructor_id = role['instructor']['instructor_id']
#     new_record.training_time = time
#     new_record.day_of_week = day
#
#     InstructorSheduleRepository.create(request.user, new_record)
#
#     return JsonResponse({'q': []}, safe=False)
#
# def instructor_delete_changes(request):
#     pk = request.GET.get("pk")
#     AdminRecordsRepository.delete_by_pk(request.user, pk)
#
#     return JsonResponse({'q': []}, safe=False)
#
# def instructor_delete_personal_training(request):
#     i_shedule_id = request.GET.get("i_shedule_id")
#     InstructorSheduleRepository.delete_filtered(request.user, {'i_shedule_id': i_shedule_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def instructor_attached_customers(request):
#     return render(request, 'main/instructor_attached_customers.html', instructor_attached_customers_func(request))
#
# def instructor_training_records(request):
#     return render(request, "main/instructor_training_records.html", instructor_training_records_func(request))
#
# def admin_profile(request):
#
#     return render(request, "main/admin_profile.html", admin_profile_func(request))
#
# def group_classes_admin(request):
#     return render(request, "main/group_classes_admin.html", group_classes_admin_func(request))
#
# def add_group_class_in_shedule(request):
#     day = request.GET.get("day")
#     time_raw = request.GET.get("time")
#     time = datetime.datetime.strptime(time_raw, '%H:%M').time()
#     instructor_id = request.GET.get("instructor_id")
#     class_id = request.GET.get("class_id")
#     club_id = request.GET.get("club_id")
#     maximum_quantity = request.GET.get("maximum_quantity")
#     busy_instructors_str = request.GET.get("busy_instructors")
#
#     busy_instructors = json.loads(busy_instructors_str)
#
#     if int(instructor_id) in busy_instructors:
#         response = JsonResponse({"error": "there was an error"})
#         response.status_code = 403
#         return response
#
#     new_record = GroupClassesShedule()
#     new_record.class_field = GroupClassesRepository.read_filtered(request.user, {'class_id': class_id})[0]
#     new_record.club = FitnessClubsRepository.read_filtered(request.user, {'club_id': club_id})[0]
#     new_record.instructor = InstructorsRepository.read_filtered(request.user, {'instructor_id': instructor_id})[0]
#     new_record.class_time = time
#     new_record.day_of_week = day
#     new_record.maximum_quantity = int(maximum_quantity)
#
#     GroupClassesSheduleRepository.create(request.user, new_record)
#
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_group_class_in_shedule(request):
#     shedule_id = request.GET.get("shedule_id")
#     GroupClassesSheduleRepository.delete_filtered(request.user, {'shedule_id': shedule_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_special_offer_by_admin(request):
#     offer_id = request.GET.get("offer_id")
#     SpecialOffersRepository.delete_filtered(request.user, {'offer_id': offer_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def add_special_offer_by_admin(request):
#     offer_name = request.GET.get("offer_name")
#     offer_description = request.GET.get("offer_description")
#
#     new_record = SpecialOffers()
#     new_record.offer_name = offer_name
#     new_record.offer_description = offer_description
#
#     SpecialOffersRepository.create(request.user, new_record)
#     return JsonResponse({'q': []}, safe=False)
#
def statistics_of_traininng(request):
    return render(request, "main/group_class_statistics.html", statistics_of_traininng_func((request)))
#
# def add_new_instructor(request):
#     instructor_id = request.GET.get("instructor_id")
#     InstructorsRepository.update_filtered(request.user, {'instructor_id': instructor_id}, {'is_active': True})
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_new_instructor(request):
#     user_id = request.GET.get("user_id")
#     CustomUserRepository.delete_filtered(request.user, {'id': user_id})
#     return JsonResponse({'q': []}, safe=False)
#
# def btn_change_instructor(request):
#     pk = request.GET.get("pk")
#
#     AdminRecordsRepository.update_by_pk(request.user, pk, {'status': AdminRecords.ACCEPTED})
#     change_dict = {}
#     admin_record = AdminRecordsRepository.read_by_pk(request.user, pk)
#
#     if admin_record.change['new_name'] != '':
#         change_dict.update({'name': admin_record.change['new_name']})
#
#     if admin_record.change['new_surname']:
#         change_dict.update({'surname': admin_record.change['new_surname']})
#
#     if admin_record.change['new_patronymic']:
#         change_dict.update({'patronymic': admin_record.change['new_patronymic']})
#
#     if admin_record.change['new_education']:
#         change_dict.update({'education': admin_record.change['new_education']})
#
#     if admin_record.change['new_experience']:
#         change_dict.update({'experience': admin_record.change['new_experience']})
#
#     if admin_record.change['new_achievements']:
#         change_dict.update({'achievements': admin_record.change['new_achievements']})
#
#     if admin_record.change['new_specialization']:
#         change_dict.update({'specialization': admin_record.change['new_specialization']})
#
#     InstructorsRepository.update_filtered(request.user, {'instructor_id': admin_record.instructor.instructor_id},
#                                           change_dict)
#     return JsonResponse({'q': []}, safe=False)
#
# def btn_not_change_instructor(request):
#     pk = request.GET.get("pk")
#     AdminRecordsRepository.update_by_pk(request.user, pk, {'status': AdminRecords.DECLINED})
#     return JsonResponse({'q': []}, safe=False)
#
def customer_profile(request):
    return render(request, "main/customer_profile.html", {'a':1})

def edit_customer_profile(request):

    if request.method == 'POST':
            return redirect('customer_profile')

    return render(request, 'main/edit_customer.html', {'a':1})

def add_measure(request):
    return JsonResponse({'a':1}, safe=False)

def delete_measure(request):
    return JsonResponse({'a':1}, safe=False)

def customer_training_records(request):
    return render(request, "main/customer_training_records.html", {'a':1})

def delete_personal_training_record(request):
    record_id = request.GET.get("record_id")
    InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record_id})

    return JsonResponse({'delete_data': []}, safe=False)

def delete_group_class_record(request):
    record_id = request.GET.get("record_id")
    GroupClassesCustomersRecordsRepository.delete_filtered(request.user, {'record_id': record_id})

    return JsonResponse({'delete_data': []}, safe=False)

def add_group_class_record(request):
    return JsonResponse({'q': []}, safe=False)

def add_personal_training_record(request):
    return JsonResponse({'q': []}, safe=False)

def appointment_to_instructor(request):
    return JsonResponse({'q': []}, safe=False)

def delete_appointment_to_instructor(request):
    return JsonResponse({'q': []}, safe=False)

def replace_appointment_to_instructor(request):
    return JsonResponse({'q': []}, safe=False)

def edit_instructor(request):

    return render(request, 'main/edit_instructor.html', {'a':1})

def instructor_add_personal_training(request):
    return JsonResponse({'q': []}, safe=False)

def instructor_delete_changes(request):
    return JsonResponse({'q': []}, safe=False)

def instructor_delete_personal_training(request):
    return JsonResponse({'q': []}, safe=False)

def instructor_attached_customers(request):
    return render(request, 'main/instructor_attached_customers.html', {})

def instructor_training_records(request):
    return render(request, "main/instructor_training_records.html", {'a':1})

def admin_profile(request):

    return render(request, "main/admin_profile.html", {'a':1})

def group_classes_admin(request):
    return render(request, "main/group_classes_admin.html", {'a':1})

def add_group_class_in_shedule(request):
    return JsonResponse({'q': []}, safe=False)

def delete_group_class_in_shedule(request):
    return JsonResponse({'q': []}, safe=False)

def delete_special_offer_by_admin(request):
    offer_id = request.GET.get("offer_id")
    SpecialOffersRepository.delete_filtered(request.user, {'offer_id': offer_id})

    return JsonResponse({'q': []}, safe=False)

def add_special_offer_by_admin(request):
    return JsonResponse({'q': []}, safe=False)

# def statistics_of_traininng(request):
#     return render(request, "main/group_class_statistics.html", {'a':1})

def add_new_instructor(request):
    return JsonResponse({'q': []}, safe=False)

def delete_new_instructor(request):
    return JsonResponse({'q': []}, safe=False)

def btn_change_instructor(request):

    return JsonResponse({'q': []}, safe=False)

def btn_not_change_instructor(request):
    return JsonResponse({'q': []}, safe=False)


#
#
# def address(request):
#     return render(request, 'main/address.html', address_func(request))
#
# def services(request):
#     return render(request, 'main/services.html', services_func(request))
#
# def get_club_schedule(request):
#     club_id = request.GET.get("club_id")
#     classes_data = form_classes_data(request.user, club_id)
#
#     return JsonResponse({'classes_data': classes_data}, safe=False)
#
# def groupclasses_func(request):
#     classes_data = form_classes_data(request.user, 1)
#     classes = GroupClassesRepository.read_all(request.user)
#     return {'form' : ClubForm(), 'classes_data' : classes_data,
#                                              'classes':classes, 'role': get_role_json(request)}
#
# def groupclasses(request):
#     return render(request, "main/group_classes.html", groupclasses_func(request))
#
# def instructors_list_func(request):
#     """Список инструкторов"""
#     instructors = InstructorsRepository.read_filtered(request.user, {'is_active': True})
#     return {'instructors': instructors, 'form' : ClubForm(), 'role': get_role_json(request)}
#
# def instructors_list(request):
#     return render(request, 'main/instructors.html', instructors_list_func(request))
#
# def instructor_detail(request, pk):
#     return render(request, 'main/instructor_detail.html', instructor_detail_func(request, pk))
#
# def prices(request):
#     return render(request, "main/prices.html", prices_func(request))
#
# # @api_view(['GET', 'POST', 'DELETE'])
# # def prices(request):
# #     if request.method == 'GET':
# #         prices = PricesRepository.read_all(request.user)
# #         for i in prices:
# #             print(i)
# #         p_ser = PricesSerializer(prices)
# #         return JsonResponse(p_ser.data)
#
# def customer_profile(request):
#     return render(request, "main/customer_profile.html", customer_profile_func(request))
#
# def customer_profile_func(request):
#     role = get_role_json(request)
#     is_chart = True
#
#     x = role['customer']['measure_dates']
#     y = role['customer']['measured_weights']
#     if len(x) == 0:
#         is_chart = False
#
#     chart = get_plot(x, y)
#
#     today = datetime.datetime.today().strftime('%Y-%m-%d')
#
#     instructor_action_logs = []
#     have_instructor = False
#     if role['customer']['instructor_id']:
#         have_instructor = True
#         instructor_action_records = InstructorPersonalTrainingsLogsRepository.read_join_filtered(request.user,
#                                                                                                   'instructor',
#                                                                      {'instructor': role['customer']['instructor_id']})
#
#         for cur in instructor_action_records:
#             if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
#                 instructor_action_logs.append(cur)
#
#     group_classes_logs = []
#     admin_action_records = AdminGroupClassesLogsRepository.read_join_filtered(request.user, 'group_class',
#                                                                          {'club': role['user']['club']})
#     for cur in admin_action_records:
#         if cur.act_date + datetime.timedelta(days=7) >= timezone.now():
#             group_classes_logs.append(cur)
#
#     return {'role': get_role_json(request), 'address': address, 'chart': chart,
#                                                           'form':AddMeasureForm(),
#                                                           'today': today,
#                                                           'is_chart': is_chart,
#                                                           'instructor_action_logs': instructor_action_logs,
#                                                           'group_classes_logs': group_classes_logs,
#                                                           'have_instructor': have_instructor}
#
# def edit_customer_profile(request):
#     role = get_role_json(request)
#
#     if request.method == 'POST':
#
#         customer_form = CustomerEditProfileForm(request.POST, instance=role['customer'])
#         customer_form.actual_user = request.user
#
#
#         if customer_form.is_valid():
#
#             CustomersRepository.update_by_pk(request.user,
#                                           role['customer']['pk'],
#                                           customer_form.cleaned_data)
#
#             return redirect('customer_profile')
#     else:
#         customer_form = CustomerEditProfileForm(instance=role['customer'])
#
#     return render(request, 'main/edit_customer.html', {'customer_form': customer_form, 'role': role})
#
# def add_measure(request):
#     weight = request.GET.get("weight")
#     date = request.GET.get("date")
#
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#     old_weights = customer.measured_weights
#     old_dates = customer.measure_dates
#
#     old_weights.append(int(weight))
#     old_dates.append(datetime.datetime.strptime(date, "%Y-%m-%d").date())
#
#     measure = []
#     for i in range(len(old_dates)):
#         measure.append((old_dates[i], old_weights[i]))
#
#     sorted_measure = sorted(measure)
#
#     new_weights = []
#     new_dates = []
#     for i in range(len(sorted_measure)):
#         new_dates.append(sorted_measure[i][0])
#         new_weights.append(sorted_measure[i][1])
#
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': new_weights,
#                                                         'measure_dates': new_dates})
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#
#     is_chart = 1
#     if len(customer.measure_dates) == 0:
#         is_chart = 0
#
#     chart = get_plot(customer.measure_dates, customer.measured_weights)
#     return JsonResponse({'chart': chart, 'is_chart': is_chart}, safe=False)
#
# def delete_measure(request):
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#     weights = customer.measured_weights
#     dates = customer.measure_dates
#
#     if len(dates) > 0:
#         dates.pop(len(dates) - 1)
#         weights.pop(len(dates) - 1)
#
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': weights,
#                                                         'measure_dates': dates})
#     customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
#     is_chart = 1
#     if len(customer.measure_dates) == 0:
#         is_chart = 0
#     chart = get_plot(customer.measure_dates, customer.measured_weights)
#
#     return JsonResponse({'chart': chart, 'is_chart': is_chart}, safe=False)
#
# def customer_training_records(request):
#     return render(request, "main/customer_training_records.html", customer_training_records_func(request))
#
# def delete_personal_training_record(request):
#     record_id = request.GET.get("record_id")
#     InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record_id})
#
#     return JsonResponse({'delete_data': []}, safe=False)
#
# def delete_group_class_record(request):
#     record_id = request.GET.get("record_id")
#     GroupClassesCustomersRecordsRepository.delete_filtered(request.user, {'record_id': record_id})
#
#     return JsonResponse({'delete_data': []}, safe=False)
#
# def add_group_class_record(request):
#     role = get_role_json(request)
#     new_record = GroupClassesCustomersRecords()
#     date_raw = request.GET.get("date")
#     date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()
#     new_record.class_date = date
#     new_record.shedule_id = request.GET.get("shedule_id")
#     new_record.customer_id=role['customer']['customer_id']
#
#
#     GroupClassesCustomersRecordsRepository.create(request.user, new_record)
#     return JsonResponse({'q': []}, safe=False)
#
# def add_personal_training_record(request):
#     i_shedule_id = request.GET.get("i_shedule_id")
#     date_raw = request.GET.get("date")
#     date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()
#
#     new_record = InstructorSheduleCustomers()
#     role = get_role_json(request)
#     new_record.customer_id = role['customer']['customer_id']
#     new_record.training_date = date
#     new_record.i_shedule_id = i_shedule_id
#
#     InstructorSheduleCustomersRepository.create(request.user, new_record)
#     return JsonResponse({'q': []}, safe=False)
#
# def appointment_to_instructor(request):
#     instructor_id = request.GET.get("instructor_id")
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': instructor_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_future_records_for_personal_trainings(request):
#     role = get_role_json(request)
#     instructors_shedule = InstructorSheduleRepository.read_filtered(request.user,
#                                                                     {'instructor_id': role['customer']['instructor_id']})
#     shedule_id_list = []
#     for sh in instructors_shedule:
#         shedule_id_list.append(sh.i_shedule_id)
#
#     records = InstructorSheduleCustomersRepository.read_filtered(request.user, {'i_shedule_id__in': shedule_id_list,
#                                                                                 'customer_id': role['customer']['customer_id']})
#
#     date_today = datetime.date.today()
#     time_today = datetime.datetime.now().time()
#
#     for record in records:
#         if record.training_date > date_today:
#             InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record.record_id})
#         if record.training_date == date_today:
#             shedule_time = InstructorSheduleRepository.read_filtered(request.user,
#                                                                      {'i_shedule_id': record.i_shedule_id})
#             if len(shedule_time) != 0 and shedule_time[0].training_time > time_today:
#                 InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record.record_id})
#
# def delete_appointment_to_instructor(request):
#     delete_future_records_for_personal_trainings(request)
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': None})
#     return JsonResponse({'q': []}, safe=False)
#
# def replace_appointment_to_instructor(request):
#     selected_instructor_id = request.GET.get("instructor_id")
#     delete_future_records_for_personal_trainings(request)
#     CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': selected_instructor_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def instructor_profile(request):
#     return render(request, "main/instructor_profile.html", instructor_profile_func(request))
#
# def instructor_attached_customers_func(request):
#     role = get_role_json(request)
#     customers_data = []
#     customers = CustomersRepository.read_filtered(request.user, {'instructor_id': role['instructor']['instructor_id']})
#     is_chart = True
#
#     for customer in customers:
#         x = customer.measure_dates
#         y = customer.measured_weights
#         if len(x) == 0:
#             is_chart = False
#         chart = get_plot(x, y)
#         customers_data.append({'name': customer.name,
#                                'surname': customer.surname,
#                                'patronymic': customer.patronymic,
#                                'chart': chart,
#                                'is_chart': is_chart,
#                                'day_of_birth': customer.day_of_birth,
#                                'height': customer.height})
#
#     return {'role': role, 'customers_data': customers_data}
#
# def edit_instructor(request):
#     role = get_role_json(request)
#
#     if request.method == 'POST':
#
#         instructor_form = InstructorEditProfileForm(request.POST, request.FILES)
#         instructor_form.actual_user = request.user
#
#         if instructor_form.is_valid():
#
#             admin_record = AdminRecords()
#             admin_record.creation_datetime = datetime.datetime.now()
#             admin_record.status = AdminRecords.PENDING
#             admin_record.instructor = role['instructor']
#             admin_record.admin = role['instructor']['admin']
#             admin_record.change = {}
#
#             new_instructor_data = instructor_form.cleaned_data
#
#
#             old_instructor_data = InstructorsRepository.read_filtered(request.user,
#                                                                       {'instructor_id': role['instructor']['instructor_id']})[0]
#
#             admin_record.change.update({'old_name': old_instructor_data.name})
#             admin_record.change.update({'old_surname': old_instructor_data.surname})
#             admin_record.change.update({'old_patronymic': old_instructor_data.patronymic})
#             admin_record.change.update({'old_education': old_instructor_data.education})
#             admin_record.change.update({'old_experience': old_instructor_data.experience})
#             admin_record.change.update({'old_achievements': old_instructor_data.achievements})
#             admin_record.change.update({'old_specialization': old_instructor_data.specialization})
#             admin_record.change.update({'old_photo': str(old_instructor_data.photo)})
#
#             if (old_instructor_data.name != new_instructor_data['name']):
#                 admin_record.change.update({'new_name': new_instructor_data['name']})
#             else:
#                 admin_record.change.update({'new_name': ''})
#             if (old_instructor_data.surname != new_instructor_data['surname']):
#                 admin_record.change.update({'new_surname': new_instructor_data['surname']})
#             else:
#                 admin_record.change.update({'new_surname': ''})
#             if (old_instructor_data.patronymic != new_instructor_data['patronymic']):
#                 admin_record.change.update({'new_patronymic': new_instructor_data['patronymic']})
#             else:
#                 admin_record.change.update({'new_patronymic': ''})
#             if (old_instructor_data.education != new_instructor_data['education']):
#                 admin_record.change.update({'new_education': new_instructor_data['education']})
#             else:
#                 admin_record.change.update({'new_education': ''})
#             if (old_instructor_data.experience != new_instructor_data['experience']):
#                 admin_record.change.update({'new_experience': new_instructor_data['experience']})
#             else:
#                 admin_record.change.update({'new_experience': ''})
#             if (old_instructor_data.achievements != new_instructor_data['achievements']):
#                 admin_record.change.update({'new_achievements': new_instructor_data['achievements']})
#             else:
#                 admin_record.change.update({'new_achievements': ''})
#             if (old_instructor_data.achievements != new_instructor_data['achievements']):
#                 admin_record.change.update({'new_achievements': new_instructor_data['achievements']})
#             else:
#                 admin_record.change.update({'new_achievements': ''})
#             if (old_instructor_data.specialization != new_instructor_data['specialization']):
#                 admin_record.change.update({'new_specialization': new_instructor_data['specialization']})
#             else:
#                 admin_record.change.update({'new_specialization': ''})
#
#             AdminRecordsRepository.create(request.user, admin_record)
#
#             return redirect('instructor_profile')
#     else:
#         instructor_form = InstructorEditProfileForm(instance=role['instructor'])
#
#     return render(request, 'main/edit_instructor.html', {'instructor_form': instructor_form, 'role': role})
#
# def instructor_add_personal_training(request):
#     day = request.GET.get("day")
#     time_raw = request.GET.get("time")
#     time = datetime.datetime.strptime(time_raw, '%H:%M').time()
#
#     role = get_role_json(request)
#
#     new_record = InstructorShedule()
#
#     new_record.instructor_id = role['instructor']['instructor_id']
#     new_record.training_time = time
#     new_record.day_of_week = day
#
#     InstructorSheduleRepository.create(request.user, new_record)
#
#     return JsonResponse({'q': []}, safe=False)
#
# def instructor_delete_changes(request):
#     pk = request.GET.get("pk")
#     AdminRecordsRepository.delete_by_pk(request.user, pk)
#
#     return JsonResponse({'q': []}, safe=False)
#
# def instructor_delete_personal_training(request):
#     i_shedule_id = request.GET.get("i_shedule_id")
#     InstructorSheduleRepository.delete_filtered(request.user, {'i_shedule_id': i_shedule_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def instructor_attached_customers(request):
#     return render(request, 'main/instructor_attached_customers.html', instructor_attached_customers_func(request))
#
# def instructor_training_records(request):
#     return render(request, "main/instructor_training_records.html", instructor_training_records_func(request))
#
# def admin_profile(request):
#
#     return render(request, "main/admin_profile.html", admin_profile_func(request))
#
# def group_classes_admin(request):
#     return render(request, "main/group_classes_admin.html", group_classes_admin_func(request))
#
# def add_group_class_in_shedule(request):
#     day = request.GET.get("day")
#     time_raw = request.GET.get("time")
#     time = datetime.datetime.strptime(time_raw, '%H:%M').time()
#     instructor_id = request.GET.get("instructor_id")
#     class_id = request.GET.get("class_id")
#     club_id = request.GET.get("club_id")
#     maximum_quantity = request.GET.get("maximum_quantity")
#     busy_instructors_str = request.GET.get("busy_instructors")
#
#     busy_instructors = json.loads(busy_instructors_str)
#
#     if int(instructor_id) in busy_instructors:
#         response = JsonResponse({"error": "there was an error"})
#         response.status_code = 403
#         return response
#
#     new_record = GroupClassesShedule()
#     new_record.class_field = GroupClassesRepository.read_filtered(request.user, {'class_id': class_id})[0]
#     new_record.club = FitnessClubsRepository.read_filtered(request.user, {'club_id': club_id})[0]
#     new_record.instructor = InstructorsRepository.read_filtered(request.user, {'instructor_id': instructor_id})[0]
#     new_record.class_time = time
#     new_record.day_of_week = day
#     new_record.maximum_quantity = int(maximum_quantity)
#
#     GroupClassesSheduleRepository.create(request.user, new_record)
#
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_group_class_in_shedule(request):
#     shedule_id = request.GET.get("shedule_id")
#     GroupClassesSheduleRepository.delete_filtered(request.user, {'shedule_id': shedule_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_special_offer_by_admin(request):
#     offer_id = request.GET.get("offer_id")
#     SpecialOffersRepository.delete_filtered(request.user, {'offer_id': offer_id})
#
#     return JsonResponse({'q': []}, safe=False)
#
# def add_special_offer_by_admin(request):
#     offer_name = request.GET.get("offer_name")
#     offer_description = request.GET.get("offer_description")
#
#     new_record = SpecialOffers()
#     new_record.offer_name = offer_name
#     new_record.offer_description = offer_description
#
#     SpecialOffersRepository.create(request.user, new_record)
#     return JsonResponse({'q': []}, safe=False)
#
# def statistics_of_traininng(request):
#     return render(request, "main/group_class_statistics.html", statistics_of_traininng_func((request)))
#
# def add_new_instructor(request):
#     instructor_id = request.GET.get("instructor_id")
#     InstructorsRepository.update_filtered(request.user, {'instructor_id': instructor_id}, {'is_active': True})
#     return JsonResponse({'q': []}, safe=False)
#
# def delete_new_instructor(request):
#     user_id = request.GET.get("user_id")
#     CustomUserRepository.delete_filtered(request.user, {'id': user_id})
#     return JsonResponse({'q': []}, safe=False)
#
# def btn_change_instructor(request):
#     pk = request.GET.get("pk")
#
#     AdminRecordsRepository.update_by_pk(request.user, pk, {'status': AdminRecords.ACCEPTED})
#     change_dict = {}
#     admin_record = AdminRecordsRepository.read_by_pk(request.user, pk)
#
#     if admin_record.change['new_name'] != '':
#         change_dict.update({'name': admin_record.change['new_name']})
#
#     if admin_record.change['new_surname']:
#         change_dict.update({'surname': admin_record.change['new_surname']})
#
#     if admin_record.change['new_patronymic']:
#         change_dict.update({'patronymic': admin_record.change['new_patronymic']})
#
#     if admin_record.change['new_education']:
#         change_dict.update({'education': admin_record.change['new_education']})
#
#     if admin_record.change['new_experience']:
#         change_dict.update({'experience': admin_record.change['new_experience']})
#
#     if admin_record.change['new_achievements']:
#         change_dict.update({'achievements': admin_record.change['new_achievements']})
#
#     if admin_record.change['new_specialization']:
#         change_dict.update({'specialization': admin_record.change['new_specialization']})
#
#     InstructorsRepository.update_filtered(request.user, {'instructor_id': admin_record.instructor.instructor_id},
#                                           change_dict)
#     return JsonResponse({'q': []}, safe=False)
#
# def btn_not_change_instructor(request):
#     pk = request.GET.get("pk")
#     AdminRecordsRepository.update_by_pk(request.user, pk, {'status': AdminRecords.DECLINED})
#     return JsonResponse({'q': []}, safe=False)
#
