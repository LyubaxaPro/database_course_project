from django.shortcuts import render, redirect
from django.http import JsonResponse

from manager.repositories import GroupClassesRepository, \
    InstructorsRepository, SpecialOffersRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, CustomUserRepository, FitnessClubsRepository, CustomersRepository

from .forms import *
from api.customer_views import CustomerProfileView, CustomerEditProfileView, CustomerEditProfilePutView, \
    CustomerEditProfileAddMeasureView, CustomerEditProfileDeleteMeasureView, CustomerTrainingRecordsView, \
    CustomerDeletePersonalTrainingRecordView, CustomerDeleteGroupTrainingRecordView, \
    CustomerAddGroupClassesRecordView, CustomerAddPersonalTrainingRecordView, CustomerAppointmentToInstructorView,\
    CustomerDeleteAppointmentToInstructorView, CustomerChangeAppointmentToInstructorView

def customer_profile(request):
    view = CustomerProfileView()
    data = view.get(request).data
    data['form'] = AddMeasureForm()
    return render(request, "main/customer_profile.html", data)

def edit_customer_profile(request):
    customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]

    if request.method == 'POST':
        customer_form = CustomerEditProfileForm(request.POST, instance=customer)
        customer_form.actual_user = request.user
        if customer_form.is_valid():
            view = CustomerEditProfilePutView()
            cleaned_data = customer_form.cleaned_data
            view.put(request=request, **cleaned_data)

            return redirect('customer_profile')
    else:
        view = CustomerEditProfileView()
        data = view.get(request).data
        data['customer_form'] = CustomerEditProfileForm(instance=customer)

    return render(request, 'main/edit_customer.html', data)

def add_measure(request):
    weight = request.GET.get("weight")
    date = request.GET.get("date")

    view = CustomerEditProfileAddMeasureView()
    data = view.put(request, **{'weight': weight, 'date': date}).data
    return JsonResponse(data, safe=False)

def delete_measure(request):
    view = CustomerEditProfileDeleteMeasureView()
    data = view.delete(request).data
    return JsonResponse(data, safe=False)

def customer_training_records(request):
    view = CustomerTrainingRecordsView()
    data = view.get(request).data
    return render(request, "main/customer_training_records.html", data)

def delete_personal_training_record(request):
    record_id = request.GET.get("record_id")
    view = CustomerDeletePersonalTrainingRecordView()
    view.delete(request, **{'record_id': record_id})
    return JsonResponse({'delete_data': []}, safe=False)

def delete_group_class_record(request):
    record_id = request.GET.get("record_id")
    view = CustomerDeleteGroupTrainingRecordView()
    view.delete(request, **{'record_id': record_id})
    return JsonResponse({'delete_data': []}, safe=False)

def add_group_class_record(request):
    date_raw = request.GET.get("date")
    shedule_id = request.GET.get("shedule_id")

    view = CustomerAddGroupClassesRecordView()
    view.post(request, **{'date_raw': date_raw, 'shedule_id': shedule_id})

    return JsonResponse({'q': []}, safe=False)


def add_personal_training_record(request):
    i_shedule_id = request.GET.get("i_shedule_id")
    date_raw = request.GET.get("date")

    view = CustomerAddPersonalTrainingRecordView()
    view.post(request, **{'date_raw': date_raw, 'i_shedule_id': i_shedule_id})

    return JsonResponse({'q': []}, safe=False)

def appointment_to_instructor(request):
    instructor_id = request.GET.get("instructor_id")

    view = CustomerAppointmentToInstructorView()
    view.put(request, **{'instructor_id': instructor_id})

    return JsonResponse({'q': []}, safe=False)

def delete_appointment_to_instructor(request):
    view = CustomerDeleteAppointmentToInstructorView()
    view.delete(request)

    return JsonResponse({'q': []}, safe=False)

def replace_appointment_to_instructor(request):
    instructor_id = request.GET.get("instructor_id")

    view = CustomerChangeAppointmentToInstructorView()
    view.put(request, **{'instructor_id': instructor_id})

    return JsonResponse({'q': []}, safe=False)

