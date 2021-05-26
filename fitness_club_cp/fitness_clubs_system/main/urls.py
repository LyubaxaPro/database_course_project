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
    path('customer_profile/', customer_profile, name='customer_profile'),
    path('instructor_profile/', instructor_profile, name='instructor_profile'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('edit_customer/', edit_customer_profile, name='edit_customer'),
    path('add_measure/', add_measure, name='add_measure'),
    path('delete_measure/', delete_measure, name='delete_measure'),
]
