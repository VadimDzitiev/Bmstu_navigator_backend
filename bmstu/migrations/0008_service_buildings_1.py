# Generated by Django 4.2.7 on 2023-11-22 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu', '0007_alter_service_buildings'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='buildings_1',
            field=models.BinaryField(blank=True, null=True, verbose_name='Фото строений'),
        ),
    ]