# Generated by Django 5.0 on 2024-02-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_ordercreate_files'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordercreate',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='ordercreate',
            name='deadline',
            field=models.CharField(choices=[('', 'Выберите желаемый срок'), ('1', '3 Недели'), ('2', '1 Месяц'), ('3', '1 Месяц 2 Недели'), ('4', '2 Месяца')], max_length=20, verbose_name='Желаемый срок'),
        ),
    ]
