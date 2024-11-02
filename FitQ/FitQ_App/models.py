from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Custom User Manager
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

# Wellness Table
class WellnessTable(models.Model):
    DAY_CHOICES = [
        (1, "Day 1"),
        (2, "Day 2"),
        (3, "Day 3"),
        (4, "Day 4"),
        (5, "Day 5"),
        (6, "Day 6"),
        (7, "Day 7"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    sleep_duration_hours = models.DecimalField(max_digits=4, decimal_places=1)
    workout_duration = models.CharField(max_length=50, choices=[
        ("15 minutes", "15 minutes"),
        ("45 minutes", "45 minutes"),
        ("More than 45 minutes", "More than 45 minutes"),
        ("No workout", "No workout")
    ])
    problems_during_day = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    water_intake_liters = models.DecimalField(max_digits=4, decimal_places=1)
    screen_time = models.DecimalField(max_digits=4, decimal_places=1)
    food_on_time = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    type_of_food = models.CharField(max_length=10, choices=[("Healthy", "Healthy"), ("Junk", "Junk")])
    smoking_habit = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    alcohol_consumption = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Wellness Entry for Day {self.day} on {self.date}"

# Feedback Model
class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# User Details Model
class UserDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=50)
    employment_status = models.CharField(max_length=50)
    height = models.FloatField()
    weight = models.FloatField()
    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"User Details for {self.user.email}"

