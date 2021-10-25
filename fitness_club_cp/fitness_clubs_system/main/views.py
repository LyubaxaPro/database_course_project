from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers

from manager.repositories import GroupClassesRepository, \
    InstructorsRepository, SpecialOffersRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, CustomUserRepository, FitnessClubsRepository


# from fitness_clubs_system.api.utils import get_plot
# from fitness_clubs_system.api.view_funcs.simple_data import *
# from fitness_clubs_system.api.view_funcs.customer import *
# from fitness_clubs_system.main.view_funcs.instructor import *
# from fitness_clubs_system.api.view_funcs.admin import *
from .forms import *
from api.form_classes_data import form_classes_data
from api.instructor_schedule import form_instructors_shedule
from api.role import get_role_json

