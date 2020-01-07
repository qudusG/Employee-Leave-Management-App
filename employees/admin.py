from django.contrib import admin
from .models import EmployeeProfile, LeaveRequest, Department, ManageRequest

admin.site.register(Department)
admin.site.register(EmployeeProfile)
admin.site.register(LeaveRequest)
admin.site.register(ManageRequest)