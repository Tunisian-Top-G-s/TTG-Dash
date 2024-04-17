from django.contrib import admin
from .models import Color, Product, SubImage, Size, Deal

# Register your models here.
admin.site.register([Product, SubImage, Color, Size, Deal])