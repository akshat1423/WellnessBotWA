from django.db import models
from django.utils import timezone

from django.utils import timezone


# Create your models here.

class UserQuery(models.Model):
    message_internal_id = models.AutoField(primary_key=True)
    user_message = models.TextField()
    doctor_response = models.TextField()
    product_response = models.TextField()
    response_message_segregation=models.TextField()
    profile_name = models.CharField(max_length=255, null=True, blank=True)
    phone_no_from = models.CharField(max_length=20, null=True, blank=True)
    gist = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    message_count = models.IntegerField(default=1)
    class Meta:
        app_label = 'bot'
    currentstate = models.IntegerField(default=0)

class UserGist(models.Model):
    phone_no_from= models.TextField()
    gist = models.TextField()
    currentstate = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        app_label = 'bot'

