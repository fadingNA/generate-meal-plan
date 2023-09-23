from .models import *

class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModel):
    username_validator = UnicodeUsernameValidator()

    # Username Field
    username = models.CharField('Username', max_length=24, unique=True, validators=[username_validator])
    is_active = models.BooleanField('Active', default=True)

    #Email Field
    email = models.EmailField('Email', unique=True, blank=True)
    is_staff = models.BooleanField('Staff status', default=False, help_text='Designates whether the user can log into this admin site.')


    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # used only on createsuperuser

    @property
    def is_django_user(self):
        return self.has_usable_password()