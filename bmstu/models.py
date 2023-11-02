from django.db import models,migrations
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Service(models.Model):
    class Meta:
        managed = True
        db_table = 'service'
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    building = models.BinaryField(blank=True, null=True)
    transition = models.BinaryField(blank=True, null=True)
    transition_time = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_published = models.BooleanField(default=True)

class UserProfile(models.Model):
    class Meta:
        managed = True
        db_table = 'users'
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    userpassword = models.CharField(max_length=100)

class Request(models.Model):
    class Meta:
        managed = True
        db_table = 'requests'
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100)  # Статус заявки (например, "ожидает", "выполняется", "завершена")
    created_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    moderator = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)  # Модератор



class RequestService(models.Model):
    class Meta:
        managed = True
        db_table = 'M-M'
    objects = models.Manager()
    request = models.ForeignKey(Request, on_delete=models.CASCADE)  # Связь с заявкой
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
