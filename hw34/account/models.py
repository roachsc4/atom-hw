from django.db import models
from django.contrib.auth.models import AbstractUser #,User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone





class User(AbstractUser):
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=15)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	age = models.PositiveIntegerField(null=True, blank=True)
	region = models.CharField(max_length=30)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS=[]
