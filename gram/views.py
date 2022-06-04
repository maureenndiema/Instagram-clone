from django.shortcuts import render
from django.http  import HttpResponse
from django.contrib.auth import login, authenticate
from .models import Image,Profile,Comments
import datetime as dt

# Create your views here.
