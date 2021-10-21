from django.contrib import admin
from .models import *
# Register your models here.



class QuestionInline(admin.TabularInline):
    model = Question

@admin.register(Student,
Teacher,
Subject,
Question,
Choice,
Exam,
StudentExam,
StudentExamQuestion
)



class StudentAdmin(admin.ModelAdmin):
    pass

class TeacherAdmin(admin.ModelAdmin):
    pass

class SubjectAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

class ChoiceAdmin(admin.ModelAdmin):
    pass

class ExamAdmin(admin.ModelAdmin):
    pass
class StudentExamAdmin(admin.ModelAdmin):
    pass

class StudentExamQuestionAdmin(admin.ModelAdmin):
    pass