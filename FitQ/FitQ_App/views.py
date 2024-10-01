import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
                return redirect('index')
            elif user.is_active == 1:
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
    if 'user_data' in request.session:
        del request.session['user_data']
    return redirect('sign_in')
