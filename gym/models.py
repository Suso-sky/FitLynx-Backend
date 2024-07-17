from django.db import models
from datetime import datetime, timedelta, date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Gym(models.Model):
    gym_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    max_capacity = models.PositiveIntegerField(default=0)

class ScheduleDay(models.Model):
    DAY_CHOICES = [ 
                    ('Monday', 'Monday'),
                    ('Tuesday', 'Tuesday'),
                    ('Wednesday', 'Wednesday'),  
                    ('Thursday', 'Thursday'), 
                    ('Friday', 'Friday'),
                    ('Saturday', 'Saturday'),
                    ('Sunday','Sunday')]

    day = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    closed = models.BooleanField(default=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.day} - {"Closed" if self.closed else f"{self.open_time} to {self.close_time}"}'

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    uid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    program = models.CharField(max_length=255, blank=True, null=True)
    student_code = models.PositiveIntegerField(default=0, unique=False, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.URLField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    student_code_edited = models.BooleanField(default=False)
    program_edited = models.BooleanField(default=False)
    phone_edited = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='gym_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='gym_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.email
    
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    date = models.DateField()
    time = models.TimeField()
    hours_amount = models.PositiveIntegerField(default=1)
    end_time = models.TimeField(blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        # Calculate the end time when saving the reservation
        if self.time and self.hours_amount:
            end_time = (datetime.combine(date(1, 1, 1), self.time) +
                        timedelta(hours=self.hours_amount)).time()
            self.end_time = end_time

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.hours_amount} hour(s) on {self.date} at {self.time}'

class Penalty(models.Model):
    penalty_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username} - {self.start_date} to {self.end_date}'

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    date = models.DateField()
    time = models.TimeField()
    hours_amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} - {self.hours_amount} hour(s) on {self.date} at {self.time}'
    
class Membership(models.Model):
    membership_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.start_date} to {self.end_date}'
