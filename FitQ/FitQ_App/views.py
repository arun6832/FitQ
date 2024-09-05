import os
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def sign_in(request):
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
