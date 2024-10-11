from django.contrib import admin
from django.urls import path
from FitQ_App import views  # Import your views here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('auth_receiver/', views.auth_receiver, name='auth_receiver'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('mytrack/', views.mytrack, name='mytrack'),
    path('create_ac/',views.create_ac,name='create'),
    path('userdashboard/',views.userdashboard,name='userdashboard'),
    path('daily/',views.daily,name='daily'),
    path('monitoring/',views.monitoring,name='monitoring'),
    path('usercalender/',views.usercalender,name='usercalender'),
<<<<<<< HEAD
    path('user_details/',views.user_details,name='user_details'),
=======
    path('feedbackform/',views.feedback,name='feedbackform'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/success/', views.feedback_success, name='feedback_success'),
>>>>>>> 54d78ded09ea0b099183813de6692aa0d0a9cd40
]
