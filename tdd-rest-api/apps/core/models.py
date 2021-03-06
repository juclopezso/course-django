from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.base import ModelBase
from django.forms.fields import EmailField

# to run migrations inside core, run: python manage.py makemigrations core
# then run: python manage.py migrate

class UserManager(BaseUserManager):

  def create_user(self, email, password=None, **extra_fields):
    """Create a user with email, password and maybe extra fields"""
    if not email:
      raise ValueError("Users must have a valid email")

    user = self.model(email=email.lower(), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user
  
  def create_superuser(self, email, password):
    """Create a super user"""
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user


class User(AbstractBaseUser, PermissionsMixin):
  """Allow login with email instead of username"""
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'

class Tag(models.Model):
  """Tag model for recipe"""
  name = models.CharField(max_length=255)
  user = models.ForeignKey(User, models.CASCADE)

  def __str__(self):
    return self.name