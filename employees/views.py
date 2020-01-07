from django.shortcuts import get_object_or_404, render, redirect
from .models import EmployeeProfile, LeaveRequest, ManageRequest
from django.contrib.auth.decorators import login_required
from .forms import EmployeeProfileForm, ExtendedUserCreationForm, LeaveRequestForm, ManageRequestForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets
from .serializers import *

class DepartmentViewSet(viewsets.ModelViewSet):
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class EmployeeProfileViewSet(viewsets.ModelViewSet):
	queryset = EmployeeProfile.objects.all()
	serializer_class = EmployeeProfileSerializer

class LeaveRequestViewSet(viewsets.ModelViewSet):
	queryset = LeaveRequest.objects.all()
	serializer_class = LeaveRequestSerializer

class ManageRequestViewSet(viewsets.ModelViewSet):
	queryset = ManageRequest.objects.all()
	serializer_class = ManageRequestSerializer

custom_user = None
custom2_user = None

def index(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = AuthenticationForm(request=request, data=request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				if user is not None:
					login(request, user)
					messages.info(request, f"You are now logged in as {username}")
					return HttpResponseRedirect(reverse('employees:index'))
				else:
					messages.error(request, "invalid username or password")
			else:
					messages.error(request, "invalid username or password")
		form = AuthenticationForm()
		return render(request, 'employees/index.html',{'form':form})
	else:
		return render(request, 'employees/index.html')

@login_required
def apply(request):
	#instanc = EmployeeProfile.objects.get(user=request.user)
	#instance = LeaveRequest(employee=instanc)
	#form = LeaveRequestForm(instance=instance)
	#form = LeaveRequestForm(initial={'employee':request.user})
	if request.method == 'POST':
		form = LeaveRequestForm(request.POST,hide_condition=True)
		#form = LeaveRequestForm(initial={'employee':employee.user})
		if form.is_valid():
			#form = LeaveRequestForm(initial={'employee':employee.user.username})
			#form.instance.employee = request.user
			form.save()
			return HttpResponseRedirect(reverse('employees:profile'))
	else:
		default = EmployeeProfile.objects.get(user=request.user)

		form = LeaveRequestForm(initial={'employee':default},hide_condition=True)
		#form = LeaveRequestForm(hide_condition=True)
	context = {'form':form}
    #self form.employee = request.User
	return render(request, 'employees/apply.html',context)

def register(request):
	#model = Employee
	#form_class = UserCreationForm
	#success_url = reverse_lazy('index')
	#template_name = 'employees/registration.html'
	if request.method == 'POST':
		form = ExtendedUserCreationForm(request.POST)
		profile_form = EmployeeProfileForm(request.POST)

		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			profile1 = profile_form.save(commit=False)
			profile1.user = user
			profile1.save()
		
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username = username, password = password)
			login(request, user)
			return HttpResponseRedirect(reverse('employees:index'))
	else:
		form = ExtendedUserCreationForm()
		profile_form = EmployeeProfileForm()
	context = {'form':form,'profile_form':profile_form}
	return render(request, 'employees/registration.html',context)

@login_required
def profile(request):
	employee_detail = EmployeeProfile.objects.get(user=request.user.id)
	#employee_detail = get_object_or_404(EmployeeProfile=request.user.id)
	context = {'employee_detail':employee_detail}
	global custom_user
	custom_user = request.user.id
	return render(request, 'employees/profile.html',context)

@staff_member_required
def manage_requests(request):
	#choic = ManageRequest.objects.filter(listed=True)
	#context['status_decision'] = choic.get_status_decision_display()
	leave_applications = LeaveRequest.objects.all()
	context = {'leave_applications':leave_applications}
	return render(request, 'employees/manage_requests.html', context)

@staff_member_required
def decision(request, leaverequest_id):
	leave_detail = get_object_or_404(LeaveRequest, pk = leaverequest_id)
	global custom2_user
	custom2_user = leaverequest_id
	#employee_detail = EmployeeProfile.objects.get(pk=employeeprofile_id)
	#leave_request = LeaveRequest.objects.get(employee=employee_detail)
	#manager_decision = ManageRequest.objects.get(manage_request=leave_detail)

	if request.method == 'POST':
		form = ManageRequestForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('employees:update_application')
			#return HttpResponseRedirect(reverse('employees:update_application',kwargs={'id':leave_detail.id}))
	else:
		#form = ManageRequestForm()
		default = LeaveRequest.objects.get(id=leaverequest_id)
		form = ManageRequestForm(initial={'manage_request':default},hide_condition=True)
	context = {'form':form,'leave_detail':leave_detail}
	
	return render(request,'employees/application.html',context=context)


@staff_member_required
def update_application(request):
	#employee_detail = EmployeeProfile.objects.get(user=custom2_user)
	leave_request = LeaveRequest.objects.get(id=custom2_user)
	manager_decision = ManageRequest.objects.get(manage_request=leave_request)
	context = {'leave_request':leave_request,'manager_decision':manager_decision}

	if manager_decision.status_decision == 'Approved':
		delete_items = LeaveRequest.objects.filter(id=custom2_user)
		delete_items.delete()

	elif ManageRequest.status_decision == 'Rejected':
		delete_items = LeaveRequest.objects.filter(pk=leaverequest_id)
		delete_items.delete()
	
	return render(request,'employees/approved.html',context=context)
	#return HttpResponseRedirect(reverse('employees:index'))

@login_required
def logout_view(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect('employees:index')


