from django.db import models

# Create your models here.

class SubImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    sub_img = models.ImageField(upload_to='Sub_Product_Images')

class Product(models.Model):
    CATEGORIES = (
        ('none', 'None'),
        ('tshirt', 'T-Shirt'),
        ('cap', 'Cap'),
        ('cup', 'Cup')
    )
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='regular')
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    img = models.ImageField(upload_to="Product_Image")
    price = models.IntegerField(default=0)
    isAvailable = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)