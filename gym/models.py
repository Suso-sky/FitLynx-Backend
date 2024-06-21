from django.db import models
from datetime import datetime, timedelta, date

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

class Person(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        abstract = True  # Define this class as abstract

    def __str__(self):
        return self.username


class User(Person):
    uid = models.CharField(max_length=255, unique=True, primary_key=True)
    program = models.CharField(max_length=255)
    student_code = models.PositiveIntegerField(default=0, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # New optional field
    photo_url = models.URLField(max_length=500, null=True, blank=True)

    # Fields to track if they have been edited
    student_code_edited = models.BooleanField(default=False)
    program_edited = models.BooleanField(default=False)
    phone_edited = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class Admin(Person):
    
    def __str__(self):
        return self.username

class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username} - {self.start_date} to {self.end_date}'

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    date = models.DateField()
    time = models.TimeField()
    hours_amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} - {self.hours_amount} hour(s) on {self.date} at {self.time}'
    
class Membership(models.Model):
    membership_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.start_date} to {self.end_date}'
