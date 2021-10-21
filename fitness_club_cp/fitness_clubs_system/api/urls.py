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
    path('customer/profile/edit/<str:name>/<str:surname>/<str:patronymic>/<str:day_of_birth>/<int:height>/', CustomerEditProfilePutView.as_view()),
    path('customer/profile/edit/add_measure/<int:weight>/<str:date>/', CustomerEditProfileAddMeasureView.as_view()),
    path('customer/profile/edit/delete_measure/', CustomerEditProfileDeleteMeasureView.as_view()),
    # instructor urls
    path('instructor/', InstructorView.as_view()),
]