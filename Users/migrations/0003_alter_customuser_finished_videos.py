# Generated by Django 5.0.2 on 2024-03-28 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0002_initial'),
        ('Users', '0002_customuser_finished_videos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='finished_videos',
            field=models.ManyToManyField(blank=True, null=True, to='Courses.video'),
        ),
    ]
