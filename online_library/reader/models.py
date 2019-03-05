from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Reader(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=30, null=True)
    icon = models.ImageField(upload_to='icon', null=False, blank=True)

    def _unicode_(self):
        return self.account.username
