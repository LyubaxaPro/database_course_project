import datetime

days = {"Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда", "Thursday": "Четверг", "Friday": "Пятница",
        "Saturday": "Суббота", "Sunday": "Воскресенье"}

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
