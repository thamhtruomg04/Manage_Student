# teachers/models.py
from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.teacher_name