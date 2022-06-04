from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image,Profile,Comments
from django.views.generic.edit import FormMixin


class SignupForm(UserCreationForm):