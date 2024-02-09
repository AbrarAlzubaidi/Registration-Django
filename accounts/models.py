from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'