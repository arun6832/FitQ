from django.urls import path
from . import views

urlpatterns=[
    path('',views.FitQ_App, name="FitQ_App"),
]