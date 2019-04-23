import uuid
from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin
import jsonfield
from django.utils import timezone
from polls.choices import * 
from polls.models import *
from polls.models import Courses
from django.core.validators import URLValidator

account_types=(('Employer','Employer'),('mentor','mentor'))

class Project(models.Model):
    name = models.CharField(max_length=150)
    Description=models.TextField(max_length=1000)
    duration=models.FloatField()
    author=models.CharField(max_length=150)
    prerequisites=models.TextField(max_length=1000)
    no_of_milestones=models.IntegerField()
    tag_name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_demo=models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Tagging(models.Model):
    tag_name=models.CharField(max_length=200,blank=True,null=True)
    course=models.ForeignKey(Courses,blank=True,null=True)
    file=models.CharField(max_length=200,blank=True,null=True)
    def __unicode__(self):
        return self.tag_name

class Milestone(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name=models.CharField(max_length=150)
    project=models.ForeignKey(Project,blank=True,null=True)
    next_chap=models.IntegerField(blank=True,null=True)
    Description=models.TextField(max_length=1000)
    doc = models.CharField(max_length=200, blank=True, null=True)
    page_content = models.CharField(max_length=200, blank=True, null=True)
    tag_name=models.ManyToManyField(Tagging)
    duration=models.FloatField()
    completed_perc=models.FloatField()
    timetaken=models.FloatField()
    completion_status=models.BooleanField()
    url=models.URLField(max_length=200, blank=True,null=True)
    def __unicode__(self):
        return self.name


    

class ProjectTest(models.Model):
    name = models.CharField(max_length=100)
    test_chap=models.ForeignKey(Milestone,blank=True, null=True)
    def __unicode__(self):
        return self.name

class ProjectQuestion(models.Model):
    ques = models.CharField(max_length=300)
    test_question = models.ForeignKey(ProjectTest,blank=True, null=True)
    def __unicode__(self):
        return self.ques
        
class ProjectAnswer(models.Model):
    ans = models.CharField(max_length=200)
    ans_question = models.ForeignKey(ProjectQuestion)
    correct=models.BooleanField(default=False)
    wrong=models.BooleanField(default=False)
    def __unicode__(self):
        return self.ans

class ProjectTestResult(models.Model):
    test_user=models.ForeignKey(Account, blank=True, null=True)
    test_test = models.ForeignKey(ProjectTest, blank=True, null=True)
    ans_records = jsonfield.JSONField()
    test_percent = models.FloatField()
    test_timetaken = models.FloatField()
    test_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __unicode__(self):
        return str(self.test_user.username + " , "+str(self.test_percent))

class ProjectAssignment(models.Model):
    assign_user=models.ForeignKey(Account,blank=True, null=True)
    test_test = models.ForeignKey(Milestone, blank=True, null=True)
    ans_records = jsonfield.JSONField(max_length=200,blank=True,null=True)
    assign_percent = models.FloatField(blank=True,null=True)
    assign_timetaken = models.FloatField(blank=True,null=True)
    assign_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __unicode__(self):
        return str(self.assign_user.username + " , "+str(self.assign_percent))

        
class RegisteredMilestone(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True)
    chapter=models.ForeignKey(Milestone)
    timetaken=models.FloatField()
    completed_perc=models.FloatField()
    completion_status=models.BooleanField()
    def __unicode__(self):
        return (self.chapter.name + ", " + self.user.username)

class ProjCart(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True)
    project=models.ForeignKey(Project)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __unicode__(self):
        return (self.project.name + ", " + self.user.username)

class RegisteredProject(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True)
    project=models.ForeignKey(Project)
    timetaken=models.FloatField()
    completed_perc=models.FloatField()
    completion_status=models.BooleanField() 
    def __unicode__(self):
        return (self.project.name + ", " + self.user.username)