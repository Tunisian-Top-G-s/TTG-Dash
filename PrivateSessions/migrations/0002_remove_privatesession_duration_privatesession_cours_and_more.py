# Generated by Django 5.0.2 on 2024-03-26 02:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0002_initial'),
        ('PrivateSessions', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatesession',
            name='Duration',
        ),
        migrations.AddField(
            model_name='privatesession',
            name='cours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='private_sessions', to='Courses.course'),
        ),
        migrations.AddField(
            model_name='privatesession',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='privatesession',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='privatesession',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='privatesession',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='privatesession',
            name='session_mode',
            field=models.CharField(blank=True, choices=[('0', 'A session by yourself alone'), ('1', 'A session just between you and your friends'), ('2', 'A session including you and another group')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='privatesession',
            name='professor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='professor_private_sessions', to='Users.professor'),
        ),
        migrations.AlterField(
            model_name='privatesession',
            name='schedule',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='privatesession',
            name='status',
            field=models.CharField(blank=True, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='privatesession',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_private_sessions', to='Users.customuser'),
        ),
        migrations.AddField(
            model_name='privatesession',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]