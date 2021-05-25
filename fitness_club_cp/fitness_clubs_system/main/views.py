import time

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
import json
from django.core import serializers

from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, CustomUserRepository, SpecialOffersRepository, PricesRepository,\
    CustomersRepository


from .forms import *

from users.models import FitnessClubs

from manager.models import Instructors
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
    print(club_id)
   # print(classes)


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
    print(classes_data)
    return classes_data

def get_club_schedule(request):
    club_id = request.GET.get("club_id")
    classes_data = form_classes_data(request.user, club_id)

    return JsonResponse({'classes_data': classes_data, 'role': get_role_json(request)}, safe=False)

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


    exp_str = "лет"
    if instructor.experience % 10 == 1 and instructor.experience != 11:
        exp_str = "год"
    elif instructor.experience % 10 in [2, 3, 4] and instructor.experience not in [12, 13, 14]:
        exp_str = "года"
    return render(request, 'main/instructor_detail.html', {'instructor' : instructor,
                                                           'education' : education,
                                                           'achievements' : achievements,
                                                           'specialization' : specialization,
                                                           'exp_str' : exp_str,
                                                           'role': get_role_json(request)})


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
    print(role)

    return render(request, "main/prices.html", {'special_offers': special_offers, 'prices': prices,
                                                'role': role})

def customer_profile(request):
    role = get_role_json(request)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user'].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address

    x = role['customer'].measure_dates
    y = role['customer'].measured_weights

    chart = get_plot(x, y)

    return render(request, "main/customer_profile.html", {'role': get_role_json(request), 'address': address, 'chart': chart})

def instructor_profile(request):
    return render(request, "main/instructor_profile.html", {'role': get_role_json(request)})

def admin_profile(request):
    return render(request, "main/admin_profile.html", {'role': get_role_json(request)})