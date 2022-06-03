from django.db import models
import datetime as dt
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length =30)
    bio = models.TextField()
    dp = models.ImageField( blank=True)
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE, primary_key=True)
