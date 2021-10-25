from django.urls import path
from .common_views import *
from .customer_views import *
from .instructor_views import *
urlpatterns = [
    # common urls
    path('info/index/', IndexView.as_view()),
    path('info/address/', AddressView.as_view()),
    path('info/services/', ServicesView.as_view()),
    path('info/groupclasses_schedule/', ClubGroupClassesView.as_view()),
    path('info/groupclasses_schedule/<int:club_id>/', ClubGroupClassesScheduleForClubView.as_view()),
    path('info/instructors/', ClubInstructorsView.as_view()),
    path('info/instructors/<int:pk>/', ClubInstructorsDetailView.as_view()),
    path('info/instructors/<int:club_id>/', ClubInstructorsForClubView.as_view()),
    path('info/prices/', PricesView.as_view()),
    # customer urls
    path('customer/profile/', CustomerProfileView.as_view()),
    path('customer/profile/edit/<str:name>/<str:surname>/<str:patronymic>/<str:day_of_birth>/<int:height>/',
         CustomerEditProfilePutView.as_view()),
    path('customer/profile/edit/add_measure/<int:weight>/<str:date>/', CustomerEditProfileAddMeasureView.as_view()),
    path('customer/profile/edit/delete_measure/', CustomerEditProfileDeleteMeasureView.as_view()),
    path('customer/training_records/', CustomerTrainingRecordsView.as_view()),
    path('customer/training_records/personal_training/delete/<int:record_id>/',
         CustomerDeletePersonalTrainingRecordView.as_view()),
    path('customer/training_records/personal_training/create_record/<str:date_raw>/<int:i_shedule_id>/',
         CustomerAddPersonalTrainingRecordView.as_view()),
    path('customer/training_records/group_classes/create_record/<str:date_raw>/<int:shedule_id>/',
         CustomerAddGroupClassesRecordView.as_view()),
    path('customer/training_records/group_classes/delete/<int:record_id>/',
         CustomerDeleteGroupTrainingRecordView.as_view()),
    path('customer/training_records/instructor/appoint/<int:instructor_id>/',
         CustomerAppointmentToInstructorView.as_view()),
    path('customer/training_records/instructor/delete_appoint/',
         CustomerDeleteAppointmentToInstructorView.as_view()),
    path('customer/training_records/instructor/change_appoint/',
         CustomerChangeAppointmentToInstructorView.as_view()),
    # instructor urls
    path('instructor/', InstructorView.as_view()),
    path('instructor/attached_customers', InstructorAttachedCustomersView.as_view()),
    path('instructor/profile/edit/<str:name>/<str:surname>/<str:patronymic>/<str:education>/<int:experience>/<str:achievements>/<str:specialization>/',
         InstructorEditProfilePostView.as_view()),
    path('instructor/personal_training/add/<str:day>/<str:time>/', InstructorAddPersonalTrainingView.as_view()),
    path('instructor/profile/delete_changes/<int:pk>', InstructorDeleteProfileChangesView.as_view()),
    path('instructor/personal_training/delete/<int:i_shedule_id>', InstructorDeletePersonalTrainingView.as_view()),
    path('instructor/records/<str:week_num>', InstructorTrainingRecordsView.as_view()),
]