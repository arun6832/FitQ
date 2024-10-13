import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from .models import WellnessTable, Feedback, UserDetails
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password



def index(request):
    return render(request, 'index.html')




def create_ac(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password2 = request.POST.get('password2')
        password1 = request.POST.get('password1')
        if User.objects.filter(username=username):
            msg = 'This username already exists please login to continue!'
            return render(request, 'sign_in.html', {'msg': msg})
        
        if password1 != password2:
            msg = "Passwords do not match!"
            return render(request, 'sign_in.html', {'msg': msg})
        
        else:
            user = User.objects.create_user(username=username, first_name = first_name, last_name = last_name, email=email)
            user.set_password(password1)
            user.save()
            msg = "user created successfully"
            return render(request, 'userdashboard/user_details.html', {'msg': msg})
        
    
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

# Sign-in view
def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password2 = request.POST['password2']

        print(f"Trying to authenticate user: {email}")
        print(f"Password provided: {password2}")

        # Fetch the user based on the email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password2)
        except User.DoesNotExist:
            print("User does not exist.")
            msg = "Invalid Credentials. Please try again!"
            return render(request, 'sign_in.html', {'msg': msg})

        if user is not None:
            login(request, user)
            return redirect('userdashboard')  # Redirect to the user dashboard page
        else:
            print("Authentication failed.")
            msg = "Invalid Credentials. Please try again!"
            return render(request, 'sign_in.html', {'msg': msg})

    return render(request, 'sign_in.html')



# User details view (protected, requires login)
@login_required
def user_details(request):
    if request.method == 'POST':
        # Extract data from the form
        username = request.POST.get('username')  # Ensure that this matches the name attribute in the HTML form
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('dob')  # Format YYYY-MM-DD for DateField
        country = request.POST.get('country')
        employment_status = request.POST.get('employment')
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        # Debugging: Print form data to verify
        print("Username:", username)
        print("Gender:", gender)
        print("Date of Birth:", date_of_birth)
        print("Country:", country)
        print("Employment Status:", employment_status)
        print("Height:", height)
        print("Weight:", weight)

        # Get the user from the User model
        try:
            usr = User.objects.get(username=username)
        except User.DoesNotExist:
            print("User not found")
            return render(request, 'userdashboard/user_details.html', {'error': 'User not found'})

        # Create and save the UserDetails object
        user_detail, created = UserDetails.objects.get_or_create(
            user=usr,
            defaults={
                'gender': gender,
                'date_of_birth': date_of_birth,
                'country': country,
                'employment_status': employment_status,
                'height': height,
                'weight': weight,
                'is_profile_complete': True
            }
        )
        if created:
            print("New user details added.")
        else:
            print("User details already exist.")

        return redirect('user_dashboard')  # Redirect to some other page after successful entry

    return render(request, 'userdashboard/user_details.html')

def feedback_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(name)
        feedbak = Feedback.objects.create(name = name, email = email, message = message)
        feedbak.save()
        return redirect(userdashboard)
    return render(request, 'userdashboard/feedbackform.html')

def create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # UserDetails fields
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        country = request.POST.get('country')
        employment = request.POST.get('employment')
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        # Check if passwords match
        if password1 != password2:
            msg = "Passwords do not match!"
            return render(request, 'sign_in.html', {'msg': msg})

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            msg = "Username already exists!"
            return render(request, 'sign_in.html', {'msg': msg})

        if User.objects.filter(email=email).exists():
            msg = "Email already exists!"
            return render(request, 'sign_in.html', {'msg': msg})

        # Create the User object
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password1)
        )
        user.save()

        # Create UserDetails record
        user_details = UserDetails.objects.create(
            user=user,
            gender=gender,
            date_of_birth=dob,
            country=country,
            employment_status=employment,
            height=height,
            weight=weight,
            is_profile_complete=False
        )
        user_details.save()

        # Automatically log in the user after sign up
        login(request, user)

        # Redirect to dashboard after successful registration
        return redirect('userdashboard')  # Change to your appropriate dashboard

    return render(request, 'sign_in.html')