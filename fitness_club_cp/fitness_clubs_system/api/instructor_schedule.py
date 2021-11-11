from manager.services import ServicesService, FitnessClubsService, GroupClassesService,\
    GroupClassesSheduleService, InstructorsService, CustomUserService, SpecialOffersService, PricesService,\
    CustomersService, InstructorSheduleService, GroupClassesCustomersRecordsService, InstructorSheduleCustomersService,\
    AdministratorsService, AdminRecordsService, InstructorPersonalTrainingsLogsService, AdminGroupClassesLogsService

from .week import *

def form_instructors_shedule_for_tarif(user, instructor_id, tarif, week, customer_id):
    shedule = InstructorSheduleService.read_filtered(user, {'instructor_id': instructor_id})
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

            training_by_customer = InstructorSheduleCustomersService.read_filtered(user, {'customer_id': customer_id,
                                                                                             'i_shedule_id': current_shed.i_shedule_id,
                                                                                             'training_date': days_dates[current_shed.day_of_week]})
            if len(training_by_customer) != 0:
                is_training_by_customer = True
            else:
                training_by_other = InstructorSheduleCustomersService.read_filtered(user, {'i_shedule_id': current_shed.i_shedule_id,
                                                                                             'training_date':days_dates[current_shed.day_of_week]})
                if len(training_by_other) != 0:
                    is_training_by_other = True

            groupclasses = GroupClassesCustomersRecordsService.read_filtered(user,
                                                                                {'customer_id': customer_id,
                                                                                 'class_date': days_dates[current_shed.day_of_week]})
            if len(groupclasses) != 0:
                for gr_class in groupclasses:
                    groupclass_time = GroupClassesSheduleService.read_filtered(user, {'shedule_id': gr_class.shedule_id})
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
    shedule = InstructorSheduleService.read_filtered(user, {'instructor_id': instructor_id})
    group_classes = GroupClassesSheduleService.read_join_filtered(user, 'class_field', {'instructor_id': instructor_id})
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
    shedule = InstructorSheduleService.read_filtered(user, {'instructor_id': instructor_id})
    group_classes = GroupClassesSheduleService.read_join_filtered(user, 'class_field', {'instructor_id': instructor_id})
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
        customer_raw = InstructorSheduleCustomersService.read_filtered(user, {'i_shedule_id': current_shed.i_shedule_id,
                                                                             'training_date': days_dates[current_shed.day_of_week]})

        if len(customer_raw) != 0:
            customer = CustomersService.read_filtered(user, {'customer_id': customer_raw[0].customer_id})[0]
        training_data[str(current_shed.training_time)[:-3]][current_shed.day_of_week].update({'name':'Персональная тренировка',
                                                                                              'is_personal': True,
                                                                                              'customer': customer})
    for current_shed in group_classes:

        count = len(GroupClassesCustomersRecordsService.read_filtered(user, {'shedule_id': current_shed.shedule_id,
                                                                             'class_date': days_dates[current_shed.day_of_week]}))

        training_data[str(current_shed.class_time)[:-3]][current_shed.day_of_week].update({'name':current_shed.class_field.class_name,
                                                                                          'is_personal': False,
                                                                                           'count': count})
    day_of_week_date = {}
    for i in range(len(days)):
        day_of_week_date.update({days[days_en[i]]: dates_raw[i]})

    return training_data, day_of_week_date

