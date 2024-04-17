from django.db import models
from Users.models import CustomUser, Transaction
from Products.models import Product
from Courses.models import Course
from django.utils.timezone import now


class Home(models.Model):
    featured_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    featured_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

class Dashboard(models.Model):
    objectif = models.IntegerField(default=0)

    def calculate_profits(self):
        return Transaction.objects.filter(type='profit', status=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def calculate_losses(self):
        return Transaction.objects.filter(type='loss', status=True).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def total_balance(self):
        profits = self.calculate_profits()
        losses = self.calculate_losses()
        return profits - losses
    
class Feedback(models.Model):
    FEEDBACKS = (
        (0, "😤"),
        (1, "🙁"),
        (2, "😐"),
        (3, "🙂"),
        (4, "😀"),
        (5, "😄"),
    )
    
    feedback_choice = models.IntegerField(choices=FEEDBACKS)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Podcast(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='podcast_images/')
    mp3 = models.FileField(upload_to='podcast_mp3s/')

    def __str__(self):
        return self.name