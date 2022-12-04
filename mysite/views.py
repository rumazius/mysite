from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import pdfkit
from django.template import Context, Template, loader

def registerPage(request: HttpRequest) -> HttpResponse:
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account was successfully created")
            return redirect('login')

    context = {"form": form}
    return render(request, 'reg.html', context)


def loginPage(request: HttpRequest) -> HttpResponse:
    form = CreateUserForm()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('register')

    # context = {"form": form}

    context = {}
    return render(request, 'login.html', context)


def homePage(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        surname = request.POST.get('surname')
        education = request.POST.get('education')
        skills = request.POST.get('skills')
        motivation = request.POST.get('motivation')
        achievements = request.POST.get('achievements')
        context = {
            'debug': "afd;kvgna;f",
            'surname': request.POST.get('surname'),
            'education': request.POST.get('education'),
            'skills': request.POST.get('skills'),
            'motivation': request.POST.get('motivation'),
            'achievements': request.POST.get('achievements'),
            'job_type': request.POST.get('job_type'),
        }

        t = render(request, 'cvpage.html', context)
        t = loader.get_template('cvpage.html')
        st = t.render(context)
        return render(request, 'cvpage.html', context)
    return render(request, 'home.html', context)

# def readycv(request: HttpRequest):
#     context = {}
#     return render(request, 'cvpage.html', context)