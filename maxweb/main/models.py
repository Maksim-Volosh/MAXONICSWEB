from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    pass


class OrderCreate(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название заказа")
    description = models.TextField(verbose_name="Описание", validators=[MinLengthValidator(100)])
    targetgroup = models.CharField(max_length=50, verbose_name="Целевая аудитория")
    TYPE_CHOICES = [
        ('', 'Выберите тип сайта'),
        ('1', 'Интернет-магазин'),
        ('2', 'Персональный сайт'),
        ('3', 'Сайты-визитка'),
        ('4', 'Форум'),
        ('5', 'Блог'),
        ('6', 'Лендинг'),
        ('7', 'Другой'),
    ]
    websitetype = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип сайта")
    budget = models.CharField(max_length=20, verbose_name="Желаемый бюджет")
    DEADLINE_CHOICES = [
        ('', 'Выберите желаемый срок'),
        ('1', '3 Недели'),
        ('2', '1 Месяц'),
        ('3', '1 Месяц 2 Недели'),
        ('4', '2 Месяца'),
    ]
    deadline = models.CharField(max_length=20, choices=DEADLINE_CHOICES, verbose_name="Желаемый срок")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
        ('consideration', 'На рассмотрении'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='consideration', verbose_name="Статус")
    files = models.FileField(upload_to='uploads/', verbose_name="Файлы", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



