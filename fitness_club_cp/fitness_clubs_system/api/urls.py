from django.conf.urls import url
from django.urls import path
from .common_views import *
from .customer_views import *
from .instructor_views import *
from .admin_views import *
urlpatterns = [
    url(r'^create/$', CreateUserApiView.as_view()),
    url(r'^auth/$', AuthUserView.as_view()),
    # common urls
    path('info/index/', IndexView.as_view()),
    path('info/address/', AddressInfoView.as_view()),
    path('info/services/', ServicesInfoView.as_view()),
    path('info/groupclasses_schedule/', ClubGroupClassesView.as_view()),
    path('info/groupclasses_schedule/<int:club_id>/', ClubGroupClassesScheduleForClubView.as_view()),
    path('info/instructors/', ClubInstructorsView.as_view()),
    path('info/instructors/<int:pk>/', ClubInstructorsDetailView.as_view()),
    path('info/instructors/<int:club_id>/', ClubInstructorsForClubView.as_view()),
    path('info/prices/', PricesView.as_view()),
    # customer urls
    path('customer/profile/', CustomerProfileView.as_view()),
    path('customer/profile/change/', CustomerEditProfileView.as_view()),
    path('customer/profile/change/measure/', CustomerEditProfileMeasureView.as_view()),
    path('customer/training_records/', CustomerTrainingRecordsView.as_view()),
    path('customer/training_records/personal_training/<int:record_id>/',
         CustomerDeletePersonalTrainingRecordView.as_view()),
    path('customer/training_records/personal_training/',
         CustomerCreatePersonalTrainingRecordView.as_view()),
    path('customer/training_records/group_classes/',
         CustomerAddGroupClassesRecordView.as_view()),
    path('customer/training_records/group_classes/<int:record_id>/',
         CustomerDeleteGroupTrainingRecordView.as_view()),
    path('customer/training_records/attachment/',
         CustomerAppointmentToInstructorView.as_view()),
    # instructor urls
    path('instructor/profile/', InstructorView.as_view()),
    path('instructor/attached_customers', InstructorAttachedCustomersView.as_view()),
    path('instructor/profile/change/', InstructorEditProfileView.as_view()),
    path('instructor/personal_training/', InstructorAddPersonalTrainingView.as_view()),
    path('instructor/profile/change/<int:pk>', InstructorDeleteProfileChangesView.as_view()),
    path('instructor/personal_training/<int:i_shedule_id>', InstructorDeletePersonalTrainingView.as_view()),
    path('instructor/records/<str:week_num>', InstructorTrainingRecordsView.as_view()),
    # admin urls
    path('administrator/profile/', AdminProfileView.as_view()),
    path('administrator/group_classes/', AdminGroupClassesView.as_view()),
    path('administrator/group_classes/<int:shedule_id>/', AdminDeleteGroupClassesView.as_view()),
    path('administrator/special_offers/', AdminAdminSpecialOfferView.as_view()),
    path('administrator/special_offers/<str:offer_name>/', AdminDeleteSpecialOfferView.as_view()),
    path('administrator/statistics/<str:week_num>/', AdminStatisticsView.as_view()),
    path('administrator/instructors/', AdminActivateInstructorView.as_view()),
    path('administrator/instructors/<int:user_id>/', AdminRejectInstructorView.as_view())
]