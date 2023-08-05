from email.policy import default
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000, null=True, blank=True)
    priority = models.IntegerField(default=5, null=True, blank=True)
    status = models.CharField(
        max_length=100, default="New", null=True, blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        "Appuser", on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


"""
This file contains the Data Models for Appuser Tables
"""


user_status_choices = [('Active', 'Active'), ('Inactive', 'Inactive')]


class Appuser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    # org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    first_login = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    recovery_email_address = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=255, choices=user_status_choices, default='Active')
    phone = models.CharField(blank=True, null=True, max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=1255, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.username)


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    used_count = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(max_length=1255, blank=True)
    modified_by = models.CharField(max_length=255, blank=True)


class TagTaskMapping(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
