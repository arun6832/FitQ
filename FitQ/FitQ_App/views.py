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
import json
from django.db import models  


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
    user = request.user

    # Check if the session variable 'current_day' is set; if not, initialize to 1
    if 'current_day' not in request.session:
        request.session['current_day'] = 1

    # Check if the session variable 'completed' is set to track if the user has completed all 7 days
    if 'completed' not in request.session:
        request.session['completed'] = False

    current_day = request.session['current_day']
    details_saved = False
    success_message = ''

    if request.method == 'POST':
        # Extract form data from POST request
        sleep_duration = request.POST.get('sleep_duration_hours')
        workout_duration = request.POST.get('workout_duration')
        problems_during_day = request.POST.get('problems_during_day')
        water_intake = request.POST.get('water_intake_liters')
        screen_time = request.POST.get('screen_time')
        food_on_time = request.POST.get('food_on_time')
        type_of_food = request.POST.get('type_of_food')
        smoking_habit = request.POST.get('smoking_habit')
        alcohol_consumption = request.POST.get('alcohol_consumption')

        try:
            # Save a new wellness entry for the current day
            wellness_entry = WellnessTable(
                user=user,
                day=current_day,
                sleep_duration_hours=float(sleep_duration) if sleep_duration else 0.0,
                workout_duration=workout_duration,
                problems_during_day=problems_during_day,
                water_intake_liters=float(water_intake) if water_intake else 0.0,
                screen_time=float(screen_time) if screen_time else 0.0,
                food_on_time=food_on_time,
                type_of_food=type_of_food,
                smoking_habit=smoking_habit,
                alcohol_consumption=alcohol_consumption
            )
            wellness_entry.save()

            # Mark as saved successfully
            details_saved = True

            # If it is Day 7, set the 'completed' flag to True and show the success message
            if current_day == 7:
                request.session['completed'] = True
                success_message = "Congratulations! You have successfully filled out all 7 days of the wellness tracker."

            # Increment the day, or if current day is 7, set completed status to True
            if current_day < 7:
                current_day += 1
            else:
                current_day = 7  # Keep it at 7 since the user is done

            # Update the session with the new day
            request.session['current_day'] = current_day

        except ValueError as ve:
            messages.error(request, 'Please enter valid numerical values for sleep, water intake, and screen time.')
            print("Value Error:", ve)
        except Exception as e:
            messages.error(request, f'An error occurred while saving your data: {str(e)}')
            print("Error:", e)

    # Query all the user's entries to display previously submitted data
    submitted_data = {
        entry.day: {
            "sleep_duration": entry.sleep_duration_hours,
            "workout_duration": entry.workout_duration,
            "problems_during_day": entry.problems_during_day,
            "water_intake": entry.water_intake_liters,
            "screen_time": entry.screen_time,
            "food_on_time": entry.food_on_time,
            "type_of_food": entry.type_of_food,
            "smoking_habit": entry.smoking_habit,
            "alcohol_consumption": entry.alcohol_consumption,
        }
        for entry in WellnessTable.objects.filter(user=user)
    }

    context = {
        'details_saved': details_saved,
        'current_day': current_day,
        'completed': request.session['completed'],  # Completion status for the template
        'success_message': success_message,         # Success message for Day 7
        'submitted_data': submitted_data            # Previously submitted data for each day
    }

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

from django.db import transaction
from django.contrib.auth.hashers import make_password

from django.db import transaction
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

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

        try:
            with transaction.atomic():
                # Create the User object
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=make_password(password1)
                )
                logger.info("User created successfully: %s", user)

                # Debug print statements to verify data before creating UserDetails
                print("Gender:", gender)
                print("Employment Status:", employment)
                print("Date of Birth:", dob)
                print("Country:", country)
                print("Height:", height)
                print("Weight:", weight)

                # Convert height and weight to appropriate types
                user_details = UserDetails.objects.create(
                    user=user,
                    gender=gender,
                    date_of_birth=dob,
                    country=country,
                    employment_status=employment,
                    height=float(height),
                    weight=float(weight),
                    is_profile_complete=False
                )
                logger.info("UserDetails created successfully: %s", user_details)

            # Automatically log in the user after sign up
            login(request, user)

            # Redirect to dashboard after successful registration
            return redirect('userdashboard')  # Adjust to your appropriate dashboard

        except Exception as e:
            logger.error("Error creating UserDetails: %s", e)
            msg = "There was an error creating your account. Please try again."
            return render(request, 'sign_in.html')

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
    
    return JsonResponse({'response': response[0], 'audio_url': response[1]})

def get_chatbot_response(user_message):
    # Get the text response based on the user input
    response_text = chatbot_responses.get(user_message.lower(), "Sorry, I didn't understand that.")
    
    # Convert the response text to speech
    tts = gTTS(text=response_text, lang='en')
    
    # Save the speech to a file
    speech_file = 'media/response.mp3'
    tts.save(speech_file)
    

    return response_text, f'/media/{speech_file.split("/")[-1]}'

from decimal import Decimal
def convert_decimals_to_floats(data):
    if isinstance(data, list):
        # Recursively process each item in a list
        return [convert_decimals_to_floats(item) for item in data]
    elif isinstance(data, dict):
        # Recursively process each value in a dictionary
        return {key: convert_decimals_to_floats(value) for key, value in data.items()}
    elif isinstance(data, Decimal):
        # Convert Decimal to float
        return float(data)
    else:
        # Return other types as is
        return data

@login_required
def useranalytics(request):
    # Get the logged-in user
    user = request.user

    # Query data specific to the logged-in user
    workout_durations = list(WellnessTable.objects.filter(user=user).values('day', 'workout_duration'))
    food_counts = WellnessTable.objects.filter(user=user).values('type_of_food').annotate(count=models.Count('type_of_food'))
    sleep_heatmap = WellnessTable.objects.filter(user=user).values_list('day', 'sleep_duration_hours')
    alcohol_counts = WellnessTable.objects.filter(user=user).values('alcohol_consumption').annotate(count=models.Count('alcohol_consumption'))
    smoking_counts = WellnessTable.objects.filter(user=user).values('smoking_habit').annotate(count=models.Count('smoking_habit'))
    
    # New queries for water intake and screen time
    water_intake = WellnessTable.objects.filter(user=user).values('day', 'water_intake_liters')
    screen_time = WellnessTable.objects.filter(user=user).values('day', 'screen_time')

    # Prepare the data structures for JSON
    workout_data = {
        'days': [entry['day'] for entry in workout_durations],
        'workouts': [entry['workout_duration'] for entry in workout_durations]
    }
    food_data = {entry['type_of_food']: entry['count'] for entry in food_counts}
    sleep_data = [[entry[0], float(entry[1])] for entry in sleep_heatmap]  # Ensure this is a list of lists
    alcohol_data = {entry['alcohol_consumption']: entry['count'] for entry in alcohol_counts}
    smoking_data = {entry['smoking_habit']: entry['count'] for entry in smoking_counts}

    # Prepare the new data for water intake and screen time
    water_data = {
        'days': [entry['day'] for entry in water_intake],
        'water': [entry['water_intake_liters'] for entry in water_intake]
    }

    screen_time_data = {
        'days': [entry['day'] for entry in screen_time],
        'screen_time': [entry['screen_time'] for entry in screen_time]
    }

    # Convert all Decimal data to float
    workout_data = convert_decimals_to_floats(workout_data)
    food_data = convert_decimals_to_floats(food_data)
    sleep_data = convert_decimals_to_floats(sleep_data)
    alcohol_data = convert_decimals_to_floats(alcohol_data)
    smoking_data = convert_decimals_to_floats(smoking_data)
    water_data = convert_decimals_to_floats(water_data)
    screen_time_data = convert_decimals_to_floats(screen_time_data)

    # Send JSON data to template
    context = {
        'workout_durations': json.dumps(workout_data),
        'food_counts': json.dumps(food_data),
        'sleep_heatmap': json.dumps(sleep_data),
        'alcohol_counts': json.dumps(alcohol_data),
        'smoking_counts': json.dumps(smoking_data),
        'water_data': json.dumps(water_data),
        'screen_time_data': json.dumps(screen_time_data),
    }

    return render(request, 'userdashboard/useranalytics.html', context)



def trainer_consulting(request):
    return render(request, 'userdashboard/trainer_consulting.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Trainer


def trainerdashboard(request):
    # Check if the user is a Trainer by verifying the existence in the Trainer model
    try:
        trainer = Trainer.objects.get(email=request.user.email)
    except Trainer.DoesNotExist:
        # Redirect or return an error if the logged-in user is not a Trainer
        return redirect('/not-authorized/')  # Replace with an appropriate path or error page

    return render(request, 'trainer/trainerdashboard.html', {'trainer': trainer})


from .models import Trainer
def trainer_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()  # Normalize email to lowercase
        password = request.POST.get('password')
        name = request.POST.get('name')

        # Check if all fields are provided
        if not email or not password or not name:
            return HttpResponse("All fields are required", status=400)

        # Check if the email already exists in the database
        if Trainer.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please use a different email.", status=400)

        # Create the trainer user and hash the password
        trainer = Trainer.objects.create_trainer(email=email, password=password, name=name)
        return redirect('trainerlogin')  # Redirect to login after sign-up

    return render(request, 'trainer/trainersignup.html')



def trainer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()  # Normalize the email to lowercase
        password = request.POST.get('password')

        # Authenticate the user using email as the username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('trainerdashboard')  # Redirect to a dashboard or home page after login
        else:
            return HttpResponse("Invalid credentials", status=400)  # If authentication fails

    return render(request, 'trainer/trainerlogin.html')


import pickle
import random
from django.shortcuts import render

# Load model only once when the server starts
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# List of possible condition combinations for predictions
condition_combinations = [
    "Cardiovascular Disease, Diabetes",
    "Cardiovascular Disease, Liver Disease",
    "Cardiovascular Disease, Liver Disease, Diabetes",
    "Cardiovascular Disease, Liver Disease, Mental Health Issues",
    "Cardiovascular Disease, Mental Health Issues",
    "Diabetes",
    "Liver Disease",
    "Liver Disease, Diabetes",
    "Mental Health Issues",
    "Mental Health Issues, Cardiovascular Disease, Diabetes",
    "Mental Health Issues, Cardiovascular Disease, Liver Disease, Diabetes",
    "Mental Health Issues, Diabetes",
    "Mental Health Issues, Liver Disease",
    "Mental Health Issues, Liver Disease, Diabetes",
    "Mental Health Issues, Respiratory Disease, Cardiovascular Disease, Diabetes",
    "None",
    "Respiratory Disease",
    "Respiratory Disease, Cardiovascular Disease",
    "Respiratory Disease, Cardiovascular Disease, Diabetes",
    "Respiratory Disease, Cardiovascular Disease, Liver Disease",
    "Respiratory Disease, Cardiovascular Disease, Liver Disease, Diabetes",
    "Respiratory Disease, Cardiovascular Disease, Liver Disease, Mental Health Issues",
    "Respiratory Disease, Cardiovascular Disease, Liver Disease, Mental Health Issues, Diabetes",
    "Respiratory Disease, Cardiovascular Disease, Mental Health Issues",
    "Respiratory Disease, Diabetes",
    "Respiratory Disease, Liver Disease",
    "Respiratory Disease, Liver Disease, Diabetes",
    "Respiratory Disease, Mental Health Issues",
    "Respiratory Disease, Mental Health Issues, Diabetes",
    "Respiratory Disease, Mental Health Issues, Liver Disease",
    "Respiratory Disease, Mental Health Issues, Liver Disease, Diabetes",
]

def predict_view(request):
    # Generate a random prediction from the condition combinations list
    prediction = random.choice(condition_combinations)

    # Render the prediction to the template
    return render(request, "userdashboard/userprediciton.html", {"prediction": prediction})

def trainercalender(request):
    return render(request, 'trainer/trainercalender.html')


from .models import Message
from django.contrib import messages as flash_messages  # Django's messages framework for feedback
def contact_form_view(request):
    if request.method == 'POST':
        name = request.POST.get('cf-name')
        email = request.POST.get('cf-email')
        message_content = request.POST.get('cf-message')

        # Save the message to the database
        Message.objects.create(name=name, email=email, message=message_content)

        # Use Django's messages framework to add a success message
        flash_messages.success(request, "Your message has been sent successfully!")

        return redirect('contact')  # Redirect to a 'contact' page or another view

    return render(request, 'index.html')  # Replace 'contact_form.html' with your actual template