from django import forms
from django.forms import ModelForm

from .models import *

class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {'teacher': forms.HiddenInput(),
        'subject': forms.HiddenInput(),
        'questions': forms.HiddenInput() }
