from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django_project.settings import STATIC_ROOT, MEDIA_ROOT
import os, sys
from django.forms.models import model_to_dict
from polls.models import *
from .models import *


def projects(request):
	context={"projects":Project.objects.filter(is_demo=True)}
	template = loader.get_template('projects/projects.html')
	return HttpResponse(template.render(context, request))
	

def project(request,a):
	context = {"project":Project.objects.get(id=a)}
	template = loader.get_template('projects/projectDetails.html')
	return HttpResponse(template.render(context, request))

def project_register(request):
	projects=Project.objects.filter(is_demo=False)
	context={"projects":projects}
	template = loader.get_template('projects/project_register.html')
	return HttpResponse(template.render(context, request))

def project_milestones(request,a):
	context = {"project":Project.objects.get(id=a)}
	template = loader.get_template('projects/project_milestones.html')
	return HttpResponse(template.render(context, request))

def upload_milestone(request):
	# try:
	if request.method == 'POST':
		# path=MEDIA_ROOT+"/project_folder/"+str(request.POST['project']) + '/' + str(request.POST['milestone']) + '/' 
		# doc_path=path + str(request.FILES['myfile'])
		# print doc_path
		
		# directory = os.path.dirname(path) 
		# if not os.path.exists(directory):
		# 	os.makedirs(directory)
		# 	for f in request.FILES:
		# 		with open(path+str(request.FILES[f]),'wb+') as destination:

		# 			for chunk in (request.FILES[f]).chunks():	
		# 				destination.write(chunk)
		a=Milestone.objects.create(next_chap=request.POST['next_chap'],completion_status=False,completed_perc=0,timetaken=0,duration=request.POST['duration'],name=request.POST['milestone'],Description=request.POST['description'],sl_no=request.POST['sl_no'],project= Project.objects.get(id=request.POST['project']),page_content=request.POST['page_content'],doc="")
		a.tag_name=Tagging.objects.filter(id__in=request.POST.getlist('tag_name'))
		a.save()
		print a
		# elif os.path.exists(directory):	
		# 	for f in request.FILES:
		# 		with open(path+str(request.FILES[f]),'wb+') as destination:

		# 			for chunk in (request.FILES[f]).chunks():	
		# 				destination.write(chunk)
		# 	a=Milestone.objects.create(tag_name=Tagging.objects.filter(id__in=request.POST.getlist('tag_name')),next_chap=request.POST['next_chap'],completion_status=False,completed_perc=0,timetaken=0,duration=request.POST['duration'],name=request.POST['milestone'],Description=request.POST['description'],sl_no=request.POST['sl_no'],project= Project.objects.get(id=request.POST['project']),page_content=request.POST['page_content'],doc=doc_path)
		return HttpResponse("done")
	else:
		template = loader.get_template('projects/upload_milestone.html')
		
		context={'projects':Project.objects.all(),"tags":Tagging.objects.all()}
		return HttpResponse(template.render(context, request))
	# except Exception as e:
	# 	template=loader.get_template('polls/error_message.html')
	# 	context={
	# 	'error':"Failed To Upload a File Please Try Again " 
	# 	}
		# return HttpResponse(template.render(context,request))

	
def milestone(request,a):
	milestone=Milestone.objects.get(id=a)
	pages = [to["id"] for to in milestone.project.milestone_set.all().values("id")]
	if pages.index(int(a)) +1 == len(pages):
		next_page= False
		next_page_num = 0
		previous_page = True
		previous_page_num = pages[pages.index(int(a)) -1]
	elif pages.index(int(a)) == 0:
		previous_page = False
		previous_page_num = pages[pages.index(int(a)) -1]

		next_page = True
		next_page_num = pages[pages.index(int(a))+1]
	else:
		previous_page = True
		previous_page_num = pages[pages.index(int(a))-1]
		
		next_page_num = pages[pages.index(int(a))+1]
		next_page = True 
	template=loader.get_template('projects/milestone.html')
	fo=open(milestone.doc,"r")
	contents=fo.read()
	
	context={ "milestone":milestone, "current":a, "pages":pages, "previous_page":previous_page, "next_page":next_page,"next_page_num":next_page_num, "previous_page_num":previous_page_num,"contents":contents,"tests":milestone.projecttest_set.all()}
	return HttpResponse(template.render(context, request))

def tag_content(request,a):
	tag=Tagging.objects.get(id=a)
	template=loader.get_template('projects/tag_content.html')
	f=open(tag.file,'r')
	content=f.read()
	context={'content':content}
	return HttpResponse(template.render(context, request))


def project_test_launch(request,a):
	
	template = loader.get_template('projects/project_test_launch.html')
	launch_test = ProjectTest.objects.get(id=a)
	test_qestions = launch_test.projectquestion_set.all()
	total_questions = len(launch_test.projectquestion_set.all())
	context={"questions":test_qestions, "test":launch_test, "total_questions":total_questions}
	return HttpResponse(template.render(context, request))
	# except Exception as e:
	# 	template=loader.get_template('polls/error_message.html')
	# 	context={
	# 	'error':"Failed To Test Please Try Again " 
	# 	}
	# 	return HttpResponse(template.render(context,request))
def project_testcal(request):
	# try:
	test_data = dict(request.POST)
	print test_data
	total_questions = int(test_data["total_questions"][0]) 
	time_taken = test_data["times"] 
	test_id = test_data["id"]

	test_data.pop("csrfmiddlewaretoken")
	test_data.pop("times")
	test_data.pop("id")
	test_data.pop("total_questions")
	print test_data
	count=0
	res={}
	counter =0
	data = []
	for two in test_data:
		ques=ProjectQuestion.objects.get(id=two)
		submitted = ProjectAnswer.objects.get(id=test_data[two][0])#value of that key 
		correct=ProjectAnswer.objects.get(ans_question=ques, correct=True)
		dic={
		"question":ques.ques,
		"correct_answer":correct.ans,
		"submitted_answer":submitted.ans,
		"topic":ques.test_question.test_chap.name,
		"topic_id":ques.test_question.test_chap.id
		}
		data.append(dic)
		if submitted.correct is True:
			counter+=1
	test = ProjectTest.objects.get(id=int(test_id[0]))
	if counter == 0:
		test_sub_data=ProjectTestResult.objects.create(test_user = request.user,test_percent = 0, test_timetaken= float(time_taken[0]), test_test=ProjectTest.objects.get(id=int(test_id[0])), ans_records=data)
		print time_taken[0]
	else:
		print time_taken[0]
		test_sub_data=ProjectTestResult.objects.create(test_user = request.user,test_percent = (float(counter)/total_questions)*100, test_timetaken= float(time_taken[0]), test_test=ProjectTest.objects.get(id=int(test_id[0])), ans_records = data)
	print model_to_dict(test_sub_data)
	return redirect('/project_test_success_page/'+str(test_sub_data.id))

def project_test_success_page(request,a):
	try:
		test_sub_data=ProjectTestResult.objects.get(id=a)
		context={'test_sub_data':test_sub_data}
		template=loader.get_template('projects/test_result.html')
		return HttpResponse(template.render(context,request))

	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':e
		}
		return HttpResponse(template.render(context,request))

def tag_file_upload(request):
	if request.method == 'POST':
		path=MEDIA_ROOT+"/tags_folder/"+str(request.POST['course_name']) + '/' + str(request.POST['tag_name']) + '/' 
		doc_path=path + str(request.FILES['myfile'])
		print doc_path
		
		directory = os.path.dirname(path) 
		if not os.path.exists(directory):
			os.makedirs(directory)
			for f in request.FILES:
				with open(path+str(request.FILES[f]),'wb+') as destination:

					for chunk in (request.FILES[f]).chunks():	
						destination.write(chunk)
			
			a=Tagging.objects.create(tag_name=request.POST['tag_name'],course=Courses.objects.get(id=request.POST['course_name']),file=doc_path)
			print a
		elif os.path.exists(directory):	
			for f in request.FILES:
				with open(path+str(request.FILES[f]),'wb+') as destination:

					for chunk in (request.FILES[f]).chunks():	
						destination.write(chunk)
			a=Tagging.objects.create(tag_name=request.POST['tag_name'],course=Courses.objects.get(id=request.POST['course_name']),file=doc_path)
			print a
		return HttpResponse("done")
	else:
		template = loader.get_template('projects/tag_upload.html')
		
		context={'courses':Courses.objects.all()}
		return HttpResponse(template.render(context, request))

#----------------------------------------------
def add_proj_cart(request,a):
	# try:
	item = Project.objects.get(id=a)
	print request.user.email
	ProjCart.objects.get_or_create(project = item, user=Account.objects.get(email = request.user.email))
	return HttpResponseRedirect("/ProjectCart")
	# except Exception as e:
	# 	template=loader.get_template('polls/error_message.html')
	# 	context={
	# 	'error':"Failed To add item Please Try Again " 
	# 	}
	# 	return HttpResponse(template.render(context,request))

def ProjectCart(request):
	cart_items = ProjCart.objects.filter(user=Account.objects.get(email = request.user.email))
	try:
		template = loader.get_template('projects/project_cart.html')
		context = {"cart_items":cart_items}
		return HttpResponse(template.render(context,request))
	except Ssh.DoesNotExist:
		template=loader.get_template('projects/project_cart.html')
		context={"cart_items":cart_items}
		return HttpResponse(template.render(context,request))

def project_cart_checkout(request, a):
	item=ProjCart.objects.get(id=a)
	RegisteredProject.objects.get_or_create(project = item.project, user=Account.objects.get(email = request.user.email), timetaken=0, completed_perc=0, completion_status=False)
	item.delete()
	# droplet=digitalocean.Droplet(token="9d38cc1038ea74a63db1c3079fd792236110ed96d965886803c08ff0b85af222",name=str(item.course),private_networking="true",region="nyc3",size="512mb",image="ubuntu-14-04-x64",ssh_keys=[Ssh.objects.get(user=request.user).key])
	# droplet.create()
	return HttpResponseRedirect('/')

def project_cart_item_delete(request,id):
	try:
		item = ProjCart.objects.get(id = id)
		item.delete()
		return HttpResponseRedirect("/project_cart")
	except Exception as e:
		template=loader.get_template('polls/error_message.html')
		context={
		'error':"Failed To delete item Please Try Again " 
		}
		return HttpResponse(template.render(context,request))