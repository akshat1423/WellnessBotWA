from django.db import models
from django.utils import timezone


# Create your models here.

class UserQuery(models.Model):
    user_message = models.TextField()
    doctor_response = models.TextField()
    product_response = models.TextField()
    phone_no_from= models.TextField()
    gist = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 
    message_count = models.IntegerField(default=1)
    class Meta:
        app_label = 'bot'

class UserGist(models.Model):
    phone_no_from= models.TextField()
    gist = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 
    class Meta:
        app_label = 'bot'

# class AcmeWebhookMessage(models.Model):
#     received_at = models.DateTimeField(help_text="When we received the event.")
#     payload = models.JSONField(default=None, null=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=["received_at"]),
#         ]