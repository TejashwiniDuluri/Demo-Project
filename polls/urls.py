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
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  
    url(r'^admin/', admin.site.urls),
    url(r'^register$', views.user_register, name='user_register'),
    url(r'^auth$', views.edx_auth, name='edx_auth'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^accounts/login/$', views.index, name='wrong url to home'),
    url(r'^message$',views.message,name='message'),
    url(r'^notifications$',views.message_service,name='message_service'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^my_account/$',views.my_account,name='my_account'),
    #url(r'^simple_upload/$',views.simple_upload,name='simple_upload')
    # url('^', include('django.contrib.auth.urls')),
    url(r'^upload_pp/$', views.upload_pp, name="upload_pp"),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^course/(?P<a>[0-9]+)/$', views.course_chapt, name='course_chapt'),
    url(r'^courseAjax/(?P<a>[0-9]+)/$', views.course_chapt_ajax, name='course_chapt_ajax'),
    url(r'^topics/(?P<a>[0-9]+)/$', views.chapt_topics, name='chapt_topics'),
    url(r'^topic/(?P<a>[0-9]+)/$', views.topic, name='topic'),
    url(r'^test/(?P<a>[0-9]+)/$', views.test_launch, name='test_launch'),
    url(r'^testcal/$', views.test_cal, name='test_cal'), 
    url(r'^timeline/$', views.timeline, name='timeline'),
    url(r'^jsfiddle/$', views.jsfiddle, name='jsfiddle'),
    url(r'^accounts/login/$', views.index, name='wrong url to home'),
    url(r'^upload/$', views.upload_file, name='upload_file'),
    url(r'^assign/(?P<a>[0-9]+)/$', views.assign, name='assign'),
    url(r'^assign_result/$', views.assign_result, name='assign_result'),
    url(r'^add_course/$', views.add_course, name='add_course'),
    url(r'^add_chapter/$', views.add_chapter, name='add_chapter'),
    url(r'^test_success_page/(\d+)/$', views.test_success_page, name='test_success_page'),
    url(r'^assign_success_page/(\d+)/$', views.assign_success_page, name='assign_success_page'),
    url(r'^reg_courses/$', views.reg_courses, name='reg_courses'),
    url(r'^course_report/(?P<a>[0-9]+)/$', views.course_report, name='course_report'),
    url(r'^user_report/(?P<a>[0-9]+)/$', views.user_report, name='user_report'),
    url(r'^chapt/(?P<a>[0-9]+)/$', views.chapt, name='chapt'),              
    url(r'^skills_set/$', views.skills_set, name='skills_set'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^cart_checkout/(\d+)/$', views.cart_checkout, name='cart_checkout'),
    url(r'^cart_item_delete/(\d+)/$', views.cart_item_delete, name='cart_item_delete'),
    url(r'^add_to_cart/(\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^ssh/$', views.userSSH, name='userSSH'),
    url(r'^userUpdate/$', views.userUpdate, name='userUpdate'),
    url(r'^mentorRegister/$', views.mentorRegister, name='mentorRegister'),
    url(r'^empRegister/$', views.empRegister, name='empRegister'),
    url(r'^group/$', views.group, name='group'),
    url(r'^mentorUpdate/$', views.mentorUpdate, name='mentorUpdate'),
    url(r'^empUpdate/$', views.empUpdate, name='empUpdate'),
    url(r'^test_creation/$', views.test_creation, name='test_creation'),
    url(r'^chapt_topic_ajax/(?P<a>[0-9]+)/$', views.chapt_topic_ajax, name='chapt_topic_ajax'),
    url(r'^test_ques/(?P<a>[0-9]+)/$', views.test_ques, name='test_ques'),
    url(r'^course_chapter_ajax/(?P<a>[0-9]+)/$', views.course_chapter_ajax, name='course_chapter_ajax'),
    url(r'^create_project/$', views.create_project, name='create_project'),
    url(r'^course_project_ajax/(?P<a>[0-9]+)/$', views.course_project_ajax, name='course_project_ajax'),
    url(r'^create_project_chapter/$', views.create_project_chapter, name='create_project_chapter'),
    url(r'^assignment_create/$', views.assignment_create, name='assignment_create'),
    url(r'^assignment_display/(?P<a>[0-9]+)/$', views.assignment_display, name='assignment_display'),
    url(r'^students_display/(?P<a>[0-9]+)/$', views.students_display, name='students_display'),
    url(r'^student_resume/(?P<a>[0-9]+)/$', views.student_resume, name='student_resume'),
    url(r'^shortlist_students/(?P<a>[0-9]+)/(?P<b>[0-9]+)/$', views.shortlist_students, name='shortlist_students'),
    url(r'^course_nav_bar/$', views.course_nav_bar, name='course_nav_bar'),
    url(r'^employer_task_create/(?P<a>[0-9]+)/$', views.employer_task_create, name='employer_task_create'),
    url(r'^user_messages/$', views.user_messages, name='user_messages'),
    url(r'^message_reply/(?P<a>[0-9]+)/$', views.message_reply, name='message_reply'),
    url(r'^message_delete/(?P<a>[0-9]+)/$', views.message_delete, name='message_delete'),





    #url(r'^oauth/login/linkedin-oauth2/$',views.index,name='wrong url to home'),
    #url(r'^oauth/complete/linkedin-oauth2/&response_type=code&client_id=814w15hmuju4jq$', views.index, name='wrong url to home'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

