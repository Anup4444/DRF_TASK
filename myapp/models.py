from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone number must be set'))
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(
        _('phone number'), max_length=15, unique=True)
    name = models.CharField(_('name'), max_length=150)
    photo = models.ImageField(upload_to='photos/', default='img.jpg')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
