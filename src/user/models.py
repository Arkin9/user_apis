import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

def user_profile_image_file_path(instance, filename):
    """Generate file path for user profile image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'profile_images', filename)


class UserManager(BaseUserManager):
    """Manager for User."""

    def create_user(self, email, contact_number, password=None, **extra_field):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an Email address.')
        if not contact_number:
            raise ValueError('User must have an Contact Number field.')

        email = self.normalize_email(email)
        user = self.model(email=email, contact_number=contact_number, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, contact_number, password):
        """Create and return a new superuser."""
        user = self.create_user(email, contact_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the System."""
    # email, contact_number, profile_image, birthdate and password
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    profile_image = models.FileField(null=True, upload_to=user_profile_image_file_path)
    birthdate = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact_number']
