from django.contrib import admin
from .models import CustomUser, Transaction, Badge, Professor

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Transaction)
admin.site.register(Badge)
admin.site.register(Professor)