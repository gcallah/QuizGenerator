from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from questions.models import Course, Module, Question
from .forms import ModuleForm, courseForm

# Create your views here.
def index(request): #Generates the index page
    return render(request, 'index.html')

@login_required
def courses(request): #Allows users to add / change a course, also generates the courses page
    if request.method == 'POST':
        form = courseForm(request.POST)
        if form.is_valid():
            course_title = form.cleaned_data['course_title']
            course_semester = form.cleaned_data['course_semester']
            course_year = form.cleaned_data['course_year']
            semester = course_semester[3:] + str(course_year)[2:]
            c = Course.objects.create(title=course_title, semester=semester)
            c.save()
        
        return HttpResponseRedirect('/courses')

    else:
        form = courseForm()
        context = {
            'courses': Course.objects.all(),
            'form' : form
        }
        return render(request, 'courses.html', context)

def course_details(request, course_id): #generates the course details page
    course = Course.objects.get(pk= course_id)
    context = {
        'modules' : course.modules.all()
    }
    return render(request, 'course_details.html', context)

def modules(request):  # creates a module
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module_name = form.cleaned_data['module_name']
            course_id = form.cleaned_data['course_id']
            c = Course.objects.get(pk=course_id)
            m = Module.objects.create(name=module_name, course=c)
            m.save()
        return HttpResponseRedirect(f'/courses/{course_id}/')

#def add_question(request):
    #Question.objects.create(question_text=request.POST.get('question_text'))

def random_question(request):
    q = Question.objects.get(pk=1)
    return HttpResponse("random question: ", q.question_text)

def register(request): #allows the user to register into the site (if the username doesn't exist),  also generates the registration page
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect('/courses')
    context['form']=form
    return render(request,'registration/register.html',context)

def login(request): #login function
    pass
