from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=250, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['id']

class UserFollower(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.DO_NOTHING,)
    follows =  models.ForeignKey(User, related_name="follows", on_delete=models.DO_NOTHING,)

    class Meta:
        managed = True
        unique_together = ("user", "follows",)