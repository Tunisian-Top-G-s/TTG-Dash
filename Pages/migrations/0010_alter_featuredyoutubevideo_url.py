# Generated by Django 5.0.2 on 2024-05-06 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pages', '0009_featuredyoutubevideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredyoutubevideo',
            name='url',
            field=models.CharField(max_length=10000),
        ),
    ]
