from django.db import models
from Users.models import CustomUser, Transaction
from Products.models import Product
from Courses.models import Course

from django.utils import timezone
from datetime import datetime, timedelta


class Home(models.Model):
    featured_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    featured_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

class Dashboard(models.Model):
    objectif = models.IntegerField(default=0)

    def get_changes_today(self):
        """
        Calculate the profits made today.
        """
        # Assuming today's date
        today = timezone.now().date()

        # Calculate the start and end of today
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        # Filter transactions for profits and losses with a date within today
        profits_today = Transaction.objects.filter(type='profit', date__range=(start_of_day, end_of_day))
        losses_today = Transaction.objects.filter(type='loss', date__range=(start_of_day, end_of_day))
    
        # Calculate the total profits and losses of today
        total_profits_today = profits_today.aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_losses_today = losses_today.aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        total_change = total_profits_today - total_losses_today

        return total_change

    def calculate_total_balance(self):
        """
        Calculate the total balance (sum of all profits and losses).
        """
        # Filter all profits and losses
        profits = Transaction.objects.filter(type='profit')
        losses = Transaction.objects.filter(type='loss')
        
        # Calculate the total profits and losses
        total_profits = profits.aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_losses = losses.aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        total_balance = total_profits - total_losses
        
        if total_balance.is_integer():
            total_balance = int(total_balance)

        return total_balance

    def calculate_change_percentage(self):
        """
        Calculate the change percentage compared to the previous day's balance.
        """
        # Get today's date and yesterday's date
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # Get the balances for today and yesterday
        today_balance = self.calculate_total_balance()
        
        # Query for yesterday's balance
        yesterday_balance = Transaction.objects.filter(date__date=yesterday).aggregate(
            total_balance=models.Sum(models.Case(
                models.When(type='profit', then=models.F('amount')),
                models.When(type='loss', then=models.F('amount') * -1),
                default=models.Value(0),
                output_field=models.FloatField()
            ))
        )['total_balance'] or 0

        # Calculate the percentage change
        if yesterday_balance != 0:
            change_percentage = ((today_balance - yesterday_balance) / yesterday_balance) * 100
        else:
            change_percentage = 0
        
        change_percentage = round(change_percentage, 2)

        return change_percentage


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
    description = models.CharField(max_length=150, blank=True, null=True)
    banner = models.ImageField(upload_to='podcast_banner/', blank=True, null=True)
    mp3 = models.FileField(upload_to='podcast_mp3s/')

    def __str__(self):
        return self.name
    
class featuredYoutubeVideo(models.Model):
    video_id = models.CharField(max_length=100, blank=True, null=True)

class Quest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="quests/", blank=True, null=True)
    def points(self):
        return sum(step.points for step in self.steps.all())

class Step(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=100)
    description = models.TextField()
    index = models.IntegerField(blank=True, null=True)
    points = models.IntegerField()

class UserQuestProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    current_step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True)
    points_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.user.username} - {self.quest.title}"

    def update_progress(self):
        # Get the next step based on the current step's index
        if self.current_step:
            next_step = Step.objects.filter(quest=self.quest, index=self.current_step.index + 1).first()
        else:
            next_step = self.quest.steps.first()

        # Update the current step
        if next_step:
            self.current_step = next_step
            self.save()

    def complete_step(self):
        if self.current_step:
            self.points_earned += self.current_step.points
            self.update_progress()

    def finished_steps_count(self):
        if self.current_step:
            print("there is current step")
            # Count the number of steps with an index less than or equal to the index of the current step
            return self.quest.steps.filter(index__lte=self.current_step.index).count()
        else:
            # If there's no current step, no steps are finished
            print("there is no current step")
            return 0
