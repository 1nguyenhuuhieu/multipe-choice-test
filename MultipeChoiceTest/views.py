from django.contrib.auth import login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.

@login_required
def index(request):
    subjects = Subject.objects.all()
    

    context = {
        'subjects': subjects
    }
    return render(request, 'index.html', context)


@login_required
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


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('index')
    else:
        form = UserProfileForm(instance=request.user)


    context = {

        'form': form

    }

    return render(request, 'registration/profile.html', context)

@login_required
def exam(request, id):
    exam = Exam.objects.get(pk=id)
    

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, request.POST['title'])
            return redirect('exam', id=id)
    else:
        form = QuestionForm()

    context = {
        'form': form,
        'exam': exam

    }

    return render(request, 'exam/exam.html', context )