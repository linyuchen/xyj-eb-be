import typing
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, mobile: str):
        return self.model.objects.get_or_create(mobile=mobile)[0]

    def create_superuser(self, mobile: str, password: str):
        user = self.create_user(mobile)
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    mobile = models.CharField(max_length=11, unique=True)
    nick = models.CharField(max_length=32, null=True, blank=True)
    wxopenid = models.CharField(max_length=64, unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'mobile'
    objects = UserManager()

    def get_full_name(self) -> str:
        return self.nick or self.mobile

    def get_short_name(self) -> str:
        return self.get_full_name()

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True

