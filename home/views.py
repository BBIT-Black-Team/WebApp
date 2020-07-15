from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserAuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request=request, data=request.POST)
        print('Login', form.is_valid(), form.cleaned_data, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}")
                return redirect('/login')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    form = CustomUserAuthenticationForm()
    return render(request=request,
                  template_name="home/login.html",
                  context={"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print('Here', form.is_valid(), form.cleaned_data , )

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("/login")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="home/register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="home/register.html",
                  context={"form": form})
