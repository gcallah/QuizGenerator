from django import forms
from django.forms.widgets import Widget
from .models import Question

class CourseForm(forms.Form):
    course_title = forms.CharField(label='Course Name', max_length=100)
    CHOICES = [('Spring', 'Spring'), ('Fall', 'Fall')]
    course_semester = forms.ChoiceField(label='Course Semester', choices=CHOICES, widget=forms.RadioSelect)
    course_year = forms.IntegerField(label='Year', max_value=2099, min_value=2000)

class ModuleForm(forms.Form):
    module_name = forms.CharField(label = 'Module Name', max_length = 100)
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), widget=forms.CheckboxSelectMultiple)
    
class QuizForm(forms.Form):
    quiz_title = forms.CharField(label = 'Quiz Name', max_length = 100)
