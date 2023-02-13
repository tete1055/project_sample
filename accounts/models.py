from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

def image_directory_path(instance, filename):
    return 'profile_images/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

class CustomUser(AbstractUser):
    email = models.EmailField(
        'email',
        unique=True,)
    image = models.ImageField(
        upload_to='profile_images/',
        default='images/profile1.png',)
    name = models.CharField(
        'name',
        max_length=50,
        blank=False,)
    context = models.TextField(
        verbose_name='自己紹介',
        max_length=160,
        blank=True)
    gender = models.CharField(
        max_length=10,
        blank=True,)
    follow_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    stripe_account = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    stripe_customer = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    created = models.DateTimeField(auto_now_add=True)