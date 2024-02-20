from django.db import models
from Users.models import CustomUser, Transaction

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