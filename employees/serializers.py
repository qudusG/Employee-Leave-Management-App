from .models import Department, LeaveRequest, EmployeeProfile, ManageRequest
from rest_framework import serializers
from django.contrib.auth.models import User

class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Department
		fields = ['department']

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email']

class EmployeeProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = EmployeeProfile
		fields = ['user','department','dob','address','city','state','origin_state','nationality','mobile']

class LeaveRequestSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = LeaveRequest
		fields = ['employee','leave_type','reason_for_leave','start_date', 'end_date']

class ManageRequestSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ManageRequest
		fields = ['manage_request','status_decision']