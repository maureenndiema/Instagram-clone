from django.shortcuts import render
from django.http  import HttpResponse
from django.contrib.auth import login, authenticate
from .models import Image,Profile,Comments
import datetime as dt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,NewImageForm,ProfileForm,CommentsForm
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from friendship.models import Friend, Follow, Block

# Create your views here.
@login_required(login_url='/accounts/login/')
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required(login_url='/accounts/login/')
def instagram(request):
    images = Image.objects.all()
    print(images)
    profiles = Profile.objects.all()
    people = Follow.objects.following(request.user)
    comments = Comments.objects.all()
    profileimage=  User.objects.all()
    
    return render(request,'instagram.html',{"images":images, "profiles":profiles , "people":people,"comments":comments,"profileimage":profileimage})

@login_required(login_url='/accounts/login/')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user.profile
            image.user = current_user

            image.save()
        return redirect('instagram')

    else:
        form = NewImageForm()
    return render(request, 'new_image.html', {"form": form})

  
@login_required(login_url='/accounts/login/')
def search_user(request):
   """
   Function that searches for profiles based on the usernames
   """
   if 'username' in request.GET and request.GET["username"]:
       name = request.GET.get("username")
       searched_profiles = User.objects.filter(username__icontains=name)
       message = f"{name}"
       profiles = User.objects.all()
       people = Follow.objects.following(request.user)
       print(profiles)
       return render(request, 'all-insta/search.html', {"message":message, "usernames":searched_profiles, "profiles":profiles,})  

