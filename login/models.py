from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.
class MenuItem(models.Model):
    """ menubar items """
    perm = models.ForeignKey(Permission)
    dispname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    target = models.CharField(max_length=64)
    alt = models.CharField(max_length=255)
