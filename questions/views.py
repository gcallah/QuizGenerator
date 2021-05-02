from django.db.models import fields
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from questions.models import Choice, Course, Module, Question
from .forms import ModuleForm, CourseForm, QuestionForm, NewestUserForm


# Create your views here.
def index(request): #Generates the index page
    if request.user.is_authenticated :
        return HttpResponseRedirect('/courses')
    return render(request, 'index.html')

#@login_required
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

def create_question(request): #creates a question
    #Question.objects.create(question_text=request.POST.get('question_text'))
    if request.method == 'POST':
        form = request.POST
        question = form['question_text']
        q = Question.objects.create(question_text=question)
        q.save()
        for i in range(4):
            c_text = form['choice' + str(i)]
            if c_text:
                answer = form.__contains__('choice' + str(i) + '-answer')
                c = Choice.objects.create(choice_text=c_text, is_answer=answer, question=q)
                c.save()
        return HttpResponse(200)
    return render(request, 'create_question.html', {'question_form': QuestionForm})


def register(request): #allows the user to register into the site (if the username doesn't exist),  also generates the registration page
    context = {}
    form = NewestUserForm(request.POST or None) #UserCreationForm replaced with NewestUserForm
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(user)
            return HttpResponseRedirect('/courses')
    context['form']=form
    return render(request,'registration/register.html',context)

def login_request(request): #login function
    #if login info is already registered, login is valid 
    if request.method == 'POST':
        form = AuthenticationForm()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username and/or password.")
        else:
            messages.error(request, "Invalid username and/or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', context = {"form": form})
    
def logout_request(request): #logout function
    logout(request)
    messages.info(request, "Successfully logged out.")
    return redirect("/")

def edit_course(request, course_id): # Edit course info
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course_title = form.cleaned_data['course_title']
            course_semester = form.cleaned_data['course_semester']
            course_year = form.cleaned_data['course_year']
            semester = course_semester + " " + str(course_year)
            course.update_title(course_title)
            course.update_semester(semester)
            course.save()

        return HttpResponseRedirect('/courses') #redirect to the courses page

    else:
        form = CourseForm()
        context = {
            'course': course,
            'course_id': course_id,
            'form' : form
        }
        return render(request, 'edit_course.html', context) #return edit_module html page

def edit_module(request, module_id): #edit module info
    module = Module.objects.get(pk = module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.isValid():
            name = form.cleaned_data['module_name']
            q = form.cleaned_data['questions']
            module.update_name(name)
            module.questions.set(q)
            module.save()
        return HttpResponseRedirect('/create_module') #redirect to the create_module page
    else:
        form = ModuleForm()
        context = {
                'form': form,
                'course_id': course_id
                }
        return render(request, 'edit_module.html', context) #return edit_module html page

def edit_question(request, question_id): #edit question info
    question = Question.objects.get(pk = question_id)
    if request.method == 'POST':
        print(request.POST)
        return HttpResponse(200)
    QuestionFormSet = inlineformset_factory(Question, Choice, fields = ('choice_text', 'is_answer'), extra = 4)
    return render(request, 'edit_question.html', {'question_form':QuestionForm, 'choices_form':QuestionFormSet}) #return edit_questions html page

def delete_course(request, course_id): #function to delete a course if necessary
    course = Course.objects.get(pk=course_id)
    course.delete()

    return HttpResponseRedirect('/courses') #redirect to the courses page

def delete_module(request, module_id): #function to delete a module if necessary
    module = Module.objects.get(pk = module_id)
    module.delete()

    return HttpResponseRedirect('/courses/{course_id}/') #redirect to the courses page

def delete_question(request, question_id): #function to delete a question if necessary
    question = Question.objects.get(pk = question_id)
    question.delete()

    return HttpResponseRedirect('/create_module') #redirect to the create_module page
