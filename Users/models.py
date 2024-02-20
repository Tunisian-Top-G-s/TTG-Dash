from django.contrib.auth.models import User
from django.db import models
from Ranks.models import Rank
from django.db.models.signals import post_save
from django.dispatch import receiver
from Courses.models import Course, CourseProgression
from django.utils import timezone

class Badge(models.Model):
    title = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="Badge_img")

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    STATUS = (
        ('regular', 'Regular'),
        ('subscriber', 'Subscriber'),
        ('moderator', 'Moderator')
    )
    
    status = models.CharField(max_length=20, choices=STATUS, default='regular')
    tel = models.CharField(max_length=16, null=True)
    address = models.CharField(max_length=255, blank=True)
    pfp = models.ImageField(upload_to='user_images', default='default_user_image.png')
    rank = models.ManyToManyField(Rank)
    badges = models.ManyToManyField(Badge)
    bio = models.TextField(max_length=150)
    enrolled_courses = models.ManyToManyField(Course, related_name='enrolled_users', blank=True)
    last_added_points_time = models.DateTimeField(blank=True, null=True)

    # Make email, first name, and last name required
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=True)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.user)

    def calculate_profits(self):
        return self.transactions.filter(type='profit', status=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def calculate_losses(self):
        return self.transactions.filter(type='loss', status=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def calculate_balance(self):
        profits = self.calculate_profits()
        losses = self.calculate_losses()
        return profits - losses

    def calculate_overall_progress(self):
        # Get all courses enrolled by the user
        enrolled_courses = self.enrolled_courses.all()

        overall_progress = 0
        total_courses = enrolled_courses.count()

        # Calculate the progress for each enrolled course
        for course in enrolled_courses:
            course_progression, created = CourseProgression.objects.get_or_create(user=self, course=course)
            course_progress = course_progression.calculate_progression()
            overall_progress += course_progress

        # Calculate the overall progress
        if total_courses > 0:
            overall_progress_percentage = (overall_progress / (total_courses * 100)) * 100
        else:
            overall_progress_percentage = 0

        return overall_progress_percentage


    def save(self, *args, **kwargs):
        # If the email field is not provided and a User instance exists, set the email field to the user's email
        if not self.email and self.user:
            self.email = self.user.email
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_custom_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'customuser'):
        CustomUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_custom_user(sender, instance, **kwargs):
    try:
        instance.customuser.save()
    except CustomUser.DoesNotExist:
        pass

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, related_name='transactions', null=True, on_delete=models.CASCADE) 
    TYPE = (
        ('profit', 'Profit'),
        ('loss', 'Loss'),
    )
    
    type = models.CharField(max_length=20, choices=TYPE, blank=False,  null=True)
    pair = models.CharField(max_length=20, blank=False,  null=True)
    amount = models.FloatField()
    img = models.ImageField(upload_to='user_transactions', blank=False, null=True)
    status = models.BooleanField(default=False, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)  # Automatically set the date when created

    def __str__(self):
        return str(self.user)