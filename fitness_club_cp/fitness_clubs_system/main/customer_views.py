from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers

from manager.repositories import GroupClassesRepository, \
    InstructorsRepository, SpecialOffersRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, CustomUserRepository, FitnessClubsRepository, CustomersRepository

from .forms import *
from api.customer_views import CustomerProfileView, CustomerEditProfileView, CustomerEditProfilePutView, \
    CustomerEditProfileAddMeasureView, CustomerEditProfileDeleteMeasureView

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

