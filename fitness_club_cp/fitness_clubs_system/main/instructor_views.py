from django.shortcuts import render, redirect
from django.http import JsonResponse

from manager.repositories import GroupClassesRepository, \
    InstructorsRepository, SpecialOffersRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, CustomUserRepository, FitnessClubsRepository, CustomersRepository

from .forms import *
from api.instructor_views import InstructorView, InstructorAttachedCustomersView, InstructorEditProfileView,\
    InstructorEditProfilePostView, InstructorAddPersonalTrainingView, InstructorDeleteProfileChangesView, \
    InstructorDeletePersonalTrainingView, InstructorTrainingRecordsView

def instructor_profile(request):
    view = InstructorView()
    data = view.get(request).data
    return render(request, "main/instructor_profile.html", data)

def instructor_attached_customers(request):
    view = InstructorAttachedCustomersView()
    data = view.get(request).data
    return render(request, 'main/instructor_attached_customers.html', data)


def edit_instructor(request):
    instructor = InstructorsRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]

    if request.method == 'POST':

        instructor_form = InstructorEditProfileForm(request.POST, request.FILES)
        instructor_form.actual_user = request.user

        if instructor_form.is_valid():
            view = InstructorEditProfilePostView()
            cleaned_data = instructor_form.cleaned_data
            view.put(request=request, **cleaned_data)

            return redirect('instructor_profile')
    else:
        view = InstructorEditProfileView()
        data = view.get(request).data
        data['instructor_form'] = InstructorEditProfileForm(instance=instructor)

    return render(request, 'main/edit_instructor.html', data)

def instructor_add_personal_training(request):
    day = request.GET.get("day")
    time_raw = request.GET.get("time")

    view = InstructorAddPersonalTrainingView()
    view.post(request, **{"day": day, "time": time_raw})

    return JsonResponse({'q': []}, safe=False)

def instructor_delete_changes(request):
    pk = request.GET.get("pk")
    view = InstructorDeleteProfileChangesView()
    view.delete(request, **{"pk": pk})

    return JsonResponse({'q': []}, safe=False)

def instructor_delete_personal_training(request):
    i_shedule_id = request.GET.get("i_shedule_id")
    view = InstructorDeletePersonalTrainingView()
    view.delete(request, **{"i_shedule_id": i_shedule_id})

    return JsonResponse({'q': []}, safe=False)

def instructor_training_records(request):
    selected_week = request.GET.get('week_num')
    view = InstructorTrainingRecordsView()
    data = view.get(request, **{"week_num": selected_week}).data
    return render(request, "main/instructor_training_records.html", data)
