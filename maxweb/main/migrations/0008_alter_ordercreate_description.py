# Generated by Django 4.2 on 2024-02-17 20:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_ordercreate_websitetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercreate',
            name='description',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(100)], verbose_name='Описание'),
        ),
    ]
