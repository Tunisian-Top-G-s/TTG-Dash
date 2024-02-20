from django.db import models
from Users.models import CustomUser
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
    