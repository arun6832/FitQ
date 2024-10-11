import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from .models import WellnessTable, Feedback
from .forms import FeedbackForm
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

  
    request.session['user_data'] = user_data

    return redirect('sign_in')

def sign_out(request):

    logout(request)
    return redirect('index')

@login_required(login_url='sign_in')

def mytrack(request):

    logout(request)
    return redirect('userdashboard')

import requests
from django.shortcuts import render

def fetch_news():
    api_key = '7451378a56084e16b51e75e922fcef47'  
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        articles = data.get('articles', [])
        return articles
    else:
        return []

def userdashboard(request):
    articles = fetch_news()  
    return render(request, 'userdashboard/userdashboard.html', {'articles': articles})


def daily(request):
    return render(request, 'userdashboard/daily.html')

def usercalender(request):
    return render(request,'userdashboard/usercalender.html')

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

       
        wellness_entry = WellnessTable(
            day="1",  
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
        wellness_entry.save()
        context['sleep_duration'] = sleep_duration
        context['workout_duration'] = workout_duration
        context['problems_during_day'] = problems_during_day
        context['water_intake'] = water_intake
        context['screen_time'] = screen_time
        context['food_on_time'] = food_on_time
        context['type_of_food'] = type_of_food
        context['smoking_habit'] = smoking_habit
        context['alcohol_consumption'] = alcohol_consumption
        
        context['success'] = True

    return render(request, 'userdashboard/daily.html', context)

def feedback_success(request):
    return render(request, 'userdashboard/feedback_success.html')

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('feedback_success')  # Redirect to a success page
    else:
        form = FeedbackForm()  # Create an empty form instance
    
    return render(request, 'userdashboard/feedbackform.html', {'form': form})