import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medclinic.settings')
django.setup()

from clinic.models import Doctor, Patient, Service, Appointment, TestResult, News, Review
from django.contrib.auth.models import User
from datetime import datetime

# Создание услуг
service1 = Service.objects.create(name="Консультация терапевта", description="Первичная консультация с терапевтом", price=500.00)
service2 = Service.objects.create(name="Анализ крови", description="Общий анализ крови", price=300.00)
service3 = Service.objects.create(name="МРТ", description="Магнитно-резонансная томография", price=2000.00)

# Создание врачей
doctor1 = Doctor.objects.create(first_name="Иван", last_name="Иванов", specialization="Терапевт", phone="123-456-789", schedule="Пн-Пт 9:00-18:00")
doctor1.services.set([service1, service2])
doctor2 = Doctor.objects.create(first_name="Петр", last_name="Петров", specialization="Радиолог", phone="987-654-321", schedule="Пн-Ср 10:00-15:00")
doctor2.services.set([service3])

# Создание пользователя и пациента
user1 = User.objects.create_user(username="user1", password="password", first_name="Анна", last_name="Антонова")
patient1 = Patient.objects.create(user=user1, date_of_birth="1990-01-01", phone="123-123-123")

# Создание записи на прием
appointment1 = Appointment.objects.create(patient=patient1, doctor=doctor1, service=service1, date=datetime.now(), reason="Регулярная проверка")

# Создание результатов анализов
test_result1 = TestResult.objects.create(patient=patient1, test_name="Анализ крови", result="Все в норме", date="2024-01-01")

# Создание новостей
news1 = News.objects.create(title="Новое оборудование", content="Мы получили новое оборудование для анализа крови.")
news2 = News.objects.create(title="Акция на МРТ", content="Скидка 20% на МРТ в этом месяце.")

# Создание отзывов
review1 = Review.objects.create(author="Сергей Сергеев", content="Очень доволен обслуживанием!", date=datetime.now())
review2 = Review.objects.create(author="Мария Мариева", content="Отличные врачи и внимательный персонал.", date=datetime.now())

print("База данных успешно заполнена.")