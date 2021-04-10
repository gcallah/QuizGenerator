from django.db import models
from django.db.models.base import Model


class Question(models.Model): #This class creates a question.
    question_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text

    def get_choices(self):
        return self.choices.all()

    def edit(self):
        question_text = models.CharField(max_length = 200)

class Choice(models.Model): #Creates choices for the questions 
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
    
    def edit(self):
        question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
        choice_text = models.CharField(max_length=200)
        is_answer = models.BooleanField(default=False)

class Course(models.Model): #Creates a course for use by a professor 
    title = models.TextField()
    semester = models.CharField(max_length=16)

    def num_of_modules(self):
        return self.modules.count()

    def __str__(self):
        return self.title

    def edit(self):
        title = models.TextField()
        semester = models.CharField(max_length = 16)

class Module(models.Model): #This creates a module for courses, can be tied to multiple courses and have multiple questions
    questions = models.ManyToManyField(Question)
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', default='')

    def __str__(self):
        return self.name
    
    def edit(self):
        questions = models.ManyToManyField(Question)
        name = models.CharField(max_length = 200)
        course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'modules', default = '')

class Quiz(models.Model): #Creates a quiz for courses.
    questions = models.ManyToManyField(Question)
    name = models.CharField(max_length = 200)
    module = models.ForeignKey(Module, on_delete = models.CASCADE, related_name = 'quizzes', default = '')
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'quizzes', default = '')

    def __str__(s.lf):
        return self.name
    
    def get_questions(self):
        #Figure out how to take in a random number of questions
        return self.questions.all()
        

    def num_of_questions(self):
        return self.questions.count()
    
    def edit(self):
        questions = models.ManyToManyField(Question)
        name = models.CharField(max_length = 200)
        module = models.ForeignKey(Module, on_delete = models.CASCADE, related_name = 'quizzes', default = '')
        course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'quizzes', default = '')
        

