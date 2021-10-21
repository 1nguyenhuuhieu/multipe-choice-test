from django.shortcuts import render
from .models import *

# Create your views here.


def index(request):
    subjects = Subject.objects.all()

    context = {
        'subjects': subjects
    }
    return render(request, 'index.html', context)