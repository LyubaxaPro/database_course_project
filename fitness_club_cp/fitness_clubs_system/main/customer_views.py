from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers

from manager.repositories import GroupClassesRepository, \
    InstructorsRepository, SpecialOffersRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, CustomUserRepository, FitnessClubsRepository

from .forms import *
