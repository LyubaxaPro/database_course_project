from django.urls import path
from .views import UserLoginView, UserSignUpView
from django.contrib.auth import views

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]