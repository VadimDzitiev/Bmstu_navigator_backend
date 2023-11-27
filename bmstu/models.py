from django.db import models,migrations
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Service(models.Model):
    class Meta:
        managed = True
        db_table = 'service'
    objects = models.Manager()
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200, verbose_name="Маршрут")
    status = models.BooleanField(default=True, verbose_name="Статус")
    buildings = models.BinaryField(blank=True, null=True, verbose_name="Фото строений")
    transition = models.BinaryField(blank=True, null=True, verbose_name="Фото маршрута")
    transition_time = models.CharField(max_length=100, verbose_name="Время перехода")
    description = models.CharField(max_length=200, verbose_name="Описание")

class UserProfile(models.Model):
    class Meta:
        managed = True
        db_table = 'users'
    objects = models.Manager()
    id = models.AutoField(primary_key=True, verbose_name="ID")
    username = models.CharField(max_length=100, verbose_name="Имя")
    userpassword = models.CharField(max_length=100, verbose_name="Пароль")
    is_moderator = models.BooleanField(default=False, verbose_name="Модератор ли")

class Request(models.Model):
    class Meta:
        managed = True
        db_table = 'requests'
    objects = models.Manager()
    statuses = (
        (1, 'Черновик'),
        (2, 'Удален'),
        (3, 'Сформирован'),
        (4, 'Завершен'),
        (5, 'Отклонен'),
    )
    id = models.AutoField(primary_key=True, verbose_name="ID")
    status = models.CharField(choices=statuses, max_length=100, verbose_name="Статус")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    completion_date = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name="Дата выполнения")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, verbose_name="Курс")

class RequestService(models.Model):
    class Meta:
        managed = True
        db_table = 'requestservice'
    objects = models.Manager()
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name="Заявка")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")