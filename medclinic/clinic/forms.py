from django import forms
from django.utils import timezone
from .models import Appointment, Patient, Doctor, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'doctor', 'reason', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.none()

        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['doctor'].queryset = Doctor.objects.filter(services__id=service_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['doctor'].queryset = self.instance.service.doctors

    def clean_date(self):
        date = self.cleaned_data['date']
        doctor = self.cleaned_data.get('doctor')
        service = self.cleaned_data.get('service')

        if Appointment.objects.filter(patient__user=self.user, date__date=date.date(), service=service).exists():
            raise ValidationError("Вы уже записаны на эту услугу в этот день.")

        if date.date() <= timezone.now().date():
            raise forms.ValidationError("Вы можете записаться только на следующий день или позже.")

        if Appointment.objects.filter(doctor=doctor, date=date).exists():
            raise forms.ValidationError("В это время уже существует запись. Пожалуйста, выберите другое время.")

        if not self.is_within_working_hours(date, doctor.schedule):
            raise forms.ValidationError("Выбранное время не входит в рабочие часы врача. Пожалуйста, выберите другое время.")

        if self.is_has_conflicting_appointments(date, doctor):
            raise forms.ValidationError("Пожалуйста выберите время на 15 минут позднее предыдущей записи")

        return date

    def is_within_working_hours(self, date, schedule):
        day_map = {
            'Пн': 0, 'Вт': 1, 'Ср': 2,
            'Чт': 3, 'Пт': 4, 'Сб': 5, 'Вс': 6
        }

        day_of_week = date.weekday()
        schedule_parts = schedule.split(";")

        print(f"Проверка для даты: {date}, день недели: {day_of_week}")

        for part in schedule_parts:
            days_hours = part.strip().split(" ")
            days = days_hours[0].split("-")
            hours = days_hours[1].split("-")

            start_time = hours[0].strip()
            end_time = hours[1].strip()
            start_hour, start_minute = map(int, start_time.split(":"))
            end_hour, end_minute = map(int, end_time.split(":"))

            start_datetime = date.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
            end_datetime = date.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)

            print(f"Проверка части расписания: {part}, start_datetime: {start_datetime}, end_datetime: {end_datetime}")

            if len(days) == 1:  # Один день, например "Пн"
                if day_map[days[0]] == day_of_week:
                    print(f"Проверка одного дня: {day_map[days[0]]}, {day_of_week}")
                    if start_datetime <= date <= end_datetime:
                        return True
            elif len(days) == 2:  # Диапазон дней, например "Пн-Пт"
                start_day = day_map[days[0]]
                end_day = day_map[days[1]]
                print(f"Проверка диапазона дней: {start_day} - {end_day}, {day_of_week}")
                if start_day <= day_of_week <= end_day:
                    if start_datetime <= date <= end_datetime:
                        return True

        return False

    def is_has_conflicting_appointments(self, date, doctor):
        appointment_times = Appointment.objects.filter(doctor=doctor).values_list('date', flat=True)
        for appointment_time in appointment_times:
            appointment_time = timezone.localtime(appointment_time)
            date = timezone.localtime(date)
            print(f"Comparing {date} with {appointment_time}")  # Отладочная информация
            if abs((date - appointment_time).total_seconds()) < 900:  # 15 минут
                return True
        return False

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.patient = Patient.objects.get(user=self.user)
        if commit:
            appointment.save()
        return appointment

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(label="Телефон", max_length=15)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 'password1', 'password2')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].label = 'Дата рождения'
        self.fields['phone'].label = 'Телефон'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }