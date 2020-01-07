from django.urls import path

from . import views
app_name = 'employees'
urlpatterns = [
	path('', views.index, name = 'index'),
	path('register', views.register, name = 'register'),
	#path('login', views.login_view, name = 'login'),
	path('logout', views.logout_view, name= 'logout'),
	path('profile', views.profile, name = 'profile'),
	path('apply', views.apply, name = 'apply'),
	path('manage_requests', views.manage_requests, name = 'manage_requests'),
	path('update_application', views.update_application, name = 'update_application'),
	path('<int:leaverequest_id>/decision', views.decision, name = 'decision'),
]