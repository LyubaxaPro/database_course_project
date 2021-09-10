from django.contrib import admin

from .models import Instructors, Customers, InstructorSheduleCustomers, Prices, GroupClassesShedule, InstructorShedule,\
    GroupClassesCustomersRecords, Administrators, AdminRecords

admin.site.register(Instructors)
admin.site.register(Customers)
admin.site.register(InstructorSheduleCustomers)
admin.site.register(Prices)
admin.site.register(GroupClassesShedule)
admin.site.register(InstructorShedule)
admin.site.register(GroupClassesCustomersRecords)
admin.site.register(Administrators)
admin.site.register(AdminRecords)