from django.db import models

# Create your models here.

class UserQuery(models.Model):
    user_message = models.TextField()
    doctor_response = models.TextField()
    product_response = models.TextField()
    class Meta:
        app_label = 'bot'