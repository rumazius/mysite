from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
import pdfkit
from django.template.loader import get_template


def blankPage(request: HttpRequest):
    return redirect('login')


def registerPage(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')
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
    if request.user.is_authenticated:
        return redirect('home')

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

    context = {}
    return render(request, 'login.html', context)


def homePage(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    if request.method == "POST":
        surname = request.POST.get('surname')
        education = request.POST.get('education')
        skills = request.POST.get('skills')
        motivation = request.POST.get('motivation')
        achievements = request.POST.get('achievements')
        context = {
            'surname': request.POST.get('surname'),
            'education': request.POST.get('education'),
            'skills': request.POST.get('skills'),
            'motivation': request.POST.get('motivation'),
            'achievements': request.POST.get('achievements'),
            'job_type': request.POST.get('job_type'),
        }

        page = get_template('cvpage.html')
        t = page.render(context)
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        ready_cv = pdfkit.from_string(t, False, configuration=config, options={"enable-local-file-access": ""})
        resp = HttpResponse(ready_cv, content_type='application/pdf')
        resp['Content-Disposition'] = 'attachment; filename=cv.pdf'

        return resp
    return render(request, 'home.html', context)
