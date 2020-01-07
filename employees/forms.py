from django import forms
from .models import EmployeeProfile, Department, LeaveRequest, ManageRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

years = [x for x in range(1940, 2021)]

class ExtendedUserCreationForm(UserCreationForm):
	email = forms.EmailField(max_length=100)
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)

	def __init__(self, *args, **kwargs):
		super(ExtendedUserCreationForm, self).__init__(*args,**kwargs)

		for fieldname in ['username', 'email', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

	class Meta:
		model = User
		fields = ('username','email','first_name','last_name','password1','password2')

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']

		if commit:
			user.save()
		return user

class EmployeeProfileForm(forms.ModelForm):
	'''def __init__(self, *args, **kwargs):
		super(EmployeeProfileForm, self).__init__(*args,**kwargs)

		for fieldname in ['username', 'email', 'password1', 'password2']:
			self.fields[fieldname].help_text = None'''

	class Meta:
		model = EmployeeProfile
		fields = ('mobile','department','dob','address','city','state','origin_state','nationality')

class LeaveRequestForm(forms.ModelForm):
	class Meta:
		model = LeaveRequest
		#employee=forms.IntegerField(widget=forms.HiddenInput(),initial=EmployeeProfile.user)
		#widgets = {'start_date': forms.DateTimeInput(attrs={'class': 'datetime-input'})}
		fields = ('employee','leave_type','reason_for_leave','start_date', 'end_date')
		
	def __init__(self, *args, **kwargs):
		from django.forms.widgets import HiddenInput
		hide_condition = kwargs.pop('hide_condition',None)
		super(LeaveRequestForm, self).__init__(*args, **kwargs)
		if hide_condition:
			self.fields['employee'].widget = HiddenInput()

class ManageRequestForm(forms.ModelForm):
	class Meta:
		model = ManageRequest
		fields = ('manage_request','status_decision')
	
	def __init__(self, *args, **kwargs):
		from django.forms.widgets import HiddenInput
		hide_condition = kwargs.pop('hide_condition',None)
		super(ManageRequestForm, self).__init__(*args, **kwargs)
		if hide_condition:
			self.fields['manage_request'].widget = HiddenInput()
