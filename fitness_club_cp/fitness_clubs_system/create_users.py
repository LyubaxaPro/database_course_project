
import csv
import  os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_clubs_system.settings')
django.setup()
from users.models import CustomUserManager, CustomUser


def read_from_file(filename):
    results = []
    with open(filename) as File:
        reader = csv.DictReader(File)
        for row in reader:
            results.append(row)
    return results


def run():
    users = read_from_file('/home/lyubaxapro/database_course_project/database_data/users.csv')
    for i in users:
        user = CustomUser.objects.create_user(email=i['email'], password=i['password'],role=i['role'], login=i['login'], phone=i['phone'], club=i['club_id'])

if __name__ == '__main__':
    run()