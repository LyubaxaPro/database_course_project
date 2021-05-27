import datetime
import time

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
import json
from django.core import serializers

from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository


from .forms import *

from manager.models import Instructors, GroupClassesCustomersRecords
from .utils import get_plot

def get_role(request):
    customer = None
    is_customer = False
    instructor = None
    is_instructor = False
    is_admin = False
    is_guest = True
    user = None

    if request.user.pk:
        user = CustomUserRepository.read_filtered(request.user, {'email': CustomUserRepository.read_by_pk(request.user, request.user.pk)})[0]
        if user.role == 0:
            customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
            is_customer = True
            is_guest = False
        elif user.role == 1:
            instructor = InstructorsRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
            is_instructor = True
            is_guest = False
        elif user.role == 2 or user.role == 3:
            is_admin = True
            is_guest = False

    return is_customer, customer, is_instructor, instructor, is_admin, is_guest, user

def get_role_json(request):
    is_customer, customer, is_instructor, instructor, is_admin, is_guest, user = get_role(request)
    return {'is_customer': is_customer, 'customer': customer, 'is_instructor': is_instructor, 'instructor': instructor,
            'is_admin': is_admin, 'is_guest': is_guest, 'user': user}

def index(request):
    data = {
        'title': 'Главная страница',
        'role': get_role_json(request)
    }
    return render(request, 'main/index.html', data)

def address(request):
    clubs = FitnessClubsRepository()
    data = {
        'clubs' : clubs.read_all(request.user),
        'role': get_role_json(request)
    }
    return render(request, 'main/address.html', data)


def services(request):
    services = ServicesRepository()
    data = {
        'services': services.read_all(request.user),
        'role': get_role_json(request)
    }
    return render(request, 'main/services.html', data)

def form_classes_data(user, club_id):
    classes = GroupClassesSheduleRepository.read_filtered(user, {"club_id" : int(club_id)})

    classes_data = {}
    seconds = 32400
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(9, 21):
        data = {}
        for day in days:
            data.update({day: []})
        classes_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600

    for current_class  in classes:
        classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week].append({"instructor_name": InstructorsRepository.read_filtered(user,
                                                                                                        {"instructor_id": current_class.instructor_id})[0].name,
                                                                                          "class_name": current_class.class_field.class_name})
    return classes_data

def form_instructors_shedule(user, instructor_id):
    shedule = InstructorSheduleRepository.read_filtered(user, {'instructor_id': instructor_id})
    training_data = {}
    seconds = 32400
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(9, 21):
        data = {}
        for day in days:
            data.update({day: []})
        training_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600

    for current_shed  in shedule:
        training_data[str(current_shed.training_time)[:-3]][current_shed.day_of_week].append(True)
    return training_data

def get_club_schedule(request):
    club_id = request.GET.get("club_id")
    classes_data = form_classes_data(request.user, club_id)

    return JsonResponse({'classes_data': classes_data}, safe=False)

def groupclasses(request):
    classes_data = form_classes_data(request.user, 1)

    classes = GroupClassesRepository.read_all(request.user)
    return render(request, "main/group_classes.html", {'form' : ClubForm(), 'classes_data' : classes_data,
                                                       'classes':classes, 'role': get_role_json(request)})


def instructors_list(request):
    """Список инструкторов"""
    instructors = InstructorsRepository.read_all(request.user)
    return render(request, 'main/instructors.html', {'instructors': instructors, 'form' : ClubForm(), 'role': get_role_json(request)})

def instructor_detail(request, pk):
    """Информация об инструкторе"""
    instructor =  InstructorsRepository.read_by_pk(request.user, pk)
    education = list(map(lambda x: x.strip("'"), instructor.education))
    achievements = list(map(lambda x: x.strip("'"), instructor.achievements))
    specialization = list(map(lambda x: x.strip("'"), instructor.specialization))
    instructor_shedule = form_instructors_shedule(request.user, instructor.instructor_id)

    exp_str = "лет"
    if instructor.experience % 10 == 1 and instructor.experience != 11:
        exp_str = "год"
    elif instructor.experience % 10 in [2, 3, 4] and instructor.experience not in [12, 13, 14]:
        exp_str = "года"

    user = CustomUserRepository.read_filtered(request.user, {'id': instructor.user_id})

    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': user[0].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address

    return render(request, 'main/instructor_detail.html', {'instructor' : instructor,
                                                           'education' : education,
                                                           'achievements' : achievements,
                                                           'specialization' : specialization,
                                                           'exp_str' : exp_str,
                                                           'role': get_role_json(request),
                                                           'shedule': instructor_shedule,
                                                           'address': address})

def get_club_instructors(request):
    club_id = request.GET.get("club_id")
    users = CustomUserRepository.read_filtered(request.user, {"club" : club_id})
    user_id_list = []
    for user in users:
        user_id_list.append(user.id)

    instructors = Instructors.objects.filter(user__in=user_id_list)
    instructors_json = serializers.serialize('json', list(instructors))


    return JsonResponse({'filtered_instructors': instructors_json}, safe=False)


def prices(request):
    special_offers = SpecialOffersRepository.read_all(request.user)
    prices = PricesRepository.read_all(request.user)
    role = get_role_json(request)

    return render(request, "main/prices.html", {'special_offers': special_offers, 'prices': prices,
                                                'role': role})

def customer_profile(request):
    role = get_role_json(request)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user'].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address

    x = role['customer'].measure_dates
    y = role['customer'].measured_weights

    chart = get_plot(x, y)

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    return render(request, "main/customer_profile.html", {'role': get_role_json(request), 'address': address, 'chart': chart,
                                                          'form':AddMeasureForm(),
                                                          'today': today})


def edit_customer_profile(request):
    role = get_role_json(request)

    if request.method == 'POST':

        customer_form = CustomerProfileForm(request.POST, instance=role['customer'])
        customer_form.actual_user = request.user

        if customer_form.is_valid():
            CustomersRepository.update_by_pk(request.user,
                                          role['customer'].pk,
                                          customer_form.cleaned_data)

            return redirect('customer_profile')
    else:
        customer_form = CustomerProfileForm(instance=role['customer'])

    return render(request, 'main/edit_customer.html', {'customer_form': customer_form, 'role': role})


def add_measure(request):
    weight = request.GET.get("weight")
    date = request.GET.get("date")

    customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
    old_weights = customer.measured_weights
    old_dates = customer.measure_dates

    old_weights.append(int(weight))
    old_dates.append(datetime.datetime.strptime(date, "%Y-%m-%d").date())

    measure = []
    for i in range(len(old_dates)):
        measure.append((old_dates[i], old_weights[i]))

    sorted_measure = sorted(measure)

    new_weights = []
    new_dates = []
    for i in range(len(sorted_measure)):
        new_dates.append(sorted_measure[i][0])
        new_weights.append(sorted_measure[i][1])

    CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': new_weights,
                                                        'measure_dates': new_dates})
    customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]

    chart = get_plot(customer.measure_dates, customer.measured_weights)

    return JsonResponse({'chart': chart}, safe=False)

def delete_measure(request):
    customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]
    weights = customer.measured_weights
    dates = customer.measure_dates

    if len(dates) > 0:
        dates.pop(len(dates) - 1)
        weights.pop(len(dates) - 1)

    CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'measured_weights': weights,
                                                        'measure_dates': dates})
    customer = CustomersRepository.read_filtered(request.user, {'user_id': request.user.pk})[0]

    chart = get_plot(customer.measure_dates, customer.measured_weights)

    return JsonResponse({'chart': chart}, safe=False)



def customer_training_records(request):
    role = get_role_json(request)
    group_classes_records = GroupClassesCustomersRecordsRepository.read_join_filtered(request.user, "shedule",
                                                                                     {'customer_id': role['customer'].customer_id})

    days = {"Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда", "Thursday": "Четверг", "Friday": "Пятница",
            "Saturday": "Суббота", "Sunday": "Воскресенье"}
    pass_classes = []
    future_classes = []
    date_today = datetime.date.today()
    time_today = datetime.datetime.now().time()

    for group_class in group_classes_records:

        data = {'date': group_class.class_date, 'day_of_week': days[group_class.shedule.day_of_week],
        'time': group_class.shedule.class_time, 'class_name': group_class.shedule.class_field.class_name}

        if date_today > data['date']:
            pass_classes.append(data)
        elif date_today == data['date'] and time_today >= data['time']:
            pass_classes.append(data)
        else:
            future_classes.append(data)

    personal_records = InstructorSheduleCustomersRepository.read_join_filtered(request.user, "i_shedule",
                                                                               {'customer_id': role['customer'].customer_id})

    pass_personal_trainings = []
    future_personal_trainings = []

    for train in personal_records:
        instructor = InstructorsRepository.read_filtered(request.user, {'instructor_id': train.i_shedule.instructor_id})[0]
        name = instructor.surname + " " + instructor.name + " " + instructor.patronymic
        data = {'date': train.training_date, 'day_of_week': days[train.i_shedule.day_of_week],
        'time': train.i_shedule.training_time, 'instructor_name': name, 'instructor_pk': instructor.pk}

        if date_today > data['date']:
            pass_personal_trainings.append(data)
        elif date_today > data['date'] and time_today >= data['time']:
            pass_personal_trainings.append(data)
        else:
            future_personal_trainings.append(data)

    return render(request, "main/customer_training_records.html", {'role': get_role_json(request), 'pass_group_classes': pass_classes,
                                                                   'future_group_classes': future_classes,
                                                                   'pass_personal_trainings': pass_personal_trainings,
                                                                   'future_personal_trainings': future_personal_trainings})

def instructor_profile(request):
    return render(request, "main/instructor_profile.html", {'role': get_role_json(request)})

def admin_profile(request):
    return render(request, "main/admin_profile.html", {'role': get_role_json(request)})

