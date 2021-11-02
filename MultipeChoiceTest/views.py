from django.contrib.auth import login, logout
from django.http.response import Http404, HttpResponseRedirect
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
            'teacher': request.user.teacher,
            'status': 'wait'
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
    subject_id = exam.subject.id
    exam_form = ExamForm(request.POST or None, instance=exam)
    questions = Question.objects.filter(exam_c=exam)

    question_form = QuestionForm()

    if 'editExamBtn' in request.POST and exam_form.is_valid():
        exam_form.save()
        return redirect('exam', id=id)
    if 'deleteExamBtn' in request.POST:
        exam.delete()
        return redirect('subject', id=subject_id )
    if 'addQuestionBtn' in request.POST:

        question_title = request.POST['questionTitle']
        exam_question = exam
        new_question = Question(
            title = question_title,
            exam_c = exam_question
        )
        new_question.save()
        list_choices = ['choice1', 'choice2', 'choice3', 'choice4']
        for choice in list_choices:
            new_choice = request.POST[choice]
            if choice == request.POST['radioChoice']:
                is_correct = True
            else:
                is_correct = False
            new_exam_choice = Choice(
                question_c = new_question,
                title = new_choice,
                is_correct = is_correct

            )
            new_exam_choice.save()
        return redirect('exam', id = id)
    if 'deleteQuestionBtn' in request.POST:
        question = Question.objects.get(pk=request.POST['deleteQuestionBtn'])
        question.delete()
        return redirect('exam', id=id)
    if 'updateQuestionBtn' in request.POST:
        question = Question.objects.get(pk=request.POST['updateQuestionBtn'])
        question.title = request.POST['questionTitle']
        try:
            old_correct_choice = Choice.objects.get(question_c=question, is_correct=True)
        except:
            return Http404

        if request.POST['is_correct_check']:
            id = request.POST['is_correct_check']
            correct_choice = Choice.objects.get(pk=id)
            old_correct_choice.is_correct = False
            old_correct_choice.save()
            correct_choice.is_correct = True
            correct_choice.save()
        question.save()
        return redirect('exam', id = exam.id)

        



    context = {
        'exam': exam,
        'exam_form': exam_form,
        'questions': questions,
        'question_form': question_form

    }

    return render(request, 'exam/exam.html', context )
