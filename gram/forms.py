from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Profile,Comment 

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    fullname=forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'fullname', 'email', 'password1','password2')
       
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'title', 'description') 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post','user']

    class Meta:
        model = Comment
        fields = ('comment',)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')  
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name',  'bio', 'profile_pic')

class LoginForm(forms.ModelForm):
    username = forms.EmailField(max_length=254)
    password = forms.EmailField(max_length=254)
    
    

    class Meta:
        model = User
        fields = ('username', 'password')
       