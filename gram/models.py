from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length =30)
    bio = models.TextField()
    dp = models.ImageField( blank=True)
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender,instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.save()  

    def delete_profile(self):
        self.delete()  

    @classmethod
    def update_profile(cls,update):
        pass

    classmethod
    def search_by_profile(cls,name):
        profile = Profile.objects.filter(user__username__icontains=name)
        return profile 

    @classmethod 
    def get_by_id(cls,id):
        profile = Profile.objects.get(user = id)
        return profile
