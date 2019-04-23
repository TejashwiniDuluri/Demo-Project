from django.conf.urls import url,include

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()





from . import views
# from views import *

urlpatterns = [
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^project/(?P<a>[0-9]+)/$', views.project, name='project'),
    url(r'^milestone/(?P<a>[0-9]+)/$', views.milestone, name='milestone'),
    url(r'^upload_milestone/$', views.upload_milestone, name='upload_milestone'),
    url(r'^project_test_launch/(?P<a>[0-9]+)/$', views.project_test_launch, name='project_test_launch'),
    url(r'^project_testcal/$', views.project_testcal, name='project_testcal'),
    url(r'^project_test_success_page/(?P<a>[0-9]+)/$', views.project_test_success_page, name='project_test_success_page'),
    url(r'^tag_file_upload/$', views.tag_file_upload, name='tag_file_upload'),
    url(r'^tag_content/(?P<a>[0-9]+)/$', views.tag_content, name='tag_content'),
    url(r'^project_register/$', views.project_register, name='project_register'),
    url(r'^project_milestones/(?P<a>[0-9]+)/$', views.project_milestones, name='project_milestones'),
    url(r'^add_proj_cart/(?P<a>[0-9]+)/$', views.add_proj_cart, name='add_proj_cart'),
    url(r'^project_cart_checkout/(?P<a>[0-9]+)/$', views.project_cart_checkout, name='project_cart_checkout'),
    url(r'^project_cart_item_delete/(?P<a>[0-9]+)/$', views.project_cart_item_delete, name='project_cart_item_delete'),
    url(r'^ProjectCart/$', views.ProjectCart, name='ProjectCart'),

    ]