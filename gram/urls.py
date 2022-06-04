from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[

path(r'^image/(\d+)',views.image,name ='image'),
    path(r'^signup/$', views.signup, name='signup'),
    path(r'^new/image$', views.new_image, name='new-image'),
    path(r'^profile/(\d+)', views.profile, name='profile'),
    path(r'^newprofile/', views.new_profile, name='new_profile'),
    path(r'^search/$', views.search_user, name='search_profile'), 
    path(r'^comment/(?P<image_id>\d+)', views.add_comment, name='comment'), 

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
