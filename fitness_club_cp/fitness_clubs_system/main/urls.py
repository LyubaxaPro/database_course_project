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
    path('customer_training_records/', customer_training_records, name='customer_training_records'),
    path('delete_personal_training_record/', delete_personal_training_record, name='delete_personal_training_record'),
    path('delete_group_class_record/', delete_group_class_record, name='delete_group_class_record'),
    path('add_group_class_record/', add_group_class_record, name='add_group_class_record'),
    path('add_personal_training_record/', add_personal_training_record, name='add_personal_training_record'),
    path('appointment_to_instructor/', appointment_to_instructor, name='appointment_to_instructor'),
    path('delete_appointment_to_instructor/', delete_appointment_to_instructor, name='delete_appointment_to_instructor'),
    path('replace_appointment_to_instructor/', replace_appointment_to_instructor, name='replace_appointment_to_instructor'),
    path('edit_instructor/', edit_instructor, name='edit_instructor'),
    path('instructor_add_personal_training/', instructor_add_personal_training, name='instructor_add_personal_training'),
    path('instructor_delete_personal_training/', instructor_delete_personal_training, name='instructor_delete_personal_training'),
    path('instructor_attached_customers/', instructor_attached_customers, name='instructor_attached_customers'),
    path('instructor_training_records/', instructor_training_records, name='instructor_training_records'),
    path('group_classes_admin/', group_classes_admin, name='group_classes_admin')
]
