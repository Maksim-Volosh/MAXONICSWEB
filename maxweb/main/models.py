from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

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
        ('3', 'Сайт-визитка'),
        ('4', 'Форум'),
        ('5', 'Блог'),
        ('6', 'Лендинг'),
        ('7', 'Другой'),
    ]
    websitetype = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип сайта")
    budget = models.CharField(max_length=20, verbose_name="Желаемый бюджет")
    DEADLINE_CHOICES = [
        ('', 'Выберите желаемый срок'),
        ('1', '30 Дней'),
        ('2', '45 Дней'),
        ('3', '60 Дней'),
        ('4', '75 Дней'),
    ]
    SOCCHOICE_CHOICES = [
        ('', 'Выберите тип связи'),
        ('1', 'Telegram'),
        ('2', 'Facebook'),
        ('3', 'WhatsApp'),
        ('4', 'Номер телефона'),
        ('5', 'Свой вариант'),
    ]
    socialnetworkchose = models.CharField(max_length=20, choices=SOCCHOICE_CHOICES, verbose_name="Тип связи")
    socialnetwork = models.CharField(max_length=50, verbose_name="Контакт для связи")
    deadline = models.CharField(max_length=20, choices=DEADLINE_CHOICES, verbose_name="Желаемый срок")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
        ('consideration', 'На рассмотрении'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='consideration', verbose_name="Статус")
    def validate_file_size(value):
        filesize = value.size

        if filesize > 52428800:
            raise ValidationError("Максимальный размер файла - 50 МБ.")

    files = models.FileField(upload_to='uploads/', verbose_name="Файлы", blank=True, validators=[validate_file_size])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



