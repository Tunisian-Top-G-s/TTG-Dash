# Generated by Django 5.0.2 on 2024-05-02 02:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0005_quiz_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_modules', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_quiz', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='video',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_videos', to='Courses.course'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='Courses.course'),
        ),
        migrations.AlterField(
            model_name='level',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_levels', to='Courses.course'),
        ),
    ]