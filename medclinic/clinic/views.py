from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Appointment, Service, TestResult, News, Review
from .forms import AppointmentForm, CustomUserCreationForm, PatientForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.timezone import now, localtime

def index(request):
    reviews = Review.objects.all().order_by('-date')
    services = Service.objects.all()
    news = News.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('index')
        else:
            return redirect('login')
    else:
        form = ReviewForm()
    return render(request, 'clinic/index.html', {'reviews': reviews, 'form': form, 'services': services, 'news': news })

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic/doctor_list.html', {'doctors': doctors})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'clinic/service_list.html', {'services': services})

def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'clinic/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True,
                                 'redirect_url': '/'})  # Укажите URL для перенаправления после успешного создания записи
        else:
            errors = {field: list(errors) for field, errors in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = AppointmentForm(user=request.user)
    return render(request, 'clinic/appointment_form.html', {'form': form, 'services': Service.objects.all()})

@login_required
def patient_dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')
    test_results = patient.testresult_set.all().order_by('-date')

    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=patient)
        if patient_form.is_valid():
            patient_form.save()
            return redirect('patient_dashboard')
    else:
        patient_form = PatientForm(instance=patient)

    return render(request, 'clinic/patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'test_results': test_results,
        'patient_form': patient_form,
        'today': localtime(now())
    })
@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient__user=request.user)
    if appointment.date <= now():
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm(instance=appointment, user=request.user)
    return render(request, 'clinic/appointment_form.html', {'form': form})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient__user=request.user)
    if appointment.date <= now():
        return redirect('patient_dashboard')

    if request.method == 'POST':
        appointment.delete()
        return redirect('patient_dashboard')
    return render(request, 'clinic/appointment_confirm_delete.html', {'appointment': appointment})

def contact(request):
    return render(request, 'clinic/contact.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            date_of_birth = form.cleaned_data.get('date_of_birth')
            phone = form.cleaned_data.get('phone')
            Patient.objects.create(user=user, date_of_birth=date_of_birth, phone=phone)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.http import JsonResponse



def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    return render(request, 'clinic/doctor_profile.html', {'doctor': doctor})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=request.user.patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваши данные успешно обновлены.')
            return redirect('patient_dashboard')
    else:
        form = PatientForm(instance=request.user.patient)
    return render(request, 'clinic/edit_profile.html', {'form': form})

def load_doctors(request):
    service_id = request.GET.get('service_id')
    doctors = Doctor.objects.filter(services__id=service_id)
    return JsonResponse({'doctors': list(doctors.values('id', 'first_name', 'last_name', 'specialization'))})

@login_required
def load_doctor_schedule(request):
    doctor_id = request.GET.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    schedule = doctor.schedule if doctor.schedule else ''
    return JsonResponse({'schedule': schedule})