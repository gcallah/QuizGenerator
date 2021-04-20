from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from questions.models import Course, Module, Question
from .forms import ModuleForm, CourseForm

# Create your views here.
def index(request): #Generates the index page
    if request.user.is_authenticated :
        return HttpResponseRedirect('/courses')
    return render(request, 'index.html')

@login_required
def courses(request): #Allows users to add / change a course, also generates the courses page
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course_title = form.cleaned_data['course_title']
            course_semester = form.cleaned_data['course_semester']
            course_year = form.cleaned_data['course_year']
            semester = course_semester + " " + str(course_year)
            c = Course.objects.create(title=course_title, semester=semester)
            c.save()
        
        return HttpResponseRedirect('/courses')

    else:
        form = CourseForm()
        context = {
            'courses': Course.objects.all(),
            'form' : form
        }
        return render(request, 'courses.html', context)

def course_details(request, course_id): #generates the course details page
    course = Course.objects.get(pk= course_id)
    context = {
        'course_id': course.pk,
        'modules' : course.modules.all()
    }
    return render(request, 'course_details.html', context)

def create_module(request, course_id):  # creates a module
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['module_name']
            q = form.cleaned_data['questions']
            c = Course.objects.get(pk=course_id)
            m = Module.objects.create(name=name, course=c)
            m.questions.set(q)
            m.save()
        return HttpResponseRedirect(f'/courses/{course_id}/')
    form = ModuleForm()
    context = {
        'form': form,
        'course_id': course_id
    }
    return render(request, 'create_module.html', context)

#def add_question(request):
    #Question.objects.create(question_text=request.POST.get('question_text'))

def random_question(request): #function to generate random questions
    q = Question.objects.get(pk=1)
    return HttpResponse("random question: ", q.question_text)

def register(request): #allows the user to register into the site (if the username doesn't exist),  also generates the registration page
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(user)
            return HttpResponseRedirect('/courses')
    context['form']=form
    return render(request,'registration/register.html',context)

def login(request): #login function
    #if login info is already registered, login is valid 
    '''
    #need to check if the username and password match what is in the database
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect('/courses')
    context['form']=form
    return render(request,'registration/register.html',context)
    
    '''
    
    return HttpResponseRedirect('/login')

def delete_course(request, course_id): #function to delete a course if necessary
    course = Course.objects.get(pk=course_id)
    course.delete()

    return HttpResponseRedirect('/courses')

def delete_module(request, module_id): #function to delete a module if necessary
    module = Module.objects.get(pk = module_id)
    module.delete()

    return HttpResponseRedirect('/courses/{course_id}/')
