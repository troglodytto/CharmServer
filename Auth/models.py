from typing import List
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from Auth.manager import UserManager

# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=128)
    profile_image = models.CharField(_("profile image"), max_length=128)
    is_active = models.BooleanField(_("is active"), default=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["username"]

    objects: BaseUserManager = UserManager()

    def __str__(self) -> str:
        return f"${self.username} [{self.email}]"

    @staticmethod
    def find_or_create(serializer):
        email = serializer.validated_data["email"]

        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return serializer.save()
