from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from questions.models import Course, Question
from .forms import courseForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def courses(request):
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

def course_details(request, course_id):
    course = Course.objects.get(pk= course_id)
    context = {
        'modules' : course.modules.all()
    }
    return render(request, 'course_details.html', context)

#def add_question(request):
    #Question.objects.create(question_text=request.POST.get('question_text'))

def random_question(request):
    q = Question.objects.get(pk=1)
    return HttpResponse("random question: ", q.question_text)

def register(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect('/courses')
    context['form']=form
    return render(request,'registration/register.html',context)
