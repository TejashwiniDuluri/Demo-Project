from django.conf.urls import url,include

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()





from . import views
urlpatterns = [
	url(r'^compiler/$', views.compiler,name="compiler"),
	url(r'^pyExec/$', views.pyExec,name="pyExec"),
]
