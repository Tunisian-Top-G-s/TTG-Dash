# Generated by Django 5.0.2 on 2024-04-25 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0004_rename_deals_deal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='Product',
            new_name='product',
        ),
    ]