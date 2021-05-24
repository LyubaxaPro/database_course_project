from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('address/', address, name='address'),
    path('services/', services, name='services'),
    path('groupclasses/', groupclasses, name='groupclasses'),
    path('instructors/', instructors_list, name='instructors'),
    path('instructors/<int:pk>/', instructor_detail, name='instructor_detail'),
    path('get_club_schedule/', get_club_schedule, name='get_club_schedule'),
    path('get_club_instructors/', get_club_instructors, name='get_club_instructors'),
    path('prices/', prices, name='prices'),
    path('cutomer_profile/', cutomer_profile, name='cutomer_profile'),
    path('instructor_profile/', instructor_profile, name='instructor_profile'),
    path('admin_profile/', admin_profile, name='admin_profile')
]
