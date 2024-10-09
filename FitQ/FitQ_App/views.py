import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from .models import WellnessTable
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'index.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password2 = request.POST['password2']
        print(email, password2)
        user = authenticate(request, username=email, password=password2)
        print(user)
        if user is not None:

            if user.is_superuser:
                login(request,user)
                return redirect('index')
            elif user.is_active == 1:
                login(request,user)
                return redirect('index')
            else:
                msg = "You are not autherized for this login"
                return render(request, 'sign_in.html', {'msg': msg})
        else:
            msg = "Invalid Credentials. Please try again!"
            return render(request, 'sign_in.html', {'msg': msg})
    return render(request, 'sign_in.html')


def create_ac(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password2 = request.POST.get('password2')
        password1 = request.POST.get('password1')
        
        if User.objects.filter(username=username):
            msg = 'This username already exists please login to continue!'
            return render(request, 'sign_in.html', {'msg': msg})
        
        if password1 != password2:
            msg = "Passwords do not match!"
            return render(request, 'sign_in.html', {'msg': msg})
        
        else:
            user = User.objects.create_user(username=username)
            user.set_password(password1)
            user.save()

            msg = "user created successfully ,please login to continue!"
            return render(request, 'sign_in.html', {'msg': msg})
        
    
    return render(request, 'sign_in.html')
    

@csrf_exempt
def auth_receiver(request):
    token = request.POST.get('credential')

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # Save user data in session
    request.session['user_data'] = user_data

    return redirect('sign_in')

def sign_out(request):
    # Remove user data from session
    logout(request)
    return redirect('index')

@login_required(login_url='sign_in')

def mytrack(request):
    # Remove user data from session
    logout(request)
    return redirect('userdashboard')

def userdashboard(request):
    return render(request, 'userdashboard/userdashboard.html')

def daily(request):
    return render(request, 'userdashboard/daily.html')

def usercalender(request):
    return render(request,'userdashboard/usercalender.html')

from .models import WellnessTable  # Import the WellnessTable model

def monitoring(request):
    context = {}

    if request.method == 'POST':
        # Extract data from the form
        sleep_duration = request.POST.get('sleep_duration_hours')
        workout_duration = request.POST.get('workout_duration')
        problems_during_day = request.POST.get('problems_during_day')
        water_intake = request.POST.get('water_intake_liters')
        screen_time = request.POST.get('screen_time')
        food_on_time = request.POST.get('food_on_time')
        type_of_food = request.POST.get('type_of_food')
        smoking_habit = request.POST.get('smoking_habit')
        alcohol_consumption = request.POST.get('alcohol_consumption')

        # Create a new WellnessTable object and save it to the database
        wellness_entry = WellnessTable(
            day="1",  # Set the appropriate day (you might want to capture this from the form)
            sleep_duration_hours=sleep_duration,
            workout_duration=workout_duration,
            problems_during_day=problems_during_day,
            water_intake_liters=water_intake,
            screen_time=screen_time,
            food_on_time=food_on_time,
            type_of_food=type_of_food,
            smoking_habit=smoking_habit,
            alcohol_consumption=alcohol_consumption
        )
        wellness_entry.save()  # Save the entry to the database

        # Add the data to context for display in the success message
        context['sleep_duration'] = sleep_duration
        context['workout_duration'] = workout_duration
        context['problems_during_day'] = problems_during_day
        context['water_intake'] = water_intake
        context['screen_time'] = screen_time
        context['food_on_time'] = food_on_time
        context['type_of_food'] = type_of_food
        context['smoking_habit'] = smoking_habit
        context['alcohol_consumption'] = alcohol_consumption
        
        # Optionally, add a success flag to show the success message
        context['success'] = True

    return render(request, 'userdashboard/daily.html', context)