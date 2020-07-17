from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserAuthenticationForm, FacultyCreationForm, CustomUserCreationForm
from .models import Faculty, Subject, ExamBlock, AssessmentDetail
from pprint import pprint


@login_required(login_url='/login')
def home_view(request):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    pprint(isFaculty)
    if not isFaculty:
        return render(request=request, template_name='home/home_admin.html')
    return render(request=request, template_name='home/home_faculty.html')


@login_required(login_url='/login')
def examblock_view(request):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    if not isFaculty:
        return render(request, 'home/admin_block.html', context={'exam_block': ExamBlock.objects.all()})
    return redirect('home')


@login_required(login_url='/login')
def assessment_view(request):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    if not isFaculty:
        return render(request, 'home/admin_assessment_details.html', context={'assessment_details': AssessmentDetail.objects.all()})
    return redirect('home')



@login_required(login_url='/login')
def faculty_details_view(request):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    if not isFaculty:
        return render(request, 'home/admin_faculty_details.html', context={'faulty_details': Faculty.objects.all()})
    return redirect('home')



@login_required(login_url='/login')
def examblock_edit(request, id):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    if not isFaculty:
        return render(request, 'home/edit_exam_block.html', context={'exam': ExamBlock.objects.filter(id=id)})
    return redirect('home')




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
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    form = CustomUserAuthenticationForm()
    return render(request=request,
                  template_name="home/login.html",
                  context={"form": form})


def faculty_register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            faculty = FacultyCreationForm({"user": user, "subjects": request.POST.getlist('subjects')})
            if faculty.is_valid():
                faculty.save()
            faculty.save()

            email = form.cleaned_data.get('email')
            messages.success(request, f"New account created: {email}")
            login(request, user)
            return redirect("home")

        else:
            for key in form.errors:
                for msg in form.errors[key]:
                    pprint(key)
                    messages.error(request, msg)
                    break
                break
            return render(request=request,
                          template_name="home/register.html",
                          context={"form": form, "subjects": Subject.objects.all()})

    form = CustomUserCreationForm

    return render(request=request,
                  template_name="home/register.html",
                  context={"form": form, "subjects": Subject.objects.all()})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")
