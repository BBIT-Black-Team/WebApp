from django.shortcuts import render
from django.views.generic import FormView
from WebApp.forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
    return render(request, 'home/login.html')

