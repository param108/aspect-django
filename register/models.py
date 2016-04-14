from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EmailVerify(models.Model):
  secret = models.CharField(max_length=50) 
  user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
  is_verified = models.BooleanField(default=False)
