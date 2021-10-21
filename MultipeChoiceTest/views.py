from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import *

from django.contrib import messages

# Create your views here.


def index(request):
    subjects = Subject.objects.all()

    context = {
        'subjects': subjects
    }
    return render(request, 'index.html', context)

def subject(request, id):

    subject = Subject.objects.get(pk=id)
    exams = Exam.objects.filter(subject=id)

    context = {
        'subject': subject,
        'exams': exams,
    

    }

    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, request.POST['title'])
            return redirect('subject', id=id)
    else:
        form = ExamForm(initial=
        {
            'subject': subject.id,
            'teacher': request.user.teacher
        })

    context['form'] = form



    return render(request, 'subject.html', context)