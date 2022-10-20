from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, username, **extra_fields):
        user = self.create_user(
            email=email,
            username=username,
            is_superuser=True,
            is_staff=True,
            **extra_fields
        )

        user.set_password(password)
        user.save()

    def create_user(self, email, username, **kwargs):
        if not email:
            raise ValueError(_("The email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_unusable_password()
        user.save()

        return user
