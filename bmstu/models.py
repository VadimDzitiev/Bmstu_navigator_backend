from django.db import models,migrations
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Service(models.Model):
    class Meta:
        managed = True
        db_table = 'service'
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    buildings = models.BinaryField(blank=True, null=True)
    transition = models.BinaryField(blank=True, null=True)
    transition_time = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'service'
    def __str__(self): 
        return self.title 

class UserProfile(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    userpassword = models.CharField(max_length=100, blank=True, null=True)
    is_moderator = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'userprofile'
    def __str__(self): 
        return self.title 

class Request(models.Model):   
    statuses = (
        (1, 'Черновик'),
        (2, 'Удален'),
        (3, 'Сформирован'),
        (4, 'Завершен'),
        (5, 'Отклонен'),
    )

    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    status = models.CharField(choices=statuses, default=1, max_length=100)
    creation_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    formation_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    completion_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    moderator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='request_moderator_set', blank=True, null=True) 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='request_user_set', blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'requests'
    def __str__(self): 
        return self.title 


class RequestService(models.Model):
    objects = models.Manager()
    request = models.ForeignKey(Request, on_delete=models.CASCADE,blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    time = models.IntegerField( blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'requestservice'
    def __str__(self): 
        return self.title 