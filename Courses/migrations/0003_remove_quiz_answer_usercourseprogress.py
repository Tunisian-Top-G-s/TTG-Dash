# Generated by Django 5.0.2 on 2024-04-24 09:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='answer',
        ),
        migrations.CreateModel(
            name='UserCourseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_levels', models.ManyToManyField(blank=True, related_name='completed_levels', to='Courses.level')),
                ('completed_modules', models.ManyToManyField(blank=True, related_name='completed_modules', to='Courses.module')),
                ('completed_videos', models.ManyToManyField(blank=True, related_name='completed_videos', to='Courses.video')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]