from django.contrib.auth import login, views as auth_views
from django.contrib import messages
from django.shortcuts import redirect, render, resolve_url
from django.views.generic import View
from django.contrib.auth import authenticate, login

from .forms import CustomUserSignUpForm
from .models import CustomUser

class UserLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    # Determine the URL to redirect to when the form is successfully validated. Returns success_url by default.
    def get_success_url(self):

        logged_user = self.request.user
        logged_user_role = logged_user.role

        if logged_user_role == CustomUser.CUSTOMER:
            print("if logged_user_role == MyUser.CUSTOMER:")
            return resolve_url('home')

        elif logged_user_role == CustomUser.INSTRUCTOR:
            print("logged_user_role == MyUser.INSTRUCTOR:")
            return resolve_url('home')

        elif logged_user_role == CustomUser.ADMIN:
            print("logged_user_role == MyUser.ADMIN:")
            return resolve_url('home')

        else:
            return resolve_url('home')


class UserSignUpView(View):
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):

        if 'user_form' not in kwargs:
            kwargs['user_form'] = CustomUserSignUpForm()

        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):

        user_form = CustomUserSignUpForm(request.POST)

        if user_form.is_valid():
            print("FFFFFF")
            user_form.save()
            return redirect('login')

        return render(request, self.template_name,
                      {'role': 'guest', 'user_form': user_form})