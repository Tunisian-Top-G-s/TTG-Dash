from django.contrib import admin
from .models import Product, SubImage

# Register your models here.
admin.site.register([Product, SubImage])