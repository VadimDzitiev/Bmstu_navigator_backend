from django.db import models,migrations
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import UserManager, User, PermissionsMixin, AbstractBaseUser


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


class NewUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=500, unique=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    is_moderator = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = NewUserManager()

    class Meta:
        verbose_name_plural = "Users"
        managed = True

    def __str__(self):
        return self.email


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
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Курс")


class RequestService(models.Model):
    class Meta:
        managed = True
        db_table = 'requestservice'
    objects = models.Manager()
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name="Заявка")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")