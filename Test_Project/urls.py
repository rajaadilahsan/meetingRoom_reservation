"""Test_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from test_app import views
from knox import views as knox_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/employees/', views.employeeList.as_view(), name='employees'),
    path('api/rooms/', views.roomList.as_view()),
    path('api/reservations/', views.reservationList.as_view()), 
    path('api/delete_reservation/<int>meeting_id>', views.reservationDetail.as_view()), 
    path('api/getRoomReservation/', views.getReservationByEmployee.as_view()),
    path('api/invitee_cancel_reservation/', views.reservationInviteeDetail.as_view()),
    path('api/invitees/', views.reservationInviteesList.as_view()),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]
