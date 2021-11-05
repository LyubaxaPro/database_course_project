from manager.repositories import ServicesService, FitnessClubsService, GroupClassesService,\
    GroupClassesSheduleService, InstructorsService, CustomUserService, SpecialOffersService, PricesService,\
    CustomersService, InstructorSheduleService, GroupClassesCustomersRecordsService, InstructorSheduleCustomersService,\
    AdministratorsService, AdminRecordsService, InstructorPersonalTrainingsLogsService, AdminGroupClassesLogsService

from .week import *
import json

def form_classes_data(user, club_id):
    classes = GroupClassesSheduleService.read_filtered(user, {"club_id" : int(club_id)})

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
        classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week].append({"instructor_name":InstructorsService.read_filtered(user,
                                                                                                        {"instructor_id": current_class.instructor_id})[0].name,
                                                                                          "class_name": current_class.class_field.class_name,
                                                                                          'shedule_id': current_class.shedule_id })
    return classes_data

def form_admin_classes_data(user, club_id, week):
    classes = GroupClassesSheduleService.read_filtered(user, {"club_id" : int(club_id)})
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
            busy = GroupClassesSheduleService.read_filtered(user, {'class_time': current_class.class_time,
                                                                      'day_of_week': current_class.day_of_week,
                                                                      "club_id": int(club_id)})
            instructors = []
            for b in busy:
                instructors.append(b.instructor_id)

            classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week].update({'busy_instructors': json.dumps(instructors)})

        count = len(GroupClassesCustomersRecordsService.read_filtered(user, {'shedule_id': current_class.shedule_id,
                                                                                'class_date': days_dates[current_class.day_of_week]}))

        classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week]['data'].append({"instructor_name": InstructorsService.read_filtered(user,
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
    classes = GroupClassesSheduleService.read_filtered(user, {"club_id": int(club_id)})
    classes_data, seconds, days_dates, days, dates, time_classes = form_data_for_tarif(tarif, week)
    date_today = datetime.date.today()
    time_today = datetime.datetime.now().time()

    for current_class in classes:
        is_in_group_classes_records = False
        is_in_personal_trainings_records = False
        class_not_done = True
        more_than_maximum_quantity = False
        if current_class.class_time.hour >= time_classes[0] and current_class.class_time.hour < time_classes[1] and current_class.day_of_week in days:
            groupclasses = GroupClassesCustomersRecordsService.read_filtered(user, {'shedule_id': current_class.shedule_id,
                                                                                       'customer_id': customer_id,
                                                                                       'class_date': days_dates[current_class.day_of_week]})
            if len(groupclasses) != 0:
                is_in_group_classes_records = True

            personal_trainings = InstructorSheduleCustomersService.read_filtered(user, {'customer_id': customer_id,
                                                                                       'training_date': days_dates[current_class.day_of_week]})
            if len(personal_trainings) != 0:
                for train in personal_trainings:
                    personal_training_time = InstructorSheduleService.read_filtered(user, {'i_shedule_id': train.i_shedule_id})
                    if len(personal_training_time) != 0 and personal_training_time[0].training_time == current_class.class_time:
                        is_in_personal_trainings_records = True

            if days_dates[current_class.day_of_week] < date_today:
                class_not_done = False

            if  days_dates[current_class.day_of_week] == date_today and current_class.class_time < time_today:
                class_not_done = False

            this_groupclasses = GroupClassesCustomersRecordsService.read_filtered(user,
                                                                                {'shedule_id': current_class.shedule_id,
                                                                                 'class_date': days_dates[current_class.day_of_week]})
            if len(this_groupclasses) > 0:
                this_class_quantity = GroupClassesSheduleService.read_filtered(user, {"shedule_id": current_class.shedule_id})[0].maximum_quantity
                if len(this_groupclasses) >= this_class_quantity:
                    more_than_maximum_quantity = True



            classes_data[str(current_class.class_time)[:-3]][current_class.day_of_week].append({"instructor_name": InstructorsService.read_filtered(user,
                                                                                                        {"instructor_id": current_class.instructor_id})[0].name,
                                                                                          "class_name": current_class.class_field.class_name,
                                                                                          'shedule_id': current_class.shedule_id,
                                                                                                'date': str(days_dates[current_class.day_of_week]),
                                                                                                'is_in_group_classes_records': is_in_group_classes_records,
                                                                                                'is_in_personal_trainings_records': is_in_personal_trainings_records,
                                                                                                'class_not_done': class_not_done,
                                                                                                'more_than_maximum_quantity': more_than_maximum_quantity})
    return classes_data, dates
##############################################
