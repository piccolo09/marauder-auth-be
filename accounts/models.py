import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('Username'),
        max_length=255,
        validators=[username_validator], blank=True, null=True)

    first_name = models.CharField(
        _('First Name'),
        max_length=255,
        blank=True,
        null=True)

    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
        blank=True,
        null=True)

    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),)

    # allow non-unique emails
    email = models.EmailField('Email address', blank=True, unique=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']  # used only on createsuperuser

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    activated = models.DateTimeField(_("Account Activated"), blank=True, null=True)
    email_confirmed = models.DateTimeField(_("Email Confirmed"), blank=True, null=True)
    setup_completed = models.DateTimeField(_("Setup Complete"), blank=True, null=True)

    @property
    def is_django_user(self):
        return self.has_usable_password()

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.uuid}>'

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    address = models.CharField(_("Permanant Address"), max_length=255, blank=True, null=True)
    department = models.CharField(_("Work Department"), max_length=255, blank=True, null=True)

    # is_activated = models.BooleanField(_("Account Activated"),)
    # email_confirmed = models.BooleanField(_("Account Activated"),)
