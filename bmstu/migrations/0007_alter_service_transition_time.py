# Generated by Django 4.2.8 on 2024-01-19 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu', '0006_remove_request_created_date_request_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='transition_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Время перехода'),
        ),
    ]
