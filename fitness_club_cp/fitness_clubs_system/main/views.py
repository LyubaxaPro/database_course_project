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
