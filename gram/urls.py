from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[

    path('image/(\d+)', views.image, name ='image'),
    path('signup/$', views.signup, name='signup'),
    path('new/image$', views.new_image, name='new-image'),
    path('profile/(\d+)', views.profile, name='profile'),
    path('newprofile/', views.new_profile, name='new_profile'),
    path('search/$', views.search_user, name='search_profile'), 
    path('comment/(?P<image_id>\d+)', views.add_comment, name='comment'), 

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
