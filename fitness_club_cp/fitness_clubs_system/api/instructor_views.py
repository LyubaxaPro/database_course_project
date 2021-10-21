from django.http import JsonResponse
from rest_framework import status

from manager.repositories import ServicesRepository, FitnessClubsRepository, GroupClassesRepository,\
    GroupClassesSheduleRepository, InstructorsRepository, SpecialOffersRepository, PricesRepository, \
    GroupClassesCustomersRecordsRepository, InstructorSheduleCustomersRepository, \
    AdminRecordsRepository, InstructorPersonalTrainingsLogsRepository, CustomUserRepository

from manager.models import AdminRecords

#from ..utils import get_plot
from .simple_data import *
from .customer import *
from .instructor import *
from .admin_funcs import *

from django.shortcuts import render

from rest_framework.response import Response

from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse

class InstructorView(APIView):
    """
    get:
        get information for instructor profile
    """

    def get(self, request):
        role = get_role_json(request)
        if not role['is_instructor']:
            return JsonResponse({'status':'false','message':'lopellandra'}, status=500)
            # return Response(status=404, data="jopel")

        fitness_club = FitnessClubsRepository.read_filtered(request.user, {'club_id': role['user']['club']})
        address = fitness_club[0].city + ", " + fitness_club[0].address
        instructor_shedule = form_instructors_shedule(request.user, role['instructor']['instructor_id'])

        exp_str = "лет"
        if role['instructor']['experience'] % 10 == 1 and role['instructor']['experience'] != 11:
            exp_str = "год"
        elif role['instructor']['experience'] % 10 in [2, 3, 4] and role['instructor']['experience'] not in [12, 13,
                                                                                                             14]:
            exp_str = "года"

        record = AdminRecordsRepository.read_filtered(request.user, {'instructor': role['instructor']['instructor_id'],
                                                                     'status': AdminRecords.PENDING})
        change_record = None
        is_already_record = False
        if record:
            is_already_record = True
            change_record = record[0]

        data = {'role': get_role_json(request), 'address': address, 'shedule': instructor_shedule,
                'exp_str': exp_str,
                'is_already_record': is_already_record,
                'change_record': change_record}
        return Response(data)