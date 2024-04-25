# Generated by Django 5.0.2 on 2024-04-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pages', '0005_home_featured_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='podcast_images/')),
                ('mp3', models.FileField(upload_to='podcast_mp3s/')),
            ],
        ),
    ]