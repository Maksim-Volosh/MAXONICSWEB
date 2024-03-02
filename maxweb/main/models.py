from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    pass


class OrderCreate(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Order name"))
    description = models.TextField(verbose_name=_("Description"), validators=[MinLengthValidator(100)])
    targetgroup = models.CharField(max_length=50, verbose_name=_("Target audience"))
    TYPE_CHOICES = [
        ('', _('Select website type')),
        ('1', _('Online store')),
        ('2', _('Personal website')),
        ('3', _('Business card website')),
        ('4', _('Forum')),
        ('5', _('Blog')),
        ('6', _('Landing page')),
        ('7', _('Other')),
    ]

    websitetype = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_("Select website type"))
    budget = models.CharField(max_length=20, verbose_name=_("Disired budget"))
    DEADLINE_CHOICES = [
        ('', _('Select desired deadline')),
        ('1', _('30 Days')),
        ('2', _('45 Days')),
        ('3', _('60 Days')),
        ('4', _('75 Days')),
    ]
    
    SOCCHOICE_CHOICES = [
        ('', _('Select communication type')),
        ('1', 'Telegram'),
        ('2', 'WhatsApp'),
        ('3', 'Viber'),
        ('4', _('Phone number')),
    ]

    socialnetworkchose = models.CharField(max_length=20, choices=SOCCHOICE_CHOICES, verbose_name=_("Communication type"))
    socialnetwork = models.CharField(max_length=50, verbose_name=_("Phone number"))
    deadline = models.CharField(max_length=20, choices=DEADLINE_CHOICES, verbose_name=_("Disired deadline"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
        ('consideration', _('Under consideration')),
        ('in_progress', _('In progress')),
        ('completed', _('Completed')),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='consideration', verbose_name=_("Status"))
    def validate_file_size(value):
        filesize = value.size

        if filesize > 52428800:
            raise ValidationError(_("The maximum file size is 50 MB."))

    files = models.FileField(upload_to='uploads/', verbose_name=_("Files"), blank=True, validators=[validate_file_size])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")



