# import uuid
#
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.db import models
#
#
# class UserManager(BaseUserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Email is required')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.create_activation_code()
#         user.save(using=self._db)
#         return user
#
#     def create(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)
#         return self._create_user(email, password, **extra_fields)
#
#
# class User(AbstractBaseUser):
#     email = models.EmailField(max_length=100, primary_key=True)
#     name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     activation_code = models.CharField(max_length=8, blank=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = UserManager()
#
#     def create_activation_code(self):
#         activation_code = str(uuid.uuid4())
#         if User.objects.filter(activation_code=activation_code).exists():
#             self.create_activation_code()
#         self.activation_code = activation_code
#         self.save()
#         return activation_code
#
#     def has_perm(self, perm, obj=None):
#         return self.is_superuser
#
#     def has_module_perms(self, app_label):
#         return self.is_superuser
#

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError('Username is required.')
        if not email:
            raise ValueError('Email is required.')
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create_user(username, email, password, **kwargs)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def create_activation_code(self):
        activation_code = str(uuid.uuid4())
        if User.objects.filter(activation_code=activation_code).exists():
            self.create_activation_code()
        self.activation_code = activation_code
        self.save()
        return activation_code

    def str(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


