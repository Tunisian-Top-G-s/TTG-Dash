# Generated by Django 5.0.2 on 2024-03-26 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PrivateSessions', '0008_alter_privatesession_cours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatesession',
            name='session_mode',
            field=models.IntegerField(choices=[(0, 'A session by yourself alone'), (1, 'A session just between you and your friends'), (2, 'A session including you and another group')], default=0),
        ),
    ]
