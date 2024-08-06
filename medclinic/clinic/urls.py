from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('services/', views.service_list, name='service_list'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/new/', views.appointment_create, name='appointment_create'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('contact/', views.contact, name='contact'),
    path('ajax/load-doctors/', views.load_doctors, name='ajax_load_doctors'),
    path('doctors/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('ajax/load-doctor-schedule/', views.load_doctor_schedule, name='ajax_load_doctor_schedule'),
]