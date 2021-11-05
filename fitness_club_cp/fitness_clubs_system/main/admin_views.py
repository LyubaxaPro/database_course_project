from django.shortcuts import render, redirect
from django.http import JsonResponse

from manager.repositories import GroupClassesRepository, \
    InstructorsRepository, SpecialOffersRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, CustomUserRepository, FitnessClubsRepository, CustomersRepository

from .forms import *
from api.admin_views import AdminProfileView, AdminGroupClassesView,\
    AdminDeleteGroupClassesView, AdminDeleteSpecialOfferView, AdminAdminSpecialOfferView, AdminStatisticsView, \
    AdminActivateInstructorView, AdminRejectInstructorView

def admin_profile(request):
    view = AdminProfileView()
    data = view.get(request).data
    return render(request, "main/admin_profile.html", data)

def group_classes_admin(request):
    view = AdminGroupClassesView()
    data = view.get(request).data
    return render(request, "main/group_classes_admin.html", data)

def add_group_class_in_shedule(request):
    day = request.GET.get("day")
    time_raw = request.GET.get("time")
    instructor_id = request.GET.get("instructor_id")
    class_id = request.GET.get("class_id")
    maximum_quantity = request.GET.get("maximum_quantity")
    request.data = {'day':day, 'time': time_raw, 'instructor_id': instructor_id, 'class_id': class_id,
                                  'maximum_quantity': maximum_quantity}
    view = AdminGroupClassesView()
    view.post(request)
    return JsonResponse({'q': []}, safe=False)

def delete_group_class_in_shedule(request):
    shedule_id = request.GET.get("shedule_id")
    view = AdminDeleteGroupClassesView()
    view.delete(request, **{'shedule_id':shedule_id})

    return JsonResponse({'q': []}, safe=False)

def delete_special_offer_by_admin(request):
    offer_id = request.GET.get("offer_id")
    view = AdminDeleteSpecialOfferView()
    view.delete(request, **{'offer_id':offer_id})

    return JsonResponse({'q': []}, safe=False)

def add_special_offer_by_admin(request):
    offer_name = request.GET.get("offer_name")
    offer_description = request.GET.get("offer_description")

    view = AdminAdminSpecialOfferView()
    request.data = {'offer_name':offer_name, 'offer_description': offer_description}
    view.post(request)

    return JsonResponse({'q': []}, safe=False)

def statistics_of_traininng(request):
    week_num = request.GET.get('week_num')
    view = AdminStatisticsView()
    data = view.get(request, **{'week_num': week_num}).data
    return render(request, "main/group_class_statistics.html", data)

def add_new_instructor(request):
    instructor_id = request.GET.get("instructor_id")

    view = AdminActivateInstructorView()
    request.data = {'instructor_id': instructor_id}
    view.patch(request)
    return JsonResponse({'q': []}, safe=False)

def delete_new_instructor(request):
    user_id = request.GET.get("user_id")
    view = AdminRejectInstructorView()
    view.delete(request, **{'user_id': user_id})

    return JsonResponse({'q': []}, safe=False)
