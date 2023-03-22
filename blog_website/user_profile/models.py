from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import customUserManager

# Create your models here.
class user(AbstractUser):
    email =  models.EmailField(
        max_length=150,
        unique=True,
        error_messages={
        "unique": "The email must be unique"
        }
    )
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_image"
    )

    REQUIRED_FIELDS = ["email"]
    objects = customUserManager()

    def __str__(self) -> str:
        return self.username
    
    def get_profile_picture(self):
        url=""
        try:
           url = self.profile_image.url
        except:
           url=""
        return url   