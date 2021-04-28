from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.forms.widgets import Widget
from .models import Choice, Question

class CourseForm(forms.Form):
    course_title = forms.CharField(label='Course Name', max_length=100)
    CHOICES = [('Spring', 'Spring'), ('Fall', 'Fall')]
    course_semester = forms.ChoiceField(label='Course Semester', choices=CHOICES, widget=forms.RadioSelect)
    course_year = forms.IntegerField(label='Year', max_value=2099, min_value=2000)

class ModuleForm(forms.Form):
    module_name = forms.CharField(label = 'Module Name', max_length = 100)
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), widget=forms.CheckboxSelectMultiple)


class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Question text', max_length=100)
    
    
class QuizForm(forms.Form):
    quiz_title = forms.CharField(label = 'Quiz Name', max_length = 100)


class NewestUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Top:
        model = User
        fields = ("username", "email", "p1", "p2") #p1 is password 1, p2 is password 2

    def saveUser(self, commit=True):
        user = super(NewestUserForm, self).saveUser(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.saveUser()
        return user

