from django.contrib import admin
from django.urls import path
from .views import *  # Import the view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('auth_receiver/', auth_receiver, name='auth_receiver'),
    path('sign_out/', sign_out, name='sign_out'),
    path('mytrack/',mytrack, name='mytrack'),
    path('create_ac/',create_ac,name='create'),
    path('userdashboard/',userdashboard,name='userdashboard'),
    path('daily/',daily,name='daily'),
    path('monitoring/',monitoring,name='monitoring'),
    path('usercalender/',usercalender,name='usercalender'),
     path('sign_in/', sign_in, name='sign_in'),
    path('user_details/', user_details, name='user_details'),
    path('feedback/', feedback_form, name='feedback'),
    path('create/', create, name='create'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('chatbot/', chatbot, name='chatbot'),
    path('chatbot/response/', chatbot_response, name='chatbot_response'),
    path('trainer_consulting',trainer_consulting,name='trainer_consulting'),
    path('chatbot/response/<str:pk>/', chatbot_response, name='chatbot_response'),
    path('trainerdashboard',trainerdashboard,name='trainerdashboard'),
    path('useranalytics',useranalytics,name='useranalytics'),
    path('trainersignup/', trainer_signup, name='trainer_signup'),
    path('trainerlogin/',trainer_login, name='trainerlogin'), 
]