# Generated by Django 5.1 on 2024-11-07 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitQ_App', '0014_trainer_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
