from django.shortcuts import render
from django.http import HttpResponse
from questions.models import Question

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

#def add_question(request):
    #Question.objects.create(question_text=request.POST.get('question_text'))

def random_question(request):
    q = Question.objects.get(pk=1)
    return HttpResponse("random question: ", q.question_text)

