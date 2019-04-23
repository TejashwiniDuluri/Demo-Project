import uuid
from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin
import jsonfield
from django.utils import timezone
from polls.choices import * 
from django.contrib.postgres.fields import ArrayField
from polls.choices import StatesOfIndia
account_types=(('Employer','Employer'),('mentor','mentor'))

class Courses(models.Model):
    name = models.CharField(max_length=200)
    Description=models.TextField(max_length=1000)
    duration=models.FloatField()
    author=models.CharField(max_length=200)
    prerequisites=models.TextField(max_length=1000)
    no_of_chapters=models.IntegerField()
    tag_name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __unicode__(self):
        return self.name
    @property
    def sorted_attendee_set(self):
        return self.attendee_set.order_by('last_name')

class Group(models.Model):
    name=models.CharField(max_length=200)
    course=models.ForeignKey(Courses,blank=True,null=True) 
    def __unicode__(self):
        return self.name

class User(models.Model):
    def create_user(
            self,
            username,
            email,
            occupation,
            location,
            first_name,
            address,
            phone_number,
            account_type,
            password,
            is_mentor,
           
            **kwargs
    ):
        msg = 'Account must have a valid %s.'
        if not email:
             raise ValueError(msg % 'email address')
        
        
        account = self.model(
            username=username,
            email=email,
            occupation=occupation,
            location=location,
            first_name=first_name,
            address=address,
            phone_number=phone_number,
            password=password,
            is_mentor=is_mentor,
            account_type=account_type,

        )
        account.set_password(password)
        account.save(using=self._db)
        return account
    
    def create_superuser(
            self,
            username,
            email,
            occupation,
            location,
            first_name,
            address,
            phone_number,
            password,
            is_mentor,
            **kwargs):
        account = self.create_user(
        username,   
        email,
        occupation,
        location,
        first_name,
        address,
        phone_number,
        password,
        is_mentor,
        
            
        )
        account.is_admin =True
        account.is_superuser = True
        account.is_staff = True
        account.save(using=self._db)

        return account
class Account(AbstractBaseUser,PermissionsMixin):
    # TODO: Add created_at and modified_at fields for this model.
    username = models.CharField(max_length=40,unique=True,blank=True,null=True)
    first_name = models.CharField(max_length=40,blank=True,null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    address = models.CharField(max_length=350,blank=True,null=True)
    phone_number = models.CharField(
            max_length=10,
            unique=True,
            blank=True,null=True,
            help_text="Enter the phone number WITHOUT country code"
        )
    account_types=(('Employer','Employer'),('mentor','mentor'))
    account_type = models.CharField(max_length=30,choices=account_types,null=True, blank=True)
        
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    is_staff = models.BooleanField(default=False)
    occupation = models.IntegerField(choices=OCCUPATION_CHOICES, default=1)
    location = models.CharField(
            max_length=50,null=True,blank=True)
            
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default = True)
    group=models.ForeignKey(Group,null=True,blank=True)
    #mentor
    technologies=models.CharField(max_length=100,blank=True,null=True)
    experience=models.CharField(max_length=100,blank=True,null=True)
    #employer
    organisation=models.CharField(max_length=100,blank=True,null=True)
    position=models.CharField(max_length=100,blank=True,null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        
            'occupation',
            'location',
            'first_name',
            'address',
            'username'
    ]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __unicode__(self):
        return '{0} ({1})'.format(self.first_name, self.phone_number)

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def set_email(self, email):
        self.email = email

    def set_phone_number(self,phone_number):
        self.phone_number=phone_number

# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'documents/{0}/{1}'.format(instance.user.username, filename)
# class Document(models.Model):
#     user=models.ForeignKey(Account, blank=True, null=True)
#     description = models.CharField(max_length=255, blank=True)
#     document = models.FileField(upload_to=user_directory_path)
#     uploaded_at = models.DateTimeField(auto_now_add=True)  




class Image(models.Model):
    account_image = models.ForeignKey(Account)
    image = models.ImageField(upload_to='image',verbose_name='image',)  
class Message(models.Model):
     
     sender = models.ForeignKey(Account,related_name='sender')
     reciever = models.ForeignKey(Account,related_name='reciever')
     msg_content = models.TextField(max_length=1000)
     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
     is_read=models.BooleanField(default=False)
     
     def __unicode__(self):
        return self.reciever.username
    
     class Meta:
        ordering = ['-created_at']

        
class Chapter(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name=models.CharField(max_length=200)
    course=models.ForeignKey(Courses,blank=True,null=True)
    next_chap=models.IntegerField(blank=True,null=True)
    Description=models.TextField(max_length=1000)
    duration=models.FloatField()
    completed_perc=models.FloatField()
    timetaken=models.FloatField()
    completion_status=models.BooleanField()
    def __unicode__(self):
        return self.name

class Topics(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name=models.CharField(max_length=100)
    percentage=models.FloatField()
    Description=models.TextField(max_length=1000, blank=True, null=True)
    chapter=models.ForeignKey(Chapter)
    notes=models.TextField(max_length=1000, blank=True, null=True)
    page_content = models.CharField(max_length=200)
    video = models.CharField(max_length=200, blank=True, null=True)
    doc = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
        return self.name  
    @property
    def sorted_attendee_set(self):
        return self.attendee_set.order_by('last_name')
class Registered_courses(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True)
    course=models.ForeignKey(Courses)
    timetaken=models.FloatField()
    completed_perc=models.FloatField()
    completion_status=models.BooleanField() 
    def __unicode__(self):
        return (self.course.name + ", " + self.user.username)
    

class Course_chapter(models.Model):
    registered_course=models.ForeignKey(Registered_courses,blank=True,null=True)
    timetaken=models.FloatField()
    completed_perc=models.FloatField()
    completion_status=models.BooleanField()
    def __unicode__(self):
        return (self.registered_course.course.name)
    
class Chapter_topic(models.Model):
    name = models.CharField(max_length=100)
    course_chap=models.ForeignKey(Course_chapter)
    timetaken=models.FloatField()
    media_video = models.CharField(max_length=200, blank=True, null=True)
    media_pdf = models.CharField(max_length=200, blank=True, null=True)
    completion_status=models.BooleanField()
    def __unicode__(self):
        return (self.name + ", "+ self.course_chap.registered_course.course.name)

class Test(models.Model):
    sl_no = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topics,blank=True, null=True)
    chapter=models.ForeignKey(Chapter,blank=True, null=True)
    def __unicode__(self):
        return ("Take a test on" +" "+ self.name)

class Question(models.Model):
    ques = models.TextField(max_length=300)
    test_question = models.ForeignKey(Test,blank=True, null=True)
    topic_ques = models.ForeignKey(Topics)
    def __unicode__(self):
        return self.ques
        
class Answer(models.Model):
    ans = models.CharField(max_length=200)
    ans_question = models.ForeignKey(Question)
    correct=models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.ans

class TestResult(models.Model):
    test_user=models.ForeignKey(Account, blank=True, null=True)
    test_test = models.ForeignKey(Test, blank=True, null=True)
    test_topic = models.ForeignKey(Topics, blank=True, null=True)
    test_course=models.ForeignKey(Courses, blank=True, null=True)
    ans_records = jsonfield.JSONField()
    test_percent = models.FloatField()
    test_timetaken = models.FloatField()
    test_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __unicode__(self):
        return str(self.test_user.username + " , "+str(self.test_percent))

class Assignment(models.Model):
    assign_user=models.ForeignKey(Account,blank=True, null=True)
    assign_course=models.ForeignKey(Courses,blank=True, null=True)
    test_test = models.ForeignKey(Chapter, blank=True, null=True)
    ans_records = jsonfield.JSONField(max_length=200,blank=True,null=True)
    assign_percent = models.FloatField(blank=True,null=True)
    assign_timetaken = models.FloatField(blank=True,null=True)
    assign_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __unicode__(self):
        return str(self.assign_user.username + " , "+str(self.assign_percent))

class Cart(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True)
    course=models.ForeignKey(Courses)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __unicode__(self):
        return (self.course.name + ", " + self.user.username)
        
class Registered_chapters(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True)
    chapter=models.ForeignKey(Chapter)
    timetaken=models.FloatField()
    completed_perc=models.FloatField()
    completion_status=models.BooleanField()
    def __unicode__(self):
        return (self.chapter.name + ", " + self.user.username)

class Registered_topics(models.Model):
    user=models.ForeignKey(Account, blank=True, null=True)
    course=models.ForeignKey(Courses,blank=True, null=True)
    topic=models.ForeignKey(Topics)
    chapter=models.ForeignKey(Chapter,blank=True, null=True)
    timetaken=models.FloatField()
   
    completed_perc=models.FloatField()
    completion_status=models.BooleanField() 
    def __unicode__(self):
        return (self.topic.name + ", " + self.user.username)

class Ssh(models.Model):
    user=models.ForeignKey(Account,blank=True, null=True)
    key=models.TextField(max_length=1000)
    def __unicode__(self):
        return unicode(self.user)
# class Project(models.Model):
#     name=models.CharField(max_length=200,blank=True,null=True)
#     course=models.ForeignKey(Courses,blank=True, null=True)
#     duration=models.FloatField()
#     price=models.FloatField()
#     technologies=models.TextField(max_length=200,blank=True,null=True)
#     def __unicode__(self):
#         return unicode(self.name)

# class project_chapters(models.Model):
#     name=models.CharField(max_length=200,blank=True,null=True)
#     course=models.ForeignKey(Courses,blank=True, null=True)

#     Project=models.ForeignKey(Project,blank=True, null=True)
#     tags=models.TextField(max_length=200,blank=True,null=True)
#     file=models.FileField()
#     def __unicode__(self):
#         return unicode(self.name)

class Assignment_create(models.Model):
    course=models.ForeignKey(Courses,blank=True, null=True)
    chapter=models.ForeignKey(Chapter,blank=True, null=True)
    snippet=models.TextField(max_length=800,blank=True,null=True)
    topic_tag=models.TextField(max_length=800,blank=True,null=True)
    question=models.TextField(max_length=800,blank=True,null=True)
    # steps=ArrayField(models.CharField(max_length=50,blank=True,null=True), blank=True,null=True)

    # keywords=ArrayField(models.CharField(max_length=50,blank=True,null=True), blank=True,null=True)
    # input_list=ArrayField(models.CharField(max_length=50,blank=True,null=True), blank=True,null=True)
    # output_list=ArrayField(models.CharField(max_length=50,blank=True,null=True), blank=True,null=True)


    def __unicode__(self):
        return unicode(self.chapter)

class employer_task(models.Model):
    course=models.ForeignKey(Courses,blank=True, null=True)
    snippet=models.TextField(max_length=800,blank=True,null=True)
    student=models.ForeignKey(Account,max_length=80,blank=True,null=True,related_name='students')
    employer=models.ForeignKey(Account,max_length=80,blank=True,null=True)
    def __unicode__(self):
        return unicode(self.student)

class shortlist(models.Model):
    course=models.ForeignKey(Courses,blank=True, null=True)
    student=models.ForeignKey(Account,max_length=80,blank=True,null=True,related_name='student')
    employer=models.ForeignKey(Account,max_length=80,blank=True,null=True)
    time=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __unicode__(self):
        return unicode(self.student)