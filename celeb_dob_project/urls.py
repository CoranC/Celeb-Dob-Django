from django.conf.urls import patterns, include, url
from django.contrib import admin
from celeb_dob import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', views.home, name='home'),
    url(r'^get_celebrity/$', views.get_celebrity, name='get_celebrity'),
)
