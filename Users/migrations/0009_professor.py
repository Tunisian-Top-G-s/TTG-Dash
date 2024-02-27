# Generated by Django 5.0.2 on 2024-02-24 19:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_customuser_last_added_points_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professor', to='Users.customuser')),
            ],
        ),
    ]
