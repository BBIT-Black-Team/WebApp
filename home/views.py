from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserAuthenticationForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request=request, data=request.POST)
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
        form = CustomUserCreationForm(request.POST)

        print('Register', form.is_valid(), form.cleaned_data)
        # form.is_valid()
        # print('ok', form.cleaned_data.get('password1'), form.cleaned_data.get('password2'))
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f"New account created: {email}")
            login(request, user)
            return redirect("/login")

        else:
            for key in form.errors:
                for msg in form.errors[key]:
                    messages.error(request, msg)
                    break
                break

            # for msg in form.error_messages:
            #     messages.error(request, f"{form.error_messages[msg]}")

            return render(request=request,
                          template_name="home/register.html",
                          context={"form": form})

    form = CustomUserCreationForm
    return render(request=request,
                  template_name="home/register.html",
                  context={"form": form})
