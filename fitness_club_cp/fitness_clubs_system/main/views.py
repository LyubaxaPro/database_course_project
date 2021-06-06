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
    CustomersRepository, InstructorSheduleRepository, GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository,\
    AdministratorsRepository, AdminRecordsRepository


from .forms import *

from manager.models import Instructors, GroupClassesCustomersRecords, InstructorSheduleCustomers, InstructorShedule,\
    GroupClassesShedule, SpecialOffers, AdminRecords
from .utils import get_plot

days = {"Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда", "Thursday": "Четверг", "Friday": "Пятница",
        "Saturday": "Суббота", "Sunday": "Воскресенье"}

def get_role(request):
    customer = None
    is_customer = False
    instructor = None
    is_instructor = False
    is_admin = False
    admin = None
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
            admin = AdministratorsRepository.read_filtered(request.user, {'user': request.user.pk})[0]
            is_guest = False


    return is_customer, customer, is_instructor, instructor, is_admin, admin, is_guest, user

def get_role_json(request):
    is_customer, customer, is_instructor, instructor, is_admin, admin, is_guest, user = get_role(request)
    return {'is_customer': is_customer, 'customer': customer, 'is_instructor': is_instructor, 'instructor': instructor,
            'is_admin': is_admin, 'admin': admin, 'is_guest': is_guest, 'user': user}

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

    for i in range (9, 21):
        data = {}
        for day in days:
            data.update({day: []})
        classes_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600

    for current_class in classes:
        classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week].append({"instructor_name": InstructorsRepository.read_filtered(user,
                                                                                                        {"instructor_id": current_class.instructor_id})[0].name,
                                                                                          "class_name": current_class.class_field.class_name,
                                                                                          'shedule_id': current_class.shedule_id })
    return classes_data

def form_admin_classes_data(user, club_id, week):
    classes = GroupClassesSheduleRepository.read_filtered(user, {"club_id" : int(club_id)})
    dates_raw = get_week_dates(week)

    classes_data = {}
    seconds = 32400
    days_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    days_dates = {}
    for i in range(len(dates_raw)):
        days_dates.update({days_en[i]: dates_raw[i]})

    for i in range (9, 21):
        data = {}
        for day in days:
            data.update({day: {'data': [], 'busy_instructors': json.dumps([])}})
        classes_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600

    for current_class in classes:
        if len(json.loads(classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week]['busy_instructors'])) == 0:
            busy = GroupClassesSheduleRepository.read_filtered(user, {'class_time': current_class.class_time,
                                                                      'day_of_week': current_class.day_of_week,
                                                                      "club_id": int(club_id)})
            instructors = []
            for b in busy:
                instructors.append(b.instructor_id)

            classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week].update({'busy_instructors': json.dumps(instructors)})

        count = len(GroupClassesCustomersRecordsRepository.read_filtered(user, {'shedule_id': current_class.shedule_id,
                                                                                'class_date': days_dates[current_class.day_of_week]}))

        classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week]['data'].append({"instructor_name": InstructorsRepository.read_filtered(user,
                                                                                                        {"instructor_id": current_class.instructor_id})[0].name,
                                                                                          "class_name": current_class.class_field.class_name,
                                                                                          'shedule_id': current_class.shedule_id,
                                                                                          'class_date': days_dates[current_class.day_of_week],
                                                                                                    'count': count})
    day_of_week_date = {}
    for i in range(len(days)):
        day_of_week_date.update({days[days_en[i]]: dates_raw[i]})
    return classes_data, day_of_week_date

def form_data_for_tarif(tarif, week):
    dates_raw = get_week_dates(week)

    classes_data = {}
    seconds = 32400
    days_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_dates = {}
    for i in range(len(dates_raw)):
        days_dates.update({days_week[i]: dates_raw[i]})

    days = tarif.days_of_week
    dates = []
    for day in days:
        dates.append(days_dates[day])

    time_classes = [9, 21]
    if tarif.is_time_restricted:
        time_min = tarif.min_time.hour
        time_max = tarif.max_time.hour
        time_classes = [max(time_min, 9), min(time_max, 21)]
        seconds = 3600 * time_classes[0]

    for i in range (time_classes[0], time_classes[1]):
        data = {}
        for day in days:
            data.update({day: []})
        classes_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600
    return classes_data, seconds, days_dates, days, dates, time_classes

def form_classes_data_for_tarif_group_classes(user, customer_id, club_id, tarif, week):
    classes = GroupClassesSheduleRepository.read_filtered(user, {"club_id": int(club_id)})
    classes_data, seconds, days_dates, days, dates, time_classes = form_data_for_tarif(tarif, week)
    date_today = datetime.date.today()
    time_today = datetime.datetime.now().time()

    for current_class in classes:
        is_in_group_classes_records = False
        is_in_personal_trainings_records = False
        class_not_done = True
        more_than_maximum_quantity = False
        if current_class.class_time.hour >= time_classes[0] and current_class.class_time.hour < time_classes[1] and current_class.day_of_week in days:
            groupclasses = GroupClassesCustomersRecordsRepository.read_filtered(user, {'shedule_id': current_class.shedule_id,
                                                                                       'customer_id': customer_id,
                                                                                       'class_date': days_dates[current_class.day_of_week]})
            if len(groupclasses) != 0:
                is_in_group_classes_records = True

            personal_trainings = InstructorSheduleCustomersRepository.read_filtered(user, {'customer_id': customer_id,
                                                                                       'training_date': days_dates[current_class.day_of_week]})
            if len(personal_trainings) != 0:
                for train in personal_trainings:
                    personal_training_time = InstructorSheduleRepository.read_filtered(user, {'i_shedule_id': train.i_shedule_id})
                    if len(personal_training_time) != 0 and personal_training_time[0].training_time == current_class.class_time:
                        is_in_personal_trainings_records = True

            if days_dates[current_class.day_of_week] < date_today:
                class_not_done = False

            if  days_dates[current_class.day_of_week] == date_today and current_class.class_time < time_today:
                class_not_done = False

            this_groupclasses = GroupClassesCustomersRecordsRepository.read_filtered(user,
                                                                                {'shedule_id': current_class.shedule_id,
                                                                                 'class_date': days_dates[current_class.day_of_week]})
            if len(this_groupclasses) > 0:
                this_class_quantity = GroupClassesSheduleRepository.read_filtered(user, {"shedule_id": current_class.shedule_id})[0].maximum_quantity
                if len(this_groupclasses) >= this_class_quantity:
                    more_than_maximum_quantity = True



            classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week].append({"instructor_name": InstructorsRepository.read_filtered(user,
                                                                                                        {"instructor_id": current_class.instructor_id})[0].name,
                                                                                          "class_name": current_class.class_field.class_name,
                                                                                          'shedule_id': current_class.shedule_id,
                                                                                                'date': str(days_dates[current_class.day_of_week]),
                                                                                                'is_in_group_classes_records': is_in_group_classes_records,
                                                                                                'is_in_personal_trainings_records': is_in_personal_trainings_records,
                                                                                                'class_not_done': class_not_done,
                                                                                                'more_than_maximum_quantity': more_than_maximum_quantity})
    return classes_data, dates

def form_instructors_shedule_for_tarif(user, instructor_id, tarif, week, customer_id):
    shedule = InstructorSheduleRepository.read_filtered(user, {'instructor_id': instructor_id})
    dates_raw = get_week_dates(week)
    training_data = {}

    seconds = 32400
    days_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_dates = {}
    for i in range(len(dates_raw)):
        days_dates.update({days_week[i]: dates_raw[i]})

    days = tarif.days_of_week
    dates = []
    for day in days:
        dates.append(days_dates[day])

    time_classes = [9, 21]
    if tarif.is_time_restricted:
        time_min = tarif.min_time.hour
        time_max = tarif.max_time.hour
        time_classes = [max(time_min, 9), min(time_max, 21)]
        seconds = 3600 * time_classes[0]

    for i in range (time_classes[0], time_classes[1]):
        data = {}
        for day in days:
            data.update({day: []})
        training_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600

    date_today = datetime.date.today()
    time_today = datetime.datetime.now().time()

    for current_shed in shedule:
        is_training_by_customer = False
        is_training_by_other = False
        is_in_group_classes_records = False
        class_not_done = True
        if current_shed.training_time.hour >= time_classes[0] and current_shed.training_time.hour < time_classes[1] and current_shed.day_of_week in days:

            training_by_customer = InstructorSheduleCustomersRepository.read_filtered(user, {'customer_id': customer_id,
                                                                                             'i_shedule_id': current_shed.i_shedule_id,
                                                                                             'training_date': days_dates[current_shed.day_of_week]})
            if len(training_by_customer) != 0:
                is_training_by_customer = True
            else:
                training_by_other = InstructorSheduleCustomersRepository.read_filtered(user, {'i_shedule_id': current_shed.i_shedule_id,
                                                                                             'training_date':days_dates[current_shed.day_of_week]})
                if len(training_by_other) != 0:
                    is_training_by_other = True

            groupclasses = GroupClassesCustomersRecordsRepository.read_filtered(user,
                                                                                {'customer_id': customer_id,
                                                                                 'class_date': days_dates[current_shed.day_of_week]})
            if len(groupclasses) != 0:
                for gr_class in groupclasses:
                    groupclass_time = GroupClassesSheduleRepository.read_filtered(user, {'shedule_id': gr_class.shedule_id})
                    if len(groupclass_time) != 0 and groupclass_time[0].class_time == current_shed.training_time:
                        is_in_group_classes_records = True

            if days_dates[current_shed.day_of_week] < date_today:
                class_not_done = False

            if  days_dates[current_shed.day_of_week] == date_today and current_shed.training_time < time_today:
                class_not_done = False

            training_data[str(current_shed.training_time)[:-3]][current_shed.day_of_week].append({'have_training': True,
                                                                                                  'i_shedule_id': current_shed.i_shedule_id,
                                                                                                  'date': str(days_dates[current_shed.day_of_week]),
                                                                                                  'is_training_by_customer': is_training_by_customer,
                                                                                                  'is_training_by_other': is_training_by_other,
                                                                                                  'is_in_group_classes_records': is_in_group_classes_records,
                                                                                                  'class_not_done': class_not_done
                                                                                                  })

    return training_data, dates

def form_instructors_shedule(user, instructor_id):
    shedule = InstructorSheduleRepository.read_filtered(user, {'instructor_id': instructor_id})
    group_classes = GroupClassesSheduleRepository.read_join_filtered(user, 'class_field', {'instructor_id': instructor_id})
    training_data = {}
    seconds = 32400
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(9, 21):
        data = {}
        for day in days:
            data.update({day: {}})
        training_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600

    for current_shed  in shedule:
        training_data[str(current_shed.training_time)[:-3]][current_shed.day_of_week].update({'name':'Персональная тренировка',
                                                                                              'is_editable': True,
                                                                                              'i_shedule_id': current_shed.i_shedule_id})
    for current_shed in group_classes:
       training_data[str(current_shed.class_time)[:-3]][current_shed.day_of_week].update({'name':current_shed.class_field.class_name,
                                                                                          'is_editable': False})
    return training_data

def form_instructors_shedule_for_week(user, instructor_id, week):
    shedule = InstructorSheduleRepository.read_filtered(user, {'instructor_id': instructor_id})
    group_classes = GroupClassesSheduleRepository.read_join_filtered(user, 'class_field', {'instructor_id': instructor_id})
    training_data = {}
    seconds = 32400
    days_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dates_raw = get_week_dates(week)
    days_dates = {}
    for i in range(len(dates_raw)):
        days_dates.update({days_en[i]: dates_raw[i]})

    for i in range(9, 21):
        data = {}
        for day in days_en:
            data.update({day: {}})
        training_data.update({time.strftime("%H:%M", time.gmtime(seconds)): data})
        seconds += 3600

    for current_shed in shedule:
        customer = None
        customer_raw = InstructorSheduleCustomersRepository.read_filtered(user, {'i_shedule_id': current_shed.i_shedule_id,
                                                                             'training_date': days_dates[current_shed.day_of_week]})

        if len(customer_raw) != 0:
            customer = CustomersRepository.read_filtered(user, {'customer_id': customer_raw[0].customer_id})[0]
        training_data[str(current_shed.training_time)[:-3]][current_shed.day_of_week].update({'name':'Персональная тренировка',
                                                                                              'is_personal': True,
                                                                                              'customer': customer})
    for current_shed in group_classes:

        count = len(GroupClassesCustomersRecordsRepository.read_filtered(user, {'shedule_id': current_shed.shedule_id,
                                                                             'class_date': days_dates[current_shed.day_of_week]}))

        training_data[str(current_shed.class_time)[:-3]][current_shed.day_of_week].update({'name':current_shed.class_field.class_name,
                                                                                          'is_personal': False,
                                                                                           'count': count})
    day_of_week_date = {}
    for i in range(len(days)):
        day_of_week_date.update({days[days_en[i]]: dates_raw[i]})

    return training_data, day_of_week_date

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
    instructors = InstructorsRepository.read_filtered(request.user, {'is_active': True})
    return render(request, 'main/instructors.html', {'instructors': instructors, 'form' : ClubForm(), 'role': get_role_json(request)})

def instructor_detail(request, pk):
    """Информация об инструкторе"""
    instructor =  InstructorsRepository.read_by_pk(request.user, pk)
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

    # instructors = Instructors.objects.filter(user__in=user_id_list)
    instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})
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
    is_chart = True

    x = role['customer'].measure_dates
    y = role['customer'].measured_weights
    if len(x) == 0:
        is_chart = False

    chart = get_plot(x, y)

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    return render(request, "main/customer_profile.html", {'role': get_role_json(request), 'address': address, 'chart': chart,
                                                          'form':AddMeasureForm(),
                                                          'today': today,
                                                          'is_chart': is_chart})


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

    is_chart = 1
    if len(customer.measure_dates) == 0:
        is_chart = 0

    chart = get_plot(customer.measure_dates, customer.measured_weights)
    return JsonResponse({'chart': chart, 'is_chart': is_chart}, safe=False)

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
    is_chart = 1
    if len(customer.measure_dates) == 0:
        is_chart = 0
    chart = get_plot(customer.measure_dates, customer.measured_weights)

    return JsonResponse({'chart': chart, 'is_chart': is_chart}, safe=False)

def get_week():
    my_week_raw = datetime.date.today().isocalendar()
    return str(my_week_raw[0]) + '-W' + str(my_week_raw[1])

def get_week_dates(week):
    date = datetime.datetime.strptime(week + '-1', '%G-W%V-%u').date()
    dates = []
    dates.append(date)
    for i in range(6):
        date += datetime.timedelta(days=1)
        dates.append(date)
    return dates

def customer_training_records(request):
    role = get_role_json(request)
    week = get_week()
    selected_week = request.GET.get('week_num')
    if selected_week:
        week = selected_week
    group_classes_records = GroupClassesCustomersRecordsRepository.read_join_filtered(request.user, "shedule",
                                                                                     {'customer_id': role['customer'].customer_id})
    pass_classes = []
    future_classes = []
    date_today = datetime.date.today()
    time_today = datetime.datetime.now().time()

    for group_class in group_classes_records:

        data = {'date': group_class.class_date, 'day_of_week': days[group_class.shedule.day_of_week],
        'time': group_class.shedule.class_time, 'class_name': group_class.shedule.class_field.class_name,
                'record_id': group_class.record_id}

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
        'time': train.i_shedule.training_time, 'instructor_name': name, 'instructor_pk': instructor.pk, 'record_id': train.record_id}

        if date_today > data['date']:
            pass_personal_trainings.append(data)
        elif date_today > data['date'] and time_today >= data['time']:
            pass_personal_trainings.append(data)
        else:
            future_personal_trainings.append(data)

    tarif = PricesRepository.read_filtered(request.user, {'tariff_id': role['customer'].tariff_id})[0]
    classes_data, dates = form_classes_data_for_tarif_group_classes(request.user, role['customer'].customer_id, role['user'].club, tarif, week)

    trainings_data = []
    instructor_data = {}
    have_instructor = False
    if role['customer'].instructor_id:
        trainings_data, dates = form_instructors_shedule_for_tarif(request.user, role['customer'].instructor_id, tarif, week, role['customer'].customer_id)
        have_instructor = True
        customers_instructor = InstructorsRepository.read_filtered(request.user, {'instructor_id': role['customer'].instructor_id})[0]
        instructor_data = {'instructor_name': customers_instructor.name, 'instructor_surname': customers_instructor.surname,
                            'instructor_patronymic': customers_instructor.patronymic,
                            'instructor_pk': customers_instructor.pk}


    day_of_week_date = {}
    for i in range(len(tarif.days_of_week)):
        day_of_week_date.update({days[tarif.days_of_week[i]]: dates[i]})

    club_id = role['user'].club
    users_instructors = CustomUserRepository.read_filtered(request.user, {"club": club_id, 'role': 1})
    user_id_list = []
    for user in users_instructors:
        user_id_list.append(user.id)
    club_instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})
    club_instructors_data = []
    for instr in club_instructors:
        data = {'name': instr.name, 'surname': instr.surname, 'patronimyc': instr.patronymic,
                'instructor_id': instr.instructor_id,
                'instructor_pk': instr.pk
                }
        club_instructors_data.append(data)
    context = {'role': get_role_json(request), 'pass_group_classes': pass_classes,
     'future_group_classes': future_classes,
     'pass_personal_trainings': pass_personal_trainings,
     'future_personal_trainings': future_personal_trainings,
     'classes_data': classes_data,
     'day_of_week_date': day_of_week_date,
    'current_week': week,
    'trainings_data': trainings_data,
    'have_instructor': have_instructor,
    'instructor_data': instructor_data,
    'club_instructors_data': club_instructors_data
     }

    return render(request, "main/customer_training_records.html", context)

def delete_personal_training_record(request):
    record_id = request.GET.get("record_id")
    InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record_id})

    return JsonResponse({'delete_data': []}, safe=False)

def delete_group_class_record(request):
    record_id = request.GET.get("record_id")
    GroupClassesCustomersRecordsRepository.delete_filtered(request.user, {'record_id': record_id})

    return JsonResponse({'delete_data': []}, safe=False)

def add_group_class_record(request):
    role = get_role_json(request)
    new_record = GroupClassesCustomersRecords()
    date_raw = request.GET.get("date")
    date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()
    new_record.class_date = date
    new_record.shedule_id = request.GET.get("shedule_id")
    new_record.customer_id=role['customer'].customer_id


    GroupClassesCustomersRecordsRepository.create(request.user, new_record)
    return JsonResponse({'q': []}, safe=False)

def add_personal_training_record(request):
    i_shedule_id = request.GET.get("i_shedule_id")
    date_raw = request.GET.get("date")
    date = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date()

    new_record = InstructorSheduleCustomers()
    role = get_role_json(request)
    new_record.customer_id = role['customer'].customer_id
    new_record.training_date = date
    new_record.i_shedule_id = i_shedule_id

    InstructorSheduleCustomersRepository.create(request.user, new_record)
    return JsonResponse({'q': []}, safe=False)

def appointment_to_instructor(request):
    instructor_id = request.GET.get("instructor_id")
    CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': instructor_id})

    return JsonResponse({'q': []}, safe=False)

def delete_future_records_for_personal_trainings(request):
    role = get_role_json(request)
    instructors_shedule = InstructorSheduleRepository.read_filtered(request.user,
                                                                    {'instructor_id': role['customer'].instructor_id})
    shedule_id_list = []
    for sh in instructors_shedule:
        shedule_id_list.append(sh.i_shedule_id)

    records = InstructorSheduleCustomersRepository.read_filtered(request.user, {'i_shedule_id__in': shedule_id_list,
                                                                                'customer_id': role['customer'].customer_id})

    date_today = datetime.date.today()
    time_today = datetime.datetime.now().time()

    for record in records:
        if record.training_date > date_today:
            InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record.record_id})
        if record.training_date == date_today:
            shedule_time = InstructorSheduleRepository.read_filtered(request.user,
                                                                     {'i_shedule_id': record.i_shedule_id})
            if len(shedule_time) != 0 and shedule_time[0].training_time > time_today:
                InstructorSheduleCustomersRepository.delete_filtered(request.user, {'record_id': record.record_id})


def delete_appointment_to_instructor(request):
    delete_future_records_for_personal_trainings(request)
    CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': None})
    return JsonResponse({'q': []}, safe=False)

def replace_appointment_to_instructor(request):
    selected_instructor_id = request.GET.get("instructor_id")
    delete_future_records_for_personal_trainings(request)
    CustomersRepository.update_filtered(request.user, {'user_id': request.user.pk}, {'instructor_id': selected_instructor_id})

    return JsonResponse({'q': []}, safe=False)


def instructor_profile(request):
    """Профиль инструктора"""
    role = get_role_json(request)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user'].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address
    instructor_shedule = form_instructors_shedule(request.user, role['instructor'].instructor_id)

    exp_str = "лет"
    if role['instructor'].experience % 10 == 1 and role['instructor'].experience != 11:
        exp_str = "год"
    elif role['instructor'].experience % 10 in [2, 3, 4] and role['instructor'].experience not in [12, 13, 14]:
        exp_str = "года"

    record = AdminRecordsRepository.read_filtered(request.user, {'instructor': role['instructor'],
                                                                 'status': AdminRecords.PENDING})
    change_record = None
    is_already_record = False
    if record:
        is_already_record = True
        change_record = record[0]

    return render(request, "main/instructor_profile.html",
                  {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                   'exp_str': exp_str,
                   'is_already_record': is_already_record,
                   'change_record': change_record})

def edit_instructor(request):
    role = get_role_json(request)

    if request.method == 'POST':

        instructor_form = InstructorProfileForm(request.POST, instance=role['customer'])
        instructor_form.actual_user = request.user

        if instructor_form.is_valid():

            admin_record = AdminRecords()
            admin_record.creation_datetime = datetime.datetime.now()
            admin_record.status = AdminRecords.PENDING
            admin_record.instructor = role['instructor']
            admin_record.admin = role['instructor'].admin
            admin_record.change = {}

            new_instructor_data = instructor_form.cleaned_data


            old_instructor_data = InstructorsRepository.read_filtered(request.user,
                                                                      {'instructor_id': role['instructor'].instructor_id})[0]

            admin_record.change.update({'old_name': old_instructor_data.name})
            admin_record.change.update({'old_surname': old_instructor_data.surname})
            admin_record.change.update({'old_patronymic': old_instructor_data.patronymic})
            admin_record.change.update({'old_education': old_instructor_data.education})
            admin_record.change.update({'old_experience': old_instructor_data.experience})
            admin_record.change.update({'old_achievements': old_instructor_data.achievements})
            admin_record.change.update({'old_specialization': old_instructor_data.specialization})
            admin_record.change.update({'old_photo': str(old_instructor_data.photo)})

            if (old_instructor_data.name != new_instructor_data['name']):
                admin_record.change.update({'new_name': new_instructor_data['name']})
            else:
                admin_record.change.update({'new_name': ''})
            if (old_instructor_data.surname != new_instructor_data['surname']):
                admin_record.change.update({'new_surname': new_instructor_data['surname']})
            else:
                admin_record.change.update({'new_surname': ''})
            if (old_instructor_data.patronymic != new_instructor_data['patronymic']):
                admin_record.change.update({'new_patronymic': new_instructor_data['patronymic']})
            else:
                admin_record.change.update({'new_patronymic': ''})
            if (old_instructor_data.education != new_instructor_data['education']):
                admin_record.change.update({'new_education': new_instructor_data['education']})
            else:
                admin_record.change.update({'new_education': ''})
            if (old_instructor_data.experience != new_instructor_data['experience']):
                admin_record.change.update({'new_experience': new_instructor_data['experience']})
            else:
                admin_record.change.update({'new_experience': ''})
            if (old_instructor_data.achievements != new_instructor_data['achievements']):
                admin_record.change.update({'new_achievements': new_instructor_data['achievements']})
            else:
                admin_record.change.update({'new_achievements': ''})
            if (old_instructor_data.achievements != new_instructor_data['achievements']):
                admin_record.change.update({'new_achievements': new_instructor_data['achievements']})
            else:
                admin_record.change.update({'new_achievements': ''})
            if (old_instructor_data.specialization != new_instructor_data['specialization']):
                admin_record.change.update({'new_specialization': new_instructor_data['specialization']})
            else:
                admin_record.change.update({'new_specialization': ''})
            if (old_instructor_data.photo != new_instructor_data['photo']):
                if new_instructor_data['photo'] != 'images/default.jpg':
                    admin_record.change.update({'new_photo': str(new_instructor_data['photo'])})
                else:
                    admin_record.change.update({'new_photo': ''})
            else:
                admin_record.change.update({'new_photo': ''})

            AdminRecordsRepository.create(request.user, admin_record)

            return redirect('instructor_profile')
    else:
        instructor_form = InstructorProfileForm(instance=role['instructor'])

    return render(request, 'main/edit_instructor.html', {'instructor_form': instructor_form, 'role': role})

def instructor_add_personal_training(request):
    day = request.GET.get("day")
    time_raw = request.GET.get("time")
    time = datetime.datetime.strptime(time_raw, '%H:%M').time()

    role = get_role_json(request)

    new_record = InstructorShedule()

    new_record.instructor_id = role['instructor'].instructor_id
    new_record.training_time = time
    new_record.day_of_week = day

    InstructorSheduleRepository.create(request.user, new_record)

    return JsonResponse({'q': []}, safe=False)

def instructor_delete_changes(request):
    pk = request.GET.get("pk")
    AdminRecordsRepository.delete_by_pk(request.user, pk)

    return JsonResponse({'q': []}, safe=False)

def instructor_delete_personal_training(request):
    i_shedule_id = request.GET.get("i_shedule_id")
    InstructorSheduleRepository.delete_filtered(request.user, {'i_shedule_id': i_shedule_id})

    return JsonResponse({'q': []}, safe=False)

def instructor_attached_customers(request):
    role = get_role_json(request)
    customers_data = []
    customers = CustomersRepository.read_filtered(request.user, {'instructor_id': role['instructor'].instructor_id})
    is_chart = True

    for customer in customers:
        x = customer.measure_dates
        y = customer.measured_weights
        if len(x) == 0:
            is_chart = False
        chart = get_plot(x, y)
        customers_data.append({'name': customer.name,
                               'surname': customer.surname,
                               'patronymic': customer.patronymic,
                               'chart': chart,
                               'is_chart': is_chart,
                               'day_of_birth': customer.day_of_birth,
                               'height': customer.height})

    return render(request, 'main/instructor_attached_customers.html', {'role': role, 'customers_data': customers_data})

def instructor_training_records(request):
    role = get_role_json(request)
    week = get_week()
    selected_week = request.GET.get('week_num')
    if selected_week:
        week = selected_week
    instructor_shedule, day_of_week_date = form_instructors_shedule_for_week(request.user, role['instructor'].instructor_id, week)


    return render(request, "main/instructor_training_records.html",
                  {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                   'day_of_week_date': day_of_week_date,
                   'current_week': week})

def admin_profile(request):
    role = get_role_json(request)
    fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user'].club})
    address = fitness_club[0].city + ", " + fitness_club[0].address

    admin = AdministratorsRepository.read_filtered(request.user, {'user': role['admin']})[0]

    users_instructors = CustomUserRepository.read_filtered(request.user, {"club": role['user'].club, 'role': 1})
    user_id_list = []
    for user in users_instructors:
        user_id_list.append(user.id)

    instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': False})

    instructors_data = []
    for instructor in instructors:
        user = CustomUserRepository.read_filtered(request.user, {'id': instructor.user_id})[0]
        instructors_data.append({'data': instructor, 'user': user})

    changes_instructors = AdminRecordsRepository.read_filtered(request.user, {'admin': role['admin'].user_id,
                                                                              'status': AdminRecords.PENDING})


    return render(request, "main/admin_profile.html", {'role': role, 'address': address,
                                                       'admin': admin, 'instructors': instructors_data,
                                                       'changes_instructors': changes_instructors})

def group_classes_admin(request):
    week = get_week()
    role = get_role_json(request)
    club_id = role['user'].club
    classes_data, day_dates = form_admin_classes_data(request.user, club_id, week)

    club_info = FitnessClubsRepository.read_filtered(request.user, {'club_id': club_id})[0]
    address = club_info.city + ", " + club_info.address

    classes = GroupClassesRepository.read_all(request.user)

    users = CustomUserRepository.read_filtered(request.user, {"club": club_id})
    user_id_list = []
    for user in users:
        user_id_list.append(user.id)

    instructors = InstructorsRepository.read_filtered(request.user, {'user__in': user_id_list, 'is_active': True})

    return render(request, "main/group_classes_admin.html", {'classes_data' : classes_data,
                                                       'classes':classes, 'role': role,
                                                             'address': address, 'instructors': instructors,
                                                             'club_id': club_id})

def add_group_class_in_shedule(request):
    day = request.GET.get("day")
    time_raw = request.GET.get("time")
    time = datetime.datetime.strptime(time_raw, '%H:%M').time()
    instructor_id = request.GET.get("instructor_id")
    class_id = request.GET.get("class_id")
    club_id = request.GET.get("club_id")
    maximum_quantity = request.GET.get("maximum_quantity")
    busy_instructors_str = request.GET.get("busy_instructors")

    busy_instructors = json.loads(busy_instructors_str)

    if int(instructor_id) in busy_instructors:
        response = JsonResponse({"error": "there was an error"})
        response.status_code = 403
        return response

    new_record = GroupClassesShedule()
    new_record.class_field = GroupClassesRepository.read_filtered(request.user, {'class_id': class_id})[0]
    new_record.club = FitnessClubsRepository.read_filtered(request.user, {'club_id': club_id})[0]
    new_record.instructor = InstructorsRepository.read_filtered(request.user, {'instructor_id': instructor_id})[0]
    new_record.class_time = time
    new_record.day_of_week = day
    new_record.maximum_quantity = int(maximum_quantity)

    GroupClassesSheduleRepository.create(request.user, new_record)

    return JsonResponse({'q': []}, safe=False)

def delete_group_class_in_shedule(request):
    shedule_id = request.GET.get("shedule_id")
    GroupClassesSheduleRepository.delete_filtered(request.user, {'shedule_id': shedule_id})


    return JsonResponse({'q': []}, safe=False)


def delete_special_offer_by_admin(request):
    offer_id = request.GET.get("offer_id")
    SpecialOffersRepository.delete_filtered(request.user, {'offer_id': offer_id})

    return JsonResponse({'q': []}, safe=False)

def add_special_offer_by_admin(request):
    offer_name = request.GET.get("offer_name")
    offer_description = request.GET.get("offer_description")

    new_record = SpecialOffers()
    new_record.offer_name = offer_name
    new_record.offer_description = offer_description

    SpecialOffersRepository.create(request.user, new_record)
    return JsonResponse({'q': []}, safe=False)

def statistics_of_traininng(request):
    week = get_week()
    selected_week = request.GET.get('week_num')
    if selected_week:
        week = selected_week

    role = get_role_json(request)
    club_id = role['user'].club
    classes_data, day_of_week_date = form_admin_classes_data(request.user, club_id, week)

    club_info = FitnessClubsRepository.read_filtered(request.user, {'club_id': club_id})[0]
    address = club_info.city + ", " + club_info.address

    classes = GroupClassesRepository.read_all(request.user)

    users = CustomUserRepository.read_filtered(request.user, {"club": club_id})
    user_id_list = []
    for user in users:
        user_id_list.append(user.id)


    return render(request, "main/group_class_statistics.html", {'classes_data': classes_data,
                                                             'classes': classes, 'role': role,
                                                             'address': address,
                                                             'club_id': club_id,
                                                             'day_of_week_date': day_of_week_date,
                                                                'current_week': week})

def add_new_instructor(request):
    instructor_id = request.GET.get("instructor_id")
    InstructorsRepository.update_filtered(request.user, {'instructor_id': instructor_id}, {'is_active': True})
    return JsonResponse({'q': []}, safe=False)

def delete_new_instructor(request):
    user_id = request.GET.get("user_id")
    CustomUserRepository.delete_filtered(request.user, {'id': user_id})
    return JsonResponse({'q': []}, safe=False)


def btn_change_instructor(request):
    pk = request.GET.get("pk")

    AdminRecordsRepository.update_by_pk(request.user, pk, {'status': AdminRecords.ACCEPTED})
    change_dict = {}
    admin_record = AdminRecordsRepository.read_by_pk(request.user, pk)

    if admin_record.change['new_name'] != '':
        change_dict.update({'name': admin_record.change['new_name']})

    if admin_record.change['new_surname']:
        change_dict.update({'surname': admin_record.change['new_surname']})

    if admin_record.change['new_patronymic']:
        change_dict.update({'patronymic': admin_record.change['new_patronymic']})

    if admin_record.change['new_education']:
        change_dict.update({'education': admin_record.change['new_education']})

    if admin_record.change['new_experience']:
        change_dict.update({'experience': admin_record.change['new_experience']})

    if admin_record.change['new_achievements']:
        change_dict.update({'achievements': admin_record.change['new_achievements']})

    if admin_record.change['new_specialization']:
        change_dict.update({'specialization': admin_record.change['new_specialization']})

    if admin_record.change['new_photo']:
        change_dict.update({'photo': admin_record.change.new_photo})

    InstructorsRepository.update_filtered(request.user, {'instructor_id': admin_record.instructor.instructor_id},
                                          change_dict)
    return JsonResponse({'q': []}, safe=False)

def btn_not_change_instructor(request):
    pk = request.GET.get("pk")
    AdminRecordsRepository.update_by_pk(request.user, pk, {'status': AdminRecords.DECLINED})
    return JsonResponse({'q': []}, safe=False)


