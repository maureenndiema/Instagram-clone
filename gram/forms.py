from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image,Profile,Comments
from django.views.generic.edit import FormMixin


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['image_name', 'pub_date','profile','user']
        widgets = {
            'likes': forms.CheckboxSelectMultiple(),
    }

class ProfileForm(forms.ModelForm):

    class Meta:
        model =Profile
        exclude=['user']

class CommentsForm(forms.ModelForm):
   class Meta:
       model = Comments
       fields = [ 'comment' ]         