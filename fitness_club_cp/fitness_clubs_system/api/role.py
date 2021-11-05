from manager.services import InstructorsService, CustomUserService, CustomersService, \
    AdministratorsService

from .serializers import *

def get_role(request):
    customer = None
    is_customer = False
    instructor = None
    is_instructor = False
    is_admin = False
    admin = None
    is_guest = True
    user = None

    if request.user.pk:
        user = CustomUserService.read_filtered(request.user, {'email': CustomUserService.read_by_pk(request.user, request.user.pk)})[0]
        if user.role == 0:
            customer = CustomersService.read_filtered(request.user, {'user_id': request.user.pk})[0]
            is_customer = True
            is_guest = False
        elif user.role == 1:
            instructor = InstructorsService.read_filtered(request.user, {'user_id': request.user.pk})[0]
            is_instructor = True
            is_guest = False
        elif user.role == 2 or user.role == 3:
            is_admin = True
            admin = AdministratorsService.read_filtered(request.user, {'user': request.user.pk})[0]
            is_guest = False

    return is_customer, CustomersSerializer(customer).data, is_instructor,\
           InstructorsSerializer(instructor).data, is_admin,\
           AdministratorsSerializer(admin).data, is_guest, \
           CustomUserSerializer(user).data

def get_role_json(request):
    is_customer, customer, is_instructor, instructor, is_admin, admin, is_guest, user = get_role(request)
    return {'is_customer': is_customer, 'customer': customer, 'is_instructor': is_instructor, 'instructor': instructor,
            'is_admin': is_admin, 'admin': admin, 'is_guest': is_guest, 'user': user}
