import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from .models import MyUser, WellnessTable, Feedback, UserDetails
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages 
from django.utils import timezone
from gtts import gTTS
from django.conf import settings
from django.views import View




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

def daily(request):
    return render(request, 'userdashboard/daily.html')

def usercalender(request):
    return render(request,'userdashboard/usercalender.html')

@login_required
def monitoring(request):
    if request.method == 'POST':
        # Extract form data
        sleep_duration = request.POST.get('sleep_duration_hours')
        workout_duration = request.POST.get('workout_duration')
        problems_during_day = request.POST.get('problems_during_day')
        water_intake = request.POST.get('water_intake_liters')
        screen_time = request.POST.get('screen_time')
        food_on_time = request.POST.get('food_on_time')
        type_of_food = request.POST.get('type_of_food')
        smoking_habit = request.POST.get('smoking_habit')
        alcohol_consumption = request.POST.get('alcohol_consumption')

        # Debugging: print all values
        print("Form Data:", {
            'user': request.user,
            'day': "1",
            'sleep_duration': sleep_duration,
            'workout_duration': workout_duration,
            'problems_during_day': problems_during_day,
            'water_intake': water_intake,
            'screen_time': screen_time,
            'food_on_time': food_on_time,
            'type_of_food': type_of_food,
            'smoking_habit': smoking_habit,
            'alcohol_consumption': alcohol_consumption
        })

        try:
            # Create and save a new wellness entry
            wellness_entry = WellnessTable(
                user=request.user,
                day="1",
                sleep_duration_hours=float(sleep_duration),  # Ensure conversion to float
                workout_duration=workout_duration,
                problems_during_day=problems_during_day,
                water_intake_liters=float(water_intake),  # Ensure conversion to float
                screen_time=float(screen_time),  # Ensure conversion to float
                food_on_time=food_on_time,
                type_of_food=type_of_food,
                smoking_habit=smoking_habit,
                alcohol_consumption=alcohol_consumption
            )
            wellness_entry.save()
            messages.success(request, 'Details saved successfully!')
            return render(request, 'userdashboard/daily.html', {
                'success': True,
                # Pass the submitted data back to the template
                'sleep_duration': sleep_duration,
                'workout_duration': workout_duration,
                'problems_during_day': problems_during_day,
                'water_intake': water_intake,
                'screen_time': screen_time,
                'food_on_time': food_on_time,
                'type_of_food': type_of_food,
                'smoking_habit': smoking_habit,
                'alcohol_consumption': alcohol_consumption,
            })
        except Exception as e:
            messages.error(request, 'An error occurred while saving your data: {}'.format(str(e)))
            print("Error:", e)  # Print the error message for debugging
            print("Error type:", type(e)._name_)  # Print the type of error

    return render(request, 'userdashboard/daily.html', {'success': False})

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

@login_required
def userdashboard(request):
    try:
        # Fetch user details from UserDetails model
        user_details = UserDetails.objects.get(user=request.user)
        
        # Calculate BMI
        if user_details.height > 0:
            height_in_meters = user_details.height / 100
            bmi = round(user_details.weight / (height_in_meters ** 2), 2)
        else:
            bmi = None

        # Get the user's registration date
        start_date = request.user.date_joined
        
        # Generate date data for the next 7 days
        days_data = []
        for i in range(7):  # For 7 days
            day_date = start_date + timezone.timedelta(days=i)
            day_number = i + 1
            
            # Check if the user has filled out the daily form for that day
            try:
                daily_form = WellnessTable.objects.filter(user=request.user, day=day_number)
                filled_status = 'Filled'
                payment_status = 'Paid'  # You can adjust this based on your logic
            except WellnessTable.DoesNotExist:
                filled_status = 'Not Filled'
                payment_status = 'Pending' if i == 0 else 'Paid'  # Example logic for payment status

            days_data.append({
                'day': f'Day {day_number}',
                'date': day_date.date(),  # Get just the date part
                'status': filled_status,  # Status based on form submission
                'payment_status': payment_status  # Payment status
            })

    except UserDetails.DoesNotExist:
        user_details = None
        bmi = None
        days_data = []  # No data for days if UserDetails does not exist

    context = {
        'user_details': user_details,
        'bmi': bmi,
        'days_data': days_data,
    }

    return render(request, 'userdashboard/userdashboard.html', context)

@login_required
def edit_profile(request):
    user_details = UserDetails.objects.get(user=request.user)

    if request.method == 'POST':
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        # Update user details
        user_details.height = height
        user_details.weight = weight
        user_details.save()

        return redirect('userdashboard')  # Redirect after saving
    # Render the edit profile page
    context = {
        'user_details': user_details,
    }
    return render(request, 'userdashboard/edit_profile.html', context)



chatbot_responses = {
    "hello": "Hi! How can I assist you today?",
    "how are you?": "I'm just a bot, but thanks for asking!",
    "what is your name?": "I am your fitness assistant bot.",
    "help": "I can assist you with your fitness questions.",
    "what should I eat after a workout?": "It's great to consume a mix of protein and carbs after a workout. A protein shake or a meal with chicken and rice works well!",
    "how much water should I drink?": "It's generally recommended to drink about 2 liters (or 8 cups) of water per day, but it varies based on your activity level.",
    "what is a good workout routine for beginners?": "A good beginner routine includes a mix of cardio and strength training. Start with 30 minutes of walking or jogging, and incorporate bodyweight exercises like push-ups and squats.",
    "how do I lose weight fast?": "The best way to lose weight is through a combination of a healthy diet and regular exercise. Aim for a calorie deficit and stay active!",
    "what is a healthy breakfast?": "A healthy breakfast could include oatmeal with fruits, yogurt with granola, or eggs with spinach.",
    "how often should I exercise?": "Aim for at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week, plus strength training on two or more days.",
    "what are some good exercises for building muscle?": "Exercises like bench presses, squats, deadlifts, and pull-ups are great for building muscle.",
    "how can I stay motivated to exercise?": "Set specific goals, find a workout buddy, and track your progress to stay motivated!",
    "what are some benefits of yoga?": "Yoga can improve flexibility, reduce stress, and enhance overall well-being.",
    "how do I improve my flexibility?": "Incorporate stretching into your routine and try yoga to improve flexibility.",
    "what is the best time to exercise?": "The best time to exercise is when it fits into your schedule! Consistency is key.",
    "how do I prevent injuries while exercising?": "Warm up before workouts, use proper form, and listen to your body to prevent injuries.",
    "what are some tips for healthy snacking?": "Choose snacks like fruits, nuts, yogurt, or veggies with hummus for healthy options.",
    "how can I get abs?": "Focus on a combination of diet, cardio, and targeted exercises like planks and crunches.",
    "is it okay to eat late at night?": "It's okay to eat late, but try to keep it light and healthy to avoid sleep disruption.",
    "how do I deal with cravings?": "Stay hydrated, eat regular meals, and opt for healthy alternatives when cravings hit.",
    "what supplements should I take?": "It's best to consult with a healthcare provider to determine what supplements are right for you based on your diet and goals.",
    "how can I track my progress?": "Keep a workout journal, use fitness apps, or take progress photos to track your improvements."
}


@login_required
def chatbot(request):
    return render(request, 'userdashboard/chatbot.html')

@login_required
def chatbot_response(request):
    user_message = request.GET.get('message', '').lower()
    response = get_chatbot_response(user_message)
    return JsonResponse({'response': response})

def get_chatbot_response(user_message):
    return chatbot_responses.get(user_message, "Sorry, I didn't understand that.")


