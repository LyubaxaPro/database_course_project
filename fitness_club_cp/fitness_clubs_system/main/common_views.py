from django.shortcuts import render
from django.http import JsonResponse

from .forms import *
from api.common_views import IndexView, AddressView, ServicesView, ClubGroupClassesView, ClubInstructorsView, \
    ClubInstructorsDetailView, ClubGroupClassesScheduleForClubView, ClubInstructorsForClubView, PricesView

def index(request):
    indexView = IndexView()
    data = indexView.get(request)
    return render(request, 'main/index.html', data.data)

def address(request):
    view = AddressView()
    data = view.get(request)
    return render(request, 'main/address.html', data.data)

def services(request):
    view = ServicesView()
    data = view.get(request)
    return render(request, 'main/services.html', data.data)

def get_club_schedule(request):
    club_id = request.GET.get("club_id")
    view = ClubGroupClassesScheduleForClubView()
    data = view.get(request, **{'club_id': club_id})
    return JsonResponse({'classes_data': data.data}, safe=False)

def groupclasses(request):
    view = ClubGroupClassesView()
    data = view.get(request).data
    return render(request, "main/group_classes.html", {'form' : ClubForm(), 'classes_data' : data['classes_data'],
                                             'classes':data['classes'], 'role': data['role']})

def get_club_instructors(request):
    club_id = request.GET.get("club_id")
    view = ClubInstructorsForClubView()
    data = view.get(request, **{'club_id': club_id}).data
    return JsonResponse(data, safe=False)

def instructors_list(request):
    view = ClubInstructorsView()
    data = view.get(request).data
    return render(request, 'main/instructors.html', {'instructors': InstructorsRepository.read_filtered(request.user, {'is_active': True}), 'form' : ClubForm(),
                                                     'role': data['role']})

def instructor_detail(request, pk):
    view = ClubInstructorsDetailView()
    data = view.get(request, **{'pk': pk}).data
    return render(request, 'main/instructor_detail.html', data)


def prices(request):
    view = PricesView()
    data = view.get(request).data
    return render(request, "main/prices.html", data)

