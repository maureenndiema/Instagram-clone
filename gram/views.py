from django.http.response import Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from .forms import *
from .models import Post, Comment, Profile, Follow
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .email import send_welcome_email

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            name=form.cleaned_data['fullname']
            email=form.cleaned_data['email']
            
            send_welcome_email(name,email)

            user = authenticate(username=username, password=password)

            login(request, user)


            return redirect('welcome')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='/accounts/login/')
def welcome(request):
    posts=Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    profiles=Profile.objects.all()[:5]
    if request.method=='POST':
        form=UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user.profile
            post.save()


            return HttpResponseRedirect(request.path_info)

    else:
        form=UploadImageForm()
    return render(request, 'instagram/index.html',{'posts':posts,'form':form,'users':users,'profiles':profiles})

def logout_view(request):
    logout(request,"welcome.html")

@login_required(login_url='/accounts/login/')
def comment(request,post_id):
        current_user=request.user.profile
        post = Post.objects.get(id=post_id)
        user_profile = User.objects.get(username=current_user.user)
        comments = Comment.objects.all()
        if request.method == 'POST':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.post = post
                        comment.user = request.user.profile
                        comment.save()  
                return HttpResponseRedirect(request.path_info)
        else:
                form = CommentForm()
        params = {
        'post': post,
        'form': form,
        'comments': comments,
    }
        return render(request, 'instagram/comment.html',params)
def like_post(request,post_id):
    post = Post.objects.get(pk=post_id)
    is_liked=False
    user=request.user.profile
    try:
        profile=Profile.objects.get(user=user.user)
        print(profile)

    except Profile.DoesNotExist:
        raise Http404()
    if post.likes.filter(id=user.user.id).exists():
        post.likes.remove(user.user)
        is_liked=False
    else:
        post.likes.add(user.user)
        is_liked=True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def search_results(request):
    posts=Post.objects.all()

    if 'search_profile' in request.GET and request.GET["search_profile"]:
        search_term = request.GET.get("search_profile")
        searched_profiles = Profile.search_profile(search_term)
        print(searched_profiles)
        message = f"{search_term}"
        return render(request, 'instagram/search_results.html', {"message":message,"profiles": searched_profiles})
    else:
        message = "You haven't searched for any profile"
    return render(request, 'instagram/search_results.html', {'message': message,'posts':posts})

@login_required()
def profile(request, username):
    current_user=request.user.profile
 
    profile=Profile.objects.get(user=current_user.user)
    posts = request.user.profile.posts.all()

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.profile=profile
            user.profile = request.user.profile
            user.save()

            prof = profile_form.save(commit=False)
            prof.profile=profile
            prof.profile = request.user.profile
            prof.save() 


            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'profile_form': profile_form,
        'posts': posts,

    }
    return render(request, 'instagram/profile.html', params)
    
@login_required()
def update_profile(request, username):
    current_user=request.user.profile

    user_profile = get_object_or_404(User, username=username)
    if request.user == user_profile:
        return redirect('profile', username=request.user.username)

    profile1=Profile.objects.get(user=current_user.user)
   
    user_posts = user_profile.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_profile.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_profile': user_profile,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status,
        'profile1':profile1,
    }
    return render(request, 'instagram/updated_profile.html', params)

def follow(request,follow):
    if request.method == 'GET':
        user_follow=Profile.objects.get(pk=follow)
        follow_user=Follow(follower=request.user.profile, followed=user_follow)
        follow_user.save()
        return redirect('user_profile',user_follow.user.username)
def unfollow(request,unfollow):
    if request.method=='GET':
        user_unfollow=Profile.objects.get(pk=unfollow)
        unfollow_user=Follow.objects.filter(follower=request.user.profile,followed=user_unfollow)
        unfollow_user.delete()
        return redirect('user_profile',user_unfollow.user.username)
    