# Generated by Django 5.1 on 2024-10-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitQ_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WellnessTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('sleep_duration_hours', models.DecimalField(decimal_places=1, max_digits=4)),
                ('workout_duration', models.CharField(choices=[('15 minutes', '15 minutes'), ('45 minutes', '45 minutes'), ('More than 45 minutes', 'More than 45 minutes'), ('No workout', 'No workout')], max_length=50)),
                ('problems_during_day', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('water_intake_liters', models.DecimalField(decimal_places=1, max_digits=4)),
                ('screen_time', models.DecimalField(decimal_places=1, max_digits=4)),
                ('food_on_time', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('type_of_food', models.CharField(choices=[('Healthy', 'Healthy'), ('Junk', 'Junk')], max_length=10)),
                ('smoking_habit', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('alcohol_consumption', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]