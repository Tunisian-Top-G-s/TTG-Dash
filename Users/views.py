import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
""" from .forms import SignUpForm, LogInForm """
from .models import CustomUser
from django.contrib import messages



# Create your views here.