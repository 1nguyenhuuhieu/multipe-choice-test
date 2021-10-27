from django import forms
from django.forms import ModelForm, fields

from .models import *
from django.contrib.auth.models import User
class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {'teacher': forms.HiddenInput(),
        'subject': forms.HiddenInput(),
        'questions': forms.HiddenInput() }

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['password','first_name', 'last_name', 'email']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'