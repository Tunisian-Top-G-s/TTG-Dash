from django.db import models
from Users.models import CustomUser
from Users.models import Professor
# Create your models here.



class PrivateSessionRequest(models.Model):
    DURATION_CHOICES = (
        (30, '30 Minutes'),
        (60, '1 Hour'),
        (90, '1H 30 Minutes'),
        (120, '2 Hours'),
    )

    PROFESSOR_CHOICES = (
        (0, 'az'),
        (1, '1 zz'),
        (2, '1H 30zz Minutes'),
    )

    TYPES = (
        ('0', 'a session by yourself alone'),
        ('1', 'a session just between you and your friends'),
        ('2', 'a session including you and another group'),
    )

    session_mode = models.CharField(max_length=20, choices=TYPES, default=0)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    duration_hours = models.PositiveIntegerField(choices=DURATION_CHOICES, blank=True, null=True)

    selected_professor = models.CharField(choices=PROFESSOR_CHOICES, blank=True, null=True, max_length=150)
    session_date = models.DateTimeField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Private Session Request #{self.id}"

    @property
    def prof_choices(self):
        return [(prof.id, prof.name) for prof in Professor.objects.all()]


        
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
    