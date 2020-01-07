from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

status = (('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'))
leave_types = ((0,'Study'),(1,'Medical'),(2,'Emergency'),(3,'Vacation'),(4,'Other'))

class Department(models.Model):
	department = models.CharField(max_length=100)

	def __str__(self):
		return self.department

class EmployeeProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	department = models.ForeignKey('Department', on_delete=models.CASCADE)
	dob = models.DateField('Date of Birth')
	address = models.CharField(max_length=75)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	origin_state = models.CharField(max_length=50)
	nationality = models.CharField(max_length=50)
	mobile = models.CharField(max_length=15)

	def __str__(self):
		#return self.user.username
		return '%s %s' % (self.user.first_name, self.user.last_name)
	

class LeaveRequest(models.Model):
	employee = models.OneToOneField(EmployeeProfile, on_delete=models.CASCADE)
	start_date = models.DateField(help_text='Start of Leave')
	end_date = models.DateField(help_text='End of Leave')
	leave_type = models.IntegerField(choices=leave_types, default=0)
	reason_for_leave = models.TextField(max_length=250)
	#time_submitted = models.DateTimeField()
	#time_approved = models.DateTimeField()

	def __str__(self):
		return '%s %s %s' % (self.employee.user.first_name, self.employee.user.last_name,
		self.employee.department)

class ManageRequest(models.Model):
	manage_request = models.OneToOneField(LeaveRequest,on_delete=models.CASCADE)#,null=True)
	status_decision = models.CharField(max_length=20,choices=status)#, default=0)
	#listed=models.BooleanField(default=True)

	def __str__(self):
		return '%s %s' % (self.manage_request.employee.user.first_name, 
		self.manage_request.employee.user.last_name)

