import time
import json
from django.shortcuts import render, redirect,get_object_or_404
import random
from random import randrange,randint
from django.forms.models import model_to_dict
from django.contrib import messages
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, sys
from django import forms
from .forms import UploadFileForm
from django_project.settings import STATIC_ROOT, MEDIA_ROOT
from polls.models import account_types
from polls.models import *
import digitalocean
from .forms import EmpForm,mentorUpdateForm,empUpdateForm
from django.core import serializers
from polls.choices import StatesOfIndia


@login_required
def change_password(request):
	try:
	    if request.method == 'POST':
	        form = PasswordChangeForm(request.user, request.POST)
	        if form.is_valid():
	            user = form.save()
	            update_session_auth_hash(request, user)  # Important!
	            messages.success(request, 'Your password was successfully updated!')
	            return redirect('change_password')
	        else:
	            messages.error(request, 'Please correct the error below.')
	    else:
	        form = PasswordChangeForm(request.user)
	    return render(request, 'polls/change_password.html', {
	        'form': form
	    })
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Change Password Please Try Again"
		}
		return HttpResponse(template.render(context,request))

@login_required
def upload_pp(request):
	try:
		if request.method == 'POST':
			#root_path='/home/sentinal/Documents/django_project/polls/static/media/pp/'
			a=request.FILES["picture"]
			path= MEDIA_ROOT+"/pp/"+request.user.username+"/"+"profile.jpg"
			directory = os.path.dirname(path)
		
			if not os.path.exists(directory):
				os.makedirs(directory)
				if a:
					with open(path,'wb+') as destination:
						for chunk in a.chunks():	
							destination.write(chunk)
			elif os.path.exists(directory):	
				if a:
					with open(path,'wb+') as destination:
						for chunk in a.chunks():	
							destination.write(chunk)
								
			return HttpResponseRedirect('/') 
		else:
			template = loader.get_template('polls/pp_form.html')	
			context={}
			return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html') 
		context={
		'error':e 
		}
		return HttpResponse(template.render(context,request))
			
def my_account(request):
	try:
		reg=Registered_courses.objects.filter(user=request.user)
		template = loader.get_template('polls/my_account.html')
		context = {"reg":reg}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Uploading Profile Picture Failed Please Try Again" 
		}
		return HttpResponse(template.render(context,request))
			#return HttpResponse("Failed To Load Your Profile Please Try Again")
@login_required
def reg_courses(request):
	try:
		active=Registered_courses.objects.filter(user=request.user)
		template = loader.get_template('polls/active_courses.html')
		context = {"active":active}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e 
		}
		return HttpResponse(template.render(context,request))

def index(request):
	if request.user.is_authenticated():
		try:
			a = Account.objects.get(email=request.user.email)
			last=request.user.registered_topics_set.last()
			print last
			template=loader.get_template('polls/index.html')
			if last:
				weight=sum([b.topic.percentage for b in a.registered_topics_set.filter(course=last.course)])
				context={"total_tests":TestResult.objects.all(),"courses":a.registered_courses_set.all(), "last":last, "weight":weight}
			

			context={"total_tests":TestResult.objects.all(),"courses":a.registered_courses_set.all(), "last":last}
			return HttpResponse(template.render(context,request))
		except Exception as e:
			template=loader.get_template('polls/index.html')
			context={
			'error':e
			}
			return HttpResponse(template.render(context,request))
	else:
		states=StatesOfIndia.get_state_names()
		types=dict(account_types)
		print types
		template=loader.get_template('polls/index.html')
		context={'types':types.values(),"states":states,}
		return HttpResponse(template.render(context,request))

@login_required
def message_service(request):
	try:
		template=loader.get_template('polls/message.html')
		return JsonResponse({"messages":len(Message.objects.filter(reciever=request.user).values())})
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed Please Try Again"
		}
		return HttpResponse(template.render(context,request))


def user_register(request):
		# try:
		
	# try:
	Account.objects.create_user(location=request.POST['locations'],email = request.POST['email'], password = request.POST['password'],username=request.POST['username'], phone_number = request.POST['phone_number'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],address=request.POST['address'])

	# except Exception as e:
	# 		return HttpResponse("Failed To Register User Please Try Again")
	template=loader.get_template('polls/user_register.html')
	context={}
	return HttpResponse(template.render(context,request))
		
		# except Exception as e:
		# 	template=loader.get_template('polls/error_message.html')
		# 	context={
		# 	'error':"Failed To Load "
		# 	}
		# 	return HttpResponse(template.render(context,request))

@login_required
def mentorRegister(request):
	try:
		if request.method=='POST':
			a=Account.objects.create_user(technologies=request.POST['technologies'],experience=request.POST['experience'],email = request.POST['email'],account_type=request.POST['account_type'], password = request.POST['password'],username=request.POST['username'], phone_number = request.POST['phone_number'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],address=request.POST['address'])
			print a.account_type
			return HttpResponseRedirect('/my_account/')
		else:
			types=dict(account_types)
			print types
			template=loader.get_template('polls/mentorRegisterForm.html')
			context={'types':types.values()}
	
			return HttpResponse(template.render(context,request))
		
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def empRegister(request):
	try:
		if request.method=='POST':
			a=Account.objects.create_user(position=request.POST['position'],organisation=request.POST['organisation'],email = request.POST['email'],account_type=request.POST['account_type'], password = request.POST['password'],username=request.POST['username'], phone_number = request.POST['phone_number'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],address=request.POST['address'],location=request.POST['locations'])
			print "-----------"
			print a.account_type
			return HttpResponseRedirect('/my_account/')
		else:
			states=StatesOfIndia.get_state_names()

			types=dict(account_types)
			print types
			template=loader.get_template('polls/empRegisterForm.html')
			context={'types':types.values(),"states":states}
			return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required		
def userUpdate(request):
	try:
		if request.method=='POST':
			current_user=request.user
			current_user.phone_number=request.POST['Contact_no']
			current_user.address=request.POST['Address']
			current_user.save()
			return HttpResponseRedirect('/my_account/')
		else:
			
			template=loader.get_template('polls/userupdate.html')
			context={}
			return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def mentorUpdate(request):
    try:
        us=get_object_or_404(Account,id=request.user.id)
        if request.method=='POST':
            form=mentorUpdateForm(request.POST,instance=us)
            if form.is_valid():
                
                form.save()
                return HttpResponseRedirect('/my_account/')
        else:
            form=mentorUpdateForm(instance=us)
    except Exception as e:
        return HttpResponse(e)
    context={"form":form}
    return render(request,'polls/mentorUpdateForm.html',context)

@login_required
def empUpdate(request):
    try:
        us=get_object_or_404(Account,id=request.user.id)
        if request.method=='POST':
            form=empUpdateForm(request.POST,instance=us)
            if form.is_valid():
                
                form.save()
                return HttpResponseRedirect('/my_account/')
        else:
            form=empUpdateForm(instance=us)
    except Exception as e:
        return HttpResponse(e)
    context={"form":form}
    return render(request,'polls/empUpdateForm.html',context)

@login_required
def message(request):
	try:

		if request.method == 'POST':
			try:
				#Message.objects.create(sender=request.user,reciever=request.POST['reciever'],message=request.POST['message'])
				Message.objects.create(sender=request.user,reciever=Account.objects.get(email=request.POST['email']),msg_content=request.POST["message"])
				return HttpResponseRedirect("/my_account/")
			except Exception as e:
				template=loader.get_template('polls/error_message.html')
		        context={
		             'error':"Failed To Send Message Please Try Again" 
		        }
		        return HttpResponse(template.render(context,request))
				
		else:

			template=loader.get_template('polls/message.html')
			lst=[]
			for msg in Message.objects.filter(reciever=request.user):
				dic={"sender":msg.sender.username ,"msg_content": msg.msg_content,"msg_id": msg.id,"date":msg.created_at}
				lst.append(dic)
			context={"inmessages":Message.objects.filter(reciever=request.user), "outmessages":Message.objects.filter(sender=request.user),"names":Account.objects.filter(group__name=request.user.group)}
			return HttpResponse(template.render(context,request))
			 # return JsonResponse(context)
	except Exception as e:
		# template=loader.get_template('polls/error_message.html')
		# context={
		# 'error':"Failed To Load Messages Please Try Again"
		# }
		return HttpResponse(e)

@login_required
def message_reply(request,a):
	try:
		if request.method=='POST':
			receiver=Account.objects.get(id=a)
			Message.objects.create(sender=request.user,reciever=Account.objects.get(email=receiver.email),msg_content=request.POST["message"])
			return HttpResponseRedirect('/user_messages/')
		else:
			template=loader.get_template('polls/msg_rply.html')
			context={'a':a}
			return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def message_delete(request,a):
	try:
		message=Message.objects.get(id=a)
		message.delete()
		return HttpResponseRedirect('/user_messages/')
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def user_messages(request):
	try:
		inmessages=Message.objects.filter(sender=request.user)
		outmessages=Message.objects.filter(reciever=request.user)

		template = loader.get_template('polls/user_messages.html')
		context={"inmessages":inmessages,"outmessages":outmessages}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def connect(request):
	try:
		if '_auth_user_id' in request.session:
			user_obj = User.objects.filter(id=request.session['_auth_user_id'])
			request.user = user_obj[0]
			messages.success(request, 'You are now logged in as {}'.format(request.user))
			login(request, request.user, backend=settings.AUTHENTICATION_BACKENDS[0])
		return HttpResponseRedirect('/')
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Login Please Try Again"
		}
		return HttpResponse(template.render(context,request)) 

def edx_auth(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)

				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/")
		else:
			return HttpResponseRedirect("/")
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Authentication Failed Please Try After Some Time" 
		}
		return HttpResponse(template.render(context,request))

@login_required
def courses(request):
	try:
		template=loader.get_template('polls/courses.html')
		all_courses = Courses.objects.all().values("id", "name", "tag_name")
		context = {"all_courses":all_courses, "h11":"h11"}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		
		return HttpResponse("Failed To Load Courses Please Try Again")

@login_required
def course_chapt(request,a):
	try:
		course=Courses.objects.get(id=a)
		try:
			registered = Registered_courses.objects.get(course=course, user=Account.objects.get(email=request.user.email))
		except Registered_courses.DoesNotExist:
			registered = None
		chapters=Chapter.objects.filter(course=course)	
		template=loader.get_template('polls/chapters.html')
		
		context={
		'chapters':chapters,
		'course':course,
		'duration':time.strftime('%H:%M:%S', time.gmtime(course.duration)),
		'registered':registered
		}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))
			#return HttpResponse("Failed To Load Chapters Please Try Again")

@login_required
def course_chapt_ajax(request,a):
	try:
		course=Courses.objects.get(id=a)
		chapters=[{"id":chapter["id"], "text":chapter["name"]} for chapter in Chapter.objects.filter(course=course).values("id", "name")] 	
		return JsonResponse({"chapters":chapters})
	except Exception as e:
			template=loader.get_template('polls/error_message.html')
			context={
			'error':"Failed To Load Topics Please Try Again" 
			}
			return HttpResponse(template.render(context,request))

@login_required
def chapt_topics(request,a):
	try:
		chapter = Chapter.objects.get(id=a)
		topics=chapter.topics_set.all().values("id", "name", "Description", "notes")
	    
		template=loader.get_template('polls/topics.html')
		context={
		'topics':topics,
		}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load Topics Please Try Again" 
		}
		return HttpResponse(template.render(context,request))
@login_required
def topic(request,a):
	topic=Topics.objects.get(id=a)
	pages = [to["id"] for to in topic.chapter.topics_set.all().values("id")]
	if pages.index(int(a)) +1 == len(pages):
		next_page= False
		next_page_num = 0
		previous_page = True
		previous_page_num = pages[pages.index(int(a)) -1]
		Registered_topics.objects.get_or_create(user=Account.objects.get(email=request.user.email),course=topic.chapter.course,chapter=topic.chapter,topic=topic,completed_perc=0,timetaken= 0,completion_status=True)
	elif pages.index(int(a)) == 0:
		previous_page = False
		previous_page_num = pages[pages.index(int(a)) -1]

		next_page = True
		next_page_num = pages[pages.index(int(a))+1]
		Registered_topics.objects.get_or_create(user=Account.objects.get(email=request.user.email),course=topic.chapter.course,chapter=topic.chapter,topic=topic,completed_perc=0,timetaken=0,completion_status=True)
	else:
		previous_page = True
		previous_page_num = pages[pages.index(int(a))-1]
		
		next_page_num = pages[pages.index(int(a))+1]
		next_page = True 
		Registered_topics.objects.get_or_create(user=Account.objects.get(email=request.user.email),course=topic.chapter.course,chapter=topic.chapter,topic=topic,completed_perc=0,timetaken=0,completion_status=True)
	template=loader.get_template('polls/topic.html')
	# ass_qns=Question.objects.order_by('?')[:3]
	course=topic.chapter.course
	chapters=Chapter.objects.filter(course=course)
	topicslist=[]
	for i in chapters:
		topicslist.append({
			str(i):Topics.objects.filter(chapter=i)})
	print topicslist
	fo=open(topic.doc,"r")
	contents=fo.read()
	topi=[top["topic"] for top in request.user.registered_topics_set.all().values("topic")]
	last=[i.topic.name for i in request.user.registered_topics_set.all()]
	context={"t_path": "/topic/"+str(topic.id)+"/", "topic":topic, "current":a, "pages":pages, "previous_page":previous_page, "next_page":next_page,"next_page_num":next_page_num, "previous_page_num":previous_page_num,"contents":contents,"tests":topic.test_set.all(), "assign":topic.chapter.id,'topi':topi,"last":last,"max":last[-1],"topicslist":topicslist}
	return HttpResponse(template.render(context, request))
	
	

@login_required
def test_launch(request,a):
	# try:
	template = loader.get_template('polls/test.html')
	launch_test = Test.objects.get(id=a)
	questions = Question.objects.filter(test_question=launch_test)
	# level_2_questions = Question.objects.filter(level='level-2',test_question=launch_test)
	# level_3_questions = Question.objects.filter(level='level-3',test_question=launch_test)
	
	total_questions = len(launch_test.question_set.all())
	context={"questions":questions,"test":launch_test, "total_questions":total_questions}
	return HttpResponse(template.render(context, request))
	# except Exception as e:
	# 	template=loader.get_template('polls/error_message.html')
	# 	context={
	# 	'error':"Failed To Test Please Try Again " 
	# 	}
	# 	return HttpResponse(template.render(context,request))

@login_required
def assign(request,a):
	try:
		template = loader.get_template('polls/assign.html')
		chap=Chapter.objects.get(id=a)
		tes=Test.objects.filter(test_chap=chap)
		index=randrange(0,2)
		qns=[]
		for i in tes:
			qns.append(i.question_set.all()[index])
		context={"chap":chap,"tes":tes,"qns":qns}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load Assignment Please Try Again" 
		}
		return HttpResponse(template.render(context,request))




@login_required
def test_cal(request):
	# try:
	test_data = dict(request.POST)
	
	total_questions = int(test_data["total_questions"][0]) 
	time_taken = test_data["times"] 
	test_id = test_data["id"]
	print time_taken
	test_data.pop("csrfmiddlewaretoken")
	test_data.pop("times")
	test_data.pop("id")
	test_data.pop("total_questions")
	
	count=0
	
	# ding={}
	# for two in test_data.keys():
	# 	q=Question.objects.get(id=two[0])
	# 	answ=Answer.objects.get(ans_question=q, correct=True)
	# 	ding[two[]]=answ.ans
			
	# 	count+=1
		
	res={}
	counter =0
	# for one in test_data.values():
	# 	ans= Answer.objects.get(id=one[0])
	# 	res[one[0]]=ans.ans
	# 	ding={}
	data = []
	
	for two in test_data:
		ques=Question.objects.get(id=two)
		submitted = Answer.objects.get(id=test_data[two][0])#value of that key 
		correct=Answer.objects.get(ans_question=ques, correct=True)
		dic={
		"question":ques.ques,
		"correct_answer":correct.ans,
		"submitted_answer":submitted.ans,
		"topic":ques.test_question.chapter.name,
		"topic_id":ques.test_question.chapter.id
		}
		data.append(dic)
		if submitted.correct is True:
			counter+=1
	test = Test.objects.get(id=int(test_id[0]))
	print time_taken[0]
	if counter == 0:
		test_sub_data=TestResult.objects.create(test_user = request.user,test_course=test.chapter.course,test_topic=test.topic,test_percent = 0, test_timetaken= float(time_taken[0]), test_test=Test.objects.get(id=int(test_id[0])), ans_records=data)
		print time_taken[0]
	else:
		print time_taken[0]
		
		test_sub_data=TestResult.objects.create(test_user = request.user,test_course=test.chapter.course,test_topic=test.topic,test_percent = (float(counter)/len(total_questions))*100, test_timetaken= float(time_taken[0]), test_test=Test.objects.get(id=int(test_id[0])), ans_records = data)
	print model_to_dict(test_sub_data)
	return redirect('/test_success_page/'+str(test_sub_data.id))
	# template=loader.get_template('polls/success.html')
	# context = {"test_sub_data": model_to_dict(test_sub_data)}
	# return redirect(reverse('success_page') + '?message='+json.dumps(context))
	# except Exception as e:
	# 	template=loader.get_template('polls/error_message.html')
	# 	context={
	# 	'error':e 
	# 	}
	# 	return HttpResponse(template.render(context,request))


@login_required
def timeline(request):
	try:
		template = loader.get_template('polls/timeline.html')
		a = TestResult.objects.filter(test_user = request.user)
		context = {"tests":a}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load Timeline Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def jsfiddle(request):
	try:
		template = loader.get_template('polls/jsfiddle.html')
		context = {}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load Frame Please Try Again " 
		}
		return HttpResponse(template.render(context,request))
@login_required
def logout_view(request):
	try:
		logout(request)
		return HttpResponseRedirect("/")
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load Logout Please Try Again " 
		}
		return HttpResponse(template.render(context,request))
# def topi(request,a):
# 	chapter=Chapter.objects.get(id=a)
# 	topi=chapter.objects.filter(chapter=chapter)
# 	try:
# 		page=request.GET.get('page')
# 		paginator=Paginator(topi,1)
		
# 		topi = paginator.page(page)
# 	except PageNotAnInteger:sss
# 		topi = paginator.page(1)
# 	except EmptyPage:
# 		topi = paginator.page(paginator.num_pages)
def course_chapter_ajax(request,a):
	course=Courses.objects.get(id=a)
	print course
	chapterslist=list(course.chapter_set.all().values("id", "name"))
	print chapterslist
	return JsonResponse({'chapterslist':chapterslist})

@login_required		 	
def upload_file(request):
	try:
		if request.method == 'POST':
			# root_path='/home/sentinal/Downloads/elearning/mysite/polls/static/media/'
			path=MEDIA_ROOT+"/folder/"+str(request.POST['course']) + '/' + str(request.POST['chapt']) + '/' + str(request.POST['topic']) + '/'
			doc_path=path + str(request.FILES['myfile'])
			print doc_path
			video_path=path + str(request.FILES['myfile1']) 

			directory = os.path.dirname(path) 
			if not os.path.exists(directory):
				os.makedirs(directory)
				for f in request.FILES:
					with open(path+str(request.FILES[f]),'wb+') as destination:

						for chunk in (request.FILES[f]).chunks():	
							destination.write(chunk)
				print request.POST['topic']
				a=Topics.objects.create(name=request.POST['topic'],Description='',sl_no=request.POST['sl_no'],notes='',percentage=request.POST['weight'],chapter= Chapter.objects.get(id=request.POST['chapt']),page_content='',video=video_path,doc=doc_path)
				print a
			elif os.path.exists(directory):	
				for f in request.FILES:
					with open(path+str(request.FILES[f]),'wb+') as destination:

						for chunk in (request.FILES[f]).chunks():	
							destination.write(chunk)
				a=Topics.objects.create(name=request.POST['topic'],Description='',sl_no=request.POST['sl_no'],notes='',percentage=request.POST['weight'],chapter= Chapter.objects.get(id=request.POST['chapt']),page_content='',video=video_path,doc=doc_path)
				print a
			return HttpResponse("done")
		else:
			template = loader.get_template('polls/topic_form.html')
			course=Courses.objects.all()
			# chapters=Chapter.objects.all()
			context={'courses':course}
			return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Upload a File Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def add_course(request):
	# try:
	if request.method == 'POST':
		Courses.objects.create(name=request.POST['course'],prerequisites=request.POST['prerequestics'],Description=request.POST['description'],duration=request.POST['duration'], author=request.POST['author'], no_of_chapters=request.POST['chapters'], tag_name=request.POST['name'])
		return HttpResponse("done")
	else:
		template=loader.get_template('polls/course_form.html')
		context={}
		return HttpResponse(template.render(context, request))
	# except Exception as e:
	# 	template=loader.get_template('polls/error_message.html')
	# 	context={
	# 	'error':"Failed To add a course Please Try Again " 
	# 	}
	# 	return HttpResponse(template.render(context,request))



@login_required
def add_chapter(request):
	try:
		if request.method == 'POST':
			cour=Courses.objects.get(id=request.POST['course'])
			Chapter.objects.create(name=request.POST['chapt'],course=cour,Description=request.POST['description'],duration=request.POST['duration'],completed_perc=0,timetaken=0,completion_status=False)
			return HttpResponse("done")
		else:
			course = Courses.objects.all()
			template = loader.get_template('polls/chapter_form.html')
			context={'course':course}
			return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To add a chapter Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def assign_result(request):
	try:
		assign_data = dict(request.POST)
		time_taken = assign_data["times"] 
		assign_id = assign_data["id"]

		assign_data.pop("csrfmiddlewaretoken")
		assign_data.pop("times")
		assign_data.pop("id")
		
		data=[]
		counter =0
		
		for one in assign_data:

			submitted_ans = Answer.objects.get(id=assign_data[one][0])
			ques=Question.objects.get(id=one)
			correct_ans=Answer.objects.get(ans_question=ques,correct=True)
			dic={
				'question':ques.ques,
				'submitted_ans':submitted_ans.ans,
				'correct_ans':correct_ans.ans,
				'topic_id':ques.topic_ques.id,
				'topic':ques.topic_ques.name
			}
			data.append(dic)
			if submitted_ans.correct is True:
				
				counter+=1
		chapter=Chapter.objects.get(id=int(assign_id[0]))
		if counter == 0:
			a=Assignment.objects.create(assign_user = request.user,assign_course=chapter.course,test_test = Chapter.objects.get(id=int(assign_id[0])), assign_percent = 0, assign_timetaken= float(time_taken[0]), ans_records=data)

		else:
			a=Assignment.objects.create(assign_user = request.user,assign_course=chapter.course,test_test = Chapter.objects.get(id=int(assign_id[0])),  assign_percent = (float(counter)/len(assign_data))*100, assign_timetaken= float(time_taken[0]), ans_records = data)
		
		# ------start from here--------
			# if a.assign_percent > 80:
			# 	Registered_chapters.objects.get_or_create(user=Account.objects.get(email = request.user.email),chapter=Chapter.objects.get(id=int(assign_id[0])),timetaken=0,completed_perc=0,completion_status=True)
		
			# if a.test_test.next_chap is not None:
			# 	next_chap=Chapter.objects.get(id=a.test_test.next_chap)
				
			# 	context={"assign":a.ans_records,"topic_id":ques.topic_ques.id,"topic":ques.topic_ques.name,'next_chap':next_chap.name,'id':a.test_test.next_chap, "assign_percent":a.assign_percent, "assign_timetaken":a.assign_timetaken}
			# 	template=loader.get_template('polls/success.html')

			# 	return HttpResponse(template.render(context, request))
				# return redirect(reverse('success_page') + '?message='+json.dumps(context))
		
		context = {"assign":a.ans_records,"topic_id":ques.topic_ques.id,"topic":ques.topic_ques.name, "assign_percent":a.assign_percent, "assign_timetaken":a.assign_timetaken}
		return redirect('/assign_success_page/'+str(a.id))
	# 	template=loader.get_template('polls/success.html')

	# 	return HttpResponse(template.render(context, request))
	# # return redirect(reverse('success_page') + '?message='+json.dumps(context))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e 
		}
		return HttpResponse(template.render(context,request))
		


@login_required
def test_success_page(request,id):
	try:
		test_sub_data=TestResult.objects.get(id=id)
		context={'test_sub_data':test_sub_data}
		template=loader.get_template('polls/success.html')
		return HttpResponse(template.render(context,request))

	# return HttpResponse(template.render(json.loads(request.GET["message"]), request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def assign_success_page(request,id):
	try:
		a=Assignment.objects.get(id=id)
		context={'assign':a.ans_records, "assign_percent":a.assign_percent, "assign_timetaken":a.assign_timetaken}
		template=loader.get_template('polls/success.html')
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def chapt(request,a):
	try:
		chap = Chapter.objects.get(id = a)
		topics = chap.topics_set.all()
		template = loader.get_template('polls/chapt.html')
		context = {'chapt':chap,'topics':topics}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Retrieve Chapters Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def skills_set(request):
	try:
		chapt = request.user.assignment_set.all()
		skills =  filter(None,set([assignment.ans_records[0]["topic"] if assignment.ans_records[0]["submitted_ans"]==assignment.ans_records[0]["correct_ans"] else "" for assignment in chapt]))
		skills1 =  set([assignment.ans_records[0]["topic"] if assignment.ans_records[0]["submitted_ans"]==assignment.ans_records[0]["correct_ans"] else "" for assignment in chapt])
		template = loader.get_template('polls/skills.html')
		context = {'skills':skills}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load Skills Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def cart(request):
	cart_items = Cart.objects.filter(user=Account.objects.get(email = request.user.email))
	try:
		template = loader.get_template('polls/cart.html')
		context = {"cart_items":cart_items, "ssh_key":Ssh.objects.get(user=request.user)}
		return HttpResponse(template.render(context,request))
	except Ssh.DoesNotExist:
		template=loader.get_template('polls/cart.html')
		context={"cart_items":cart_items}
		return HttpResponse(template.render(context,request))


@login_required
def cart_checkout(request, id):

	item = Cart.objects.get(id = id)
	
	Registered_courses.objects.get_or_create(course = item.course, user=Account.objects.get(email = request.user.email), timetaken=0, completed_perc=0, completion_status=False)
	item.delete()

	# droplet=digitalocean.Droplet(token="9d38cc1038ea74a63db1c3079fd792236110ed96d965886803c08ff0b85af222",name=str(item.course),private_networking="true",region="nyc3",size="512mb",image="ubuntu-14-04-x64",ssh_keys=[Ssh.objects.get(user=request.user).key])
	# droplet.create()
	return HttpResponseRedirect('/')

@login_required
def userSSH(request):
	try:
	    if request.method=='POST':
	    	
	    	Ssh.objects.create(user=request.user,key=request.POST['ssh_key'])
	    	return HttpResponseRedirect("/cart/")
	    else:

	    	template=loader.get_template('polls/ssh_key.html')
	    	context={}
	    	return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def cart_item_delete(request,id):
	try:
		item = Cart.objects.get(id = id)
		item.delete()
		return HttpResponseRedirect("/cart")
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To delete item Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def add_to_cart(request,id):
	try:
		item = Courses.objects.get(id=id)
		Cart.objects.get_or_create(course = item, user=Account.objects.get(email = request.user.email))
		return HttpResponseRedirect("/cart")
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To add item Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def group(request):
	data={"python":[[22,23,24,25,26]],'django':[[27,28,29,30,31]]}
	for key in data:
		for nestedlist in data[key]:
			grp=Group.objects.create(name=str(key)+str(randint(100000,1000000)),course=Courses.objects.get(name=key))
			for listelement in nestedlist:
				you=Account.objects.get(id=listelement)
				you.group=grp
				you.save()
	return HttpResponse('done')

@login_required
def test_creation(request):
	try:
		if request.method=='POST':
			test=Test.objects.create(name=request.POST['test'],test_chap=Chapter.objects.get(id=request.POST['chapter']),test_chapter=Topics.objects.get(id=request.POST['topic']))
			return redirect('/test_ques/'+str(test.id)) 
		else:
			template=loader.get_template('polls/test_creation_form.html')
	    	courses=Courses.objects.all()
	    	context={'courses':courses}
	    	return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To add item Please Try Again " 
		}
		return HttpResponse(template.render(context,request))	

@login_required
def chapt_topic_ajax(request,a):
	course=Courses.objects.get(id=a)
	chapters=list(course.chapter_set.all())
	chapterslist=list(course.chapter_set.all().values("id", "name"))
	print chapterslist
	topicslist={}
	for i in chapters:
			topicslist[i.id]=list(i.topics_set.all().values("id", "name"))
	print topicslist
	return JsonResponse({'topicslist':topicslist,'chapterslist':chapterslist})

@login_required
def test_ques(request,a):
	# try:
	if request.method=='POST':
		test_id=request.POST['test_id']
		print test_id
		test=Test.objects.get(id=request.POST['test_id'])

		ques=Question.objects.create(test_question=test,ques=request.POST['question'],topic_ques=test.test_chapter)
		ans1=Answer.objects.create(ans=request.POST['answer1'],ans_question=ques,correct=request.POST.get("checkbox1", False))
		ans2=Answer.objects.create(ans=request.POST['answer2'],ans_question=ques,correct=request.POST.get("checkbox2", False))
		ans3=Answer.objects.create(ans=request.POST['answer3'],ans_question=ques,correct=request.POST.get("checkbox3", False))
		ans4=Answer.objects.create(ans=request.POST['answer4'],ans_question=ques,correct=request.POST.get("checkbox4", False))
		return HttpResponseRedirect('/test_ques/'+str(test.id))
		
	else:
		template=loader.get_template('polls/test_ques_form.html')
		context={'test_id':a}
		return HttpResponse(template.render(context,request))
	# except Exception as e:
	# 	template=loader.get_template('polls/error_message.html')
	# 	context={
	# 	'error':e
	# 	}
	# 	return HttpResponse(template.render(context,request))

@login_required
def create_project(request):
	try:
		if request.method=='POST':
			Project.objects.create(name="project",course=Courses.objects.get(id=request.POST['course']),duration=request.POST['duration'],price=request.POST['price'],technologies=request.POST['technologies'])
			return HttpResponse('DONE')
		else:
			context={'courses':Courses.objects.all()}
			template=loader.get_template('polls/project_create.html')
			return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))


def course_project_ajax(request,a):
	course=Courses.objects.get(id=a)
	print course
	projectslist=list(course.project_set.all().values("id", "name"))
	
	return JsonResponse({'projectslist':projectslist})

@login_required
def create_project_chapter(request):
	try:
		if request.method == 'POST':
			path=MEDIA_ROOT+"/project/"+str(request.POST['course']) + '/' + str(request.POST['project']) + '/' + str(request.POST['chapter']) + '/'
			doc_path=path + str(request.FILES['myfile'])
			directory = os.path.dirname(path) 
			if not os.path.exists(directory):
				os.makedirs(directory)
				for f in request.FILES:
					with open(path+str(request.FILES[f]),'wb+') as destination:

						for chunk in (request.FILES[f]).chunks():	
							destination.write(chunk)
				
				a=project_chapters.objects.create(name=request.POST['chapter'],course=Courses.objects.get(id=request.POST['course']),Project=Project.objects.get(id=request.POST['project']),tags=request.POST['tags'],file=doc_path)
				print a
			elif os.path.exists(directory):	
				for f in request.FILES:
					with open(path+str(request.FILES[f]),'wb+') as destination:

						for chunk in (request.FILES[f]).chunks():	
							destination.write(chunk)
				a=project_chapters.objects.create(name=request.POST['chapter'],course=Courses.objects.get(id=request.POST['course']),Project=Project.objects.get(id=request.POST['project']),tags=request.POST['tags'],file=doc_path)
				print a
			return HttpResponse("done")
		else:
			template = loader.get_template('polls/project_chapters_create.html')
			course=Courses.objects.all()
			
			context={'courses':course}
			return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def assignment_create(request):
	try:
		if request.method=='POST':
			Assignment_create.objects.create(course=Courses.objects.get(id=request.POST['course']),chapter=Chapter.objects.get(id=request.POST['chapt']),question=request.POST['question'],snippet=request.POST['code'],topic_tag=request.POST['topic_tag'],steps=request.POST['steps'],keywords=request.POST['keywords'],input_list=request.POST['input_list'],output_list=request.POST['output_list'])
			return HttpResponse("ding")
		else:
			template = loader.get_template('polls/assignment_create_form.html')
			course=Courses.objects.all()
			
			context={'courses':course}
			return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))		

@login_required
def assignment_display(request,a):
	try:
		chap=Chapter.objects.get(id=a)
		assignment=chap.assignment_create_set.all()
		for i in assignment:
			print i.input_list[0]
		template = loader.get_template('polls/assignment_display.html')
		context={'assignment':assignment,'chap':chap}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))	

	
	#=======================================employer related====================================
@login_required
def empRegister(request):
	try:
		if request.method=='POST':
			a=Account.objects.create_user(position=request.POST['position'],organisation=request.POST['organisation'],email = request.POST['email'],account_type=request.POST['account_type'], password = request.POST['password'],username=request.POST['username'], phone_number = request.POST['phone_number'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],address=request.POST['address'],location=request.POST['locations'])
			print "-----------"
			print a.account_type
			return HttpResponseRedirect('/my_account/')
		else:
			states=StatesOfIndia.get_state_names()

			types=dict(account_types)
			print types
			template=loader.get_template('polls/empRegisterForm.html')
			context={'types':types.values(),"states":states}
			return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def empUpdate(request):
    try:
        us=get_object_or_404(Account,id=request.user.id)
        if request.method=='POST':
            form=empUpdateForm(request.POST,instance=us)
            if form.is_valid():
                
                form.save()
                return HttpResponseRedirect('/my_account/')
        else:
            form=empUpdateForm(instance=us)
    except Exception as e:
        return HttpResponse(e)
    context={"form":form}
    return render(request,'polls/empUpdateForm.html',context)

@login_required
def course_nav_bar(request):
	try:
		courses=Courses.objects.all()
		context={'courses':courses}
		template = loader.get_template('polls/main.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def students_display(request,a):
	try:
		l=Registered_courses.objects.filter(course=Courses.objects.get(id=a))

		template = loader.get_template('polls/students_display.html')
		context={'l':l}
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def student_resume(request,a):
	try:
		student=Account.objects.get(id=a)
		res=Registered_courses.objects.filter(user=student)
		#==================assessments and assignments list======================

		data=[]
		for i in res:
			data.append({
				str(i.course.name):
					{
					"assessments":[

						{"test":j.test_test,
						"topic":j.test_topic,
						"percentage":j.test_percent,
						"timetaken":j.test_timetaken,
						"test_time":j.test_time }

						for j in TestResult.objects.filter(test_user=student,test_course=i.course)
					
					],
					"total_tests":len(set(TestResult.objects.filter(test_user=student,test_course=i.course).values_list('test_test',flat=True))),
					"attempted_tests":len(TestResult.objects.filter(test_user=student,test_course=i.course).values('test_test')),
					
					"with_repetition_test_score":(sum(TestResult.objects.filter(test_user=student,test_course=i.course).values_list('test_percent',flat=True))/len(TestResult.objects.filter(test_user=student,test_course=i.course).values_list('test_percent',flat=True))),
					"assignments":[

						{"chapter":k.test_test,
						"percentage":k.assign_percent,
						"timetaken":k.assign_timetaken,
						"assignment_time":k.assign_time}

					  for k in Assignment.objects.filter(assign_user=student, assign_course=i.course)
					],
					"total_assignments":len(set(Assignment.objects.filter(assign_user=student, assign_course=i.course).values_list('test_test',flat=True))),
					"attempted_assignments":len(Assignment.objects.filter(assign_user=student, assign_course=i.course).values_list('test_test',flat=True)),
					"with_repetition_assi_score":(sum(Assignment.objects.filter(assign_user=student, assign_course=i.course).values_list('assign_percent',flat=True))/len(Assignment.objects.filter(assign_user=student, assign_course=i.course).values_list('assign_percent',flat=True))),	
					"course":i.course.id
						}
					
				})
		print data
		shortlisted=shortlist.objects.filter(student=student)
		print shortlisted
		context={'data':data,"student":student,"shortlisted":shortlisted}
		template = loader.get_template('polls/student_resume.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

@login_required
def course_report(request,a):
	try:
		template = loader.get_template('polls/courses_report.html')
		context = {'course':Courses.objects.get(id=a)}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To course report Please Try Again " 
		}
		return HttpResponse(template.render(context,request))
	
@login_required
def user_report(request ,a):
	try:
		report_chapter = Chapter.objects.get(id=a)
		print report_chapter.assignment_set.all()
		b = report_chapter.topics_set.all()
		data = []
		for topic in b:
			dic={
				"topic":topic.name,
				"data":topic.testresult_set.all()
			}
			data.append(dic)
		template = loader.get_template('polls/report.html')
		context = {'data':data,'assigns':report_chapter.assignment_set.all(), "chapter":report_chapter}
		return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load User report Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def employer_task_create(request,a):
	try:
		if request.method=='POST':
			student=Account.objects.get(id=a)
			employer_task.objects.create(course=Courses.objects.get(id=request.POST['course']),snippet=request.POST['code'],student=student,employer=request.user)
			return HttpResponseRedirect('/students_display/')
		else:
			courses=Courses.objects.all()
			template = loader.get_template('polls/employer_task.html')
			context = {'courses':courses,'a':a}
			return HttpResponse(template.render(context,request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load User report Please Try Again " 
		}
		return HttpResponse(template.render(context,request))

@login_required
def shortlist_students(request,a,b):
	try:
		shortlisted_students=shortlist.objects.get_or_create(course=Courses.objects.get(id=b),student=Account.objects.get(id=a),employer=Account.objects.get(id=request.user.id))
		total=shortlist.objects.filter(employer=request.user)
		context={'total':total,"shortlisted_students":shortlisted_students}
		template = loader.get_template('polls/shortlisted_students.html')
		return HttpResponse(template.render(context, request))
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To Load User report Please Try Again " 
		}
		return HttpResponse(template.render(context,request))
