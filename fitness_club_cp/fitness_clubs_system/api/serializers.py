from rest_framework import serializers
from manager.models import Administrators, Customers, GroupClasses, GroupClassesCustomersRecords, Instructors,\
GroupClassesShedule, AdminRecords, InstructorShedule, InstructorSheduleCustomers, Prices, Services, SpecialOffers,\
InstructorPersonalTrainingsLogs, AdminGroupClassesLogs

from users.models import FitnessClubs, CustomUser

class AdministratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrators
        fields = '__all__'

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class GroupClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupClasses
        fields = '__all__'

class GroupClassesCustomersRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupClassesCustomersRecords
        fields = '__all__'

class InstructorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructors
        fields = '__all__'

class GroupClassesSheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupClassesShedule
        fields = '__all__'

class AdminRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRecords
        fields = '__all__'

class InstructorSheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorShedule
        fields = '__all__'

class AInstructorSheduleCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorSheduleCustomers
        fields = '__all__'

class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class SpecialOffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffers
        fields = '__all__'

class InstructorPersonalTrainingsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorPersonalTrainingsLogs
        fields = '__all__'

class AdminGroupClassesLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminGroupClassesLogs
        fields = '__all__'

class FitnessClubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClubs
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
