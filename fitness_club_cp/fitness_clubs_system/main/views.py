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
#     return JsonResponse({'q': []}, safe=False)def edit_customer_profile(request)


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
