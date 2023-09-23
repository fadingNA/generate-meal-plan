import uuid
from typing import Any
from django.db import models


# Create your models here.
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager, Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


class AbstractBaseModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.__class__.__name__} {self.uuid}'

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.uuid}>'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user(password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = ((
        'user', 'User'
    ), ('admin', 'Admin'))

    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLES, default='user')

    objects = CustomUserManager()

    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name="customuser_groups",  # custom related name
        related_query_name="customuser",
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    
    # Override user_permissions to avoid clash
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name="customuser_user_permissions",  # custom related name
        related_query_name="customuser",
        help_text=('Specific permissions for this user.'),
    )

    def __str__(self):
        return str(self.id)
    
    

