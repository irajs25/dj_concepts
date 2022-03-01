from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 

from django.db.models.signals import post_save

# Create your models here.

# Creating CustomUserManager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
        user = self.model(
            username=self.normalize_email(email),
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user



# Creating Custom User
class User(AbstractUser):
    username = models.CharField(
        null=True,
        blank=True,
        max_length=512
    )
    fullname = models.CharField(
        null=True,
        blank=True,
        max_length=512,
        help_text="Your fullname like first and last name, 512 characters."
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site."
    )

    is_active = models.BooleanField(
        default=True,
        help_text= (
            "Designates whether this user should be treated as active. "
            "Deselect this instead of deleting accounts."
        ),
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD  = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("id", )

    def get_full_name(self):
        return self.fullname


    def __str__(self):
        return "{}{}".format(self.get_full_name(), self.email)

# Creating UserProfile
class UserProfile(models.Model):

    user = models.OneToOneField(
        User, related_name="profile", unique=True, on_delete=models.CASCADE
    )
    profile_pic = models.FileField(
        upload_to="media", blank=True, null=True, default=None
    )
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(null=True, blank=True, default=None)
    country = models.CharField(max_length=255, null=True, blank=True, default=None)
    state = models.CharField(max_length=255, null=True, blank=True, default=None)
    city = models.CharField(max_length=255, null=True, blank=True, default=None)
    zip_code = models.IntegerField(null=True, blank=True, default=None)
    facebook = models.URLField(null=True, blank=True, default=None)
    instagram = models.URLField(null=True, blank=True, default=None)
    twitter = models.URLField(null=True, blank=True, default=None)
    linkedin = models.URLField(null=True, blank=True, default=None)
    about = models.TextField()

    def create_user_profile(sender, signal, instance, **kwargs):
        if kwargs['created']:
            UserProfile.objects.create(user=instance)

post_save.connect(UserProfile.create_user_profile, sender=User)