# Generated by Django 5.1 on 2024-11-06 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitQ_App', '0013_trainer_alter_userdetails_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
