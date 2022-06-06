from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('login', views.login , name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup_view, name='signup'),
    path('', views.welcome, name='welcome'),
    path('comment/<post_id>', views.comment, name='comment'),
    re_path('like/(?P<post_id>\d+)',views.like_post,name='LikePost'),
    re_path(r'^search/', views.search_results,name='search_results'),
    path('profile/<username>/', views.profile, name='profile'),
    path('user_profile/<username>/', views.update_profile, name='user_profile'),
    path('unfollow/<unfollow>', views.unfollow, name='unfollow'),
    path('follow/<follow>', views.follow, name='follow'),
    
   
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
