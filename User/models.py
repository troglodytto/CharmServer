from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

from User.manager import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=128)
    profile_image = models.CharField(_("profile image"), max_length=128)
    is_active = models.BooleanField(_("is active"), default=True)
    is_staff = models.BooleanField(_("is staff"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = ["username"]

    objects: UserManager = UserManager()

    def __str__(self) -> str:
        is_active = "✅" if self.is_active else "❌"
        return f"{self.username} [{self.email} {is_active}]"

    @staticmethod
    def find_or_create(serializer):
        email = serializer.validated_data["email"]

        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            return serializer.save()
