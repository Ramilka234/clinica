from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    specialization = models.CharField("Специализация", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    schedule = models.TextField("Расписание")  # Информация о расписании
    services = models.ManyToManyField('Service', verbose_name="Услуги", related_name='doctors')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.specialization})"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

class Patient(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    date_of_birth = models.DateField("Дата рождения")
    phone = models.CharField("Телефон", max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

class Service(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, verbose_name="Врач", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, verbose_name="Услуга", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField("Дата и время")
    reason = models.TextField("Причина")

    def __str__(self):
        return f"{self.patient} - {self.doctor} на {self.date}"

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

class TestResult(models.Model):
    patient = models.ForeignKey(Patient, verbose_name="Пациент", on_delete=models.CASCADE, null=True, blank=True)
    test_name = models.CharField("Название анализа", max_length=100)
    result = models.TextField("Результат")
    date = models.DateField("Дата")

    def __str__(self):
        return f"{self.test_name} для {self.patient} на {self.date}"

    class Meta:
        verbose_name = "Результат анализа"
        verbose_name_plural = "Результаты анализов"

class News(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Содержание")
    date = models.DateTimeField("Дата", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.TextField("Отзыв")
    date = models.DateTimeField("Дата", auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.date}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"