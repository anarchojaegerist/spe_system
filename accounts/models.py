from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True


    def create_inactive_user(self, email, **extra_fields):
        """Create and save an 'inactive' User with an unusable password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=False, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def register_active_user(self, password, **extra_fields):
        """Register an 'active' User with an unusable password."""

        user = self.model(is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model that uses email for authentication instead
    of username."""

    class Meta:
        """Metadata options for the custom User model."""
        db_table = 'user'

    username = None
    first_name = None
    title = models.CharField(max_length=4, blank=False)
    given_names = models.CharField(max_length=60, blank=False)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Student(models.Model):
    
    class Meta:
        """Metadata options for the Student model."""
        db_table = 'student'


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=8, blank=False)
    spe1 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    spe2 = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    
    REQUIRED_FIELDS = []


class Coordinator(models.Model):
    
    class Meta:
        """Metadata options for the Coordinator model."""
        db_table = 'coordinator'

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    REQUIRED_FIELDS = []