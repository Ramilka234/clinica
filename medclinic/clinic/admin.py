from django.contrib import admin

from .models import Doctor, Patient, Service, Appointment, TestResult, News, Review

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(TestResult)
admin.site.register(News)
admin.site.register(Review)
