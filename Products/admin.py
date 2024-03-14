from django.contrib import admin
from .models import Color, Product, SubImage, Size

# Register your models here.
admin.site.register([Product, SubImage, Color, Size])