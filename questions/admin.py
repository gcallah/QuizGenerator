from django.contrib import admin
from .models import Question, Module, Course, Choice
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Module)
admin.site.register(Course)