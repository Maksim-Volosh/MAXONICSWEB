# Generated by Django 4.2 on 2024-03-01 21:36

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_ordercreate_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercreate',
            name='deadline',
            field=models.CharField(choices=[('', 'Выберите желаемый срок'), ('1', '20 Дней'), ('2', '40 Дней'), ('3', '60 Дней')], max_length=20, verbose_name='Желаемый срок'),
        ),
        migrations.AlterField(
            model_name='ordercreate',
            name='files',
            field=models.FileField(blank=True, upload_to='uploads/', validators=[main.models.OrderCreate.validate_file_size], verbose_name='Файлы'),
        ),
        migrations.AlterField(
            model_name='ordercreate',
            name='websitetype',
            field=models.CharField(choices=[('', 'Выберите тип сайта'), ('1', 'Интернет-магазин'), ('2', 'Персональный сайт'), ('3', 'Сайт-визитка'), ('4', 'Форум'), ('5', 'Блог'), ('6', 'Лендинг'), ('7', 'Другой')], max_length=20, verbose_name='Тип сайта'),
        ),
    ]