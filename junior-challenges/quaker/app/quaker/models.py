from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core import validators

class Quak(models.Model):
    message = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    seen_by_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)
    profile_pic = models.TextField(default='/static/img/profile1.png')
    description = models.TextField(default='')
    following = models.ManyToManyField(User, related_name='following')
    quaks = models.ManyToManyField(Quak, related_name='quaks')
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()   

class Message(models.Model):
    user_from = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='user_to', on_delete=models.CASCADE)
    message = models.TextField(default='')
    seen = models.BooleanField(default=False)
    token = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
