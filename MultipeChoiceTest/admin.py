from django.contrib import admin
from .models import *
# Register your models here.



class QuestionInline(admin.TabularInline):
    model = Question

@admin.register(Student)

class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)

class TeacherAdmin(admin.ModelAdmin):
    pass
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass