from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
import uuid
from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'Username',
        max_length=255,
        unique=True, validators=[username_validator])
    is_active = models.BooleanField('Active', default=True)

    # allow non-unique emails
    email = models.EmailField('Email address', blank=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # used only on createsuperuser

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    @property
    def is_django_user(self):
        return self.has_usable_password()

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.uuid}>'

    objects = UserManager()
