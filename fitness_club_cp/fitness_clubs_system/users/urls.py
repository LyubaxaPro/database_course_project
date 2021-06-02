from django.urls import path
from .views import UserLoginView, InstructorSignUpView, CustomerSignUpView
from django.contrib.auth import views

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/instructor', InstructorSignUpView.as_view(), name='signup_instructor'),
    path('signup/customer', CustomerSignUpView.as_view(), name='signup_customer'),
]