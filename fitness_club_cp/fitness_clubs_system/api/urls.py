from django.urls import path
from .common_views import *
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
    # instructor urls
    path('instructor/', InstructorView.as_view()),
]