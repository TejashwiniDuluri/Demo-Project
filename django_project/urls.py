"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from django.views.generic.base import TemplateView
#from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
 #path(r'^', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^', include('polls.urls')),
    url(r'^', include('projects.urls')),
    url(r'^', include('mirror.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social_django.urls', namespace='social')),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #path('polls/', include('django.contrib.auth.urls')),
    #path('edx_auth/', views.edx_auth.as_view(), name='edx_auth'),
]

