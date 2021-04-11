from django import forms
import datetime

class courseForm(forms.Form):
    course_title = forms.CharField(label='Course Name', max_length=100)
    CHOICES = [('spring', 'spring'), ('fall', 'fall')]
    course_semester = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    course_year = forms.IntegerField(label="year", max_value=2099, min_value=2000)

class ModuleForm(forms.Form):
    module_name = forms.CharField(label = 'Module Name', max_length = 100)
