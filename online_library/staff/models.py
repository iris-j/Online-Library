from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    class Meta:
        permissions = (
            ("can_add", "Can add book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        )

    def _unicode_(self):
        return self.account.username
