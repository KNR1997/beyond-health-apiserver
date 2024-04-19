from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, validate_email
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)

phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 10 digits only."
)

class UserAccountManager(BaseUserManager):
    # def create_user(self, email, password=None, **kwargs):
    #     if not email:
    #         raise ValueError('Users must have an email address')

    #     email = self.normalize_email(email)
    #     email = email.lower()

    #     user = self.model(
    #         email=email,
    #         **kwargs
    #     )

    #     user.set_password(password)
    #     user.save(using=self._db)

    #     return user

    # def create_superuser(self, email, password=None, **kwargs):
    #     user = self.create_user(
    #         email,
    #         password=password,
    #         **kwargs
    #     )

    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)

    #     return user
    
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone_number")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number=phone_number, password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True, max_length=255)
    # phone_number = models.CharField(
    #     unique=True, max_length=10, null=False, blank=False, validators=[phone_regex]
    # )
    # otp = models.CharField(max_length=6)
    # otp_expiry = models.DateTimeField(blank=True, null=True)
    # max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    # otp_max_out = models.DateTimeField(blank=True, null=True)
    
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # user_registered_at = models.DateTimeField(auto_now_add=True)
    
    # objects = UserAccountManager()

    # USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    # def __str__(self):
    #     return self.email
    
    
    phone_number = models.CharField(
        unique=True, max_length=10, null=False, blank=False, validators=[phone_regex]
    )
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_email],
    )
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"

    objects = UserAccountManager()

    def __str__(self):
        return self.phone_number