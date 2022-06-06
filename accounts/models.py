from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# create token when user is created
from mywebsite import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import BookProduct
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError(_('Phone must be set'))
        if len(phone) != 10:
            raise ValidationError(_('Phone must be 10 digits'))
        phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_active',True)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff set to True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser set to True'))
        return self._create_user(phone, password, **extra_fields)



class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=10, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone


# create token automatically when new user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    avatar = models.ImageField(upload_to='profiles', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile of {self.user.phone}'

# create profile automatically when new user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)
