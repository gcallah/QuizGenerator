from django.db import models
from django.db.models.base import Model


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text

    def get_choices(self):
        return self.choices.all()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Module(models.Model):
    questions = models.ManyToManyField(Question)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
