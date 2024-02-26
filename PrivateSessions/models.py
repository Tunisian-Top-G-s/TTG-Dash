from django.db import models
from Users.models import CustomUser
from Users.models import Professor
# Create your models here.

class PrivateSession(models.Model):
    STATUS = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )
    
    status = models.CharField(max_length=20, choices=STATUS, default='scheduled')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_private_sessions')
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='professor_private_sessions')
    # Assuming that the Courses model is defined in the 'Courses' app
    # cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='private_sessions')
    schedule = models.DateTimeField()
    Duration = models.DurationField()
    


class PrivateSessionRequest(models.Model):
    TYPES = (
        ('0', 'a session by yourself alone'),
        ('1', 'a session just between you and your friends'),
        ('2', 'a session inculding you and another group'),
    )
    prof = models.ForeignKey(Professor, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPES, default='0')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    duration_hours = models.PositiveIntegerField(blank=True, null=True)

    date_requested = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    session_date = models.DateTimeField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    # Add more fields as necessary

    def __str__(self):
        return f"Private Session Request #{self.id} by {self.user.username}"