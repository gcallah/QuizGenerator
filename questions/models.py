from django.db import models
from django.db.models.base import Model


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text

    def get_choices(self):
        return self.choices.all()

    def edit(self):
        question_text = models.CharField(max_length = 200)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Course(models.Model):
    title = models.TextField()
    semester = models.CharField(max_length=16)

    def num_of_modules(self):
        return self.modules.count()

    def __str__(self):
        return self.title

    def edit(self):
        title = models.TextField()
        semester = models.CharField(max_length = 16)

class Module(models.Model):
    questions = models.ManyToManyField(Question)
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', default='')

    def __str__(self):
        return self.name
    
    def edit(self):
        questions = models.ManyToManyField(Question)
        name = models.CharField(max_length = 200)
        course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'modules', default = '')

class Quiz(models.Model):
    questions = models.ManyToManyField(Question)
    name = models.CharField(max_length = 200)
    module = models.ForeignKey(Module, on_delete = models.CASCADE, related_name = 'quizzes', default = '')
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'quizzes', default = '')

    def __str__(self):
        return self.name
    
    def get_questions(self):
        #Figure out how to take in a random number of questions
        return self.questions.all()
        

    def num_of_questions(self):
        return self.questions.count()

