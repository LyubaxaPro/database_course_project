from django.contrib import admin

from .models import Instructors, Customers, InstructorSheduleCustomers, Prices

admin.site.register(Instructors)
admin.site.register(Customers)
admin.site.register(InstructorSheduleCustomers)
admin.site.register(Prices)