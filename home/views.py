from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserAuthenticationForm, FacultyCreationForm, CustomUserCreationForm, ExamAddForm, AssessmentAddForm, AddPaper
from .models import Faculty, Subject, ExamBlock, AssessmentDetail, Assessment
from pprint import pprint


@login_required(login_url='/login')
def home_view(request):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    pprint(isFaculty)
    if not isFaculty:
        if(request.POST):
            # Main Algo
            Assessment.objects.all().delete()
            faculty = Faculty.objects.all()
            assessment = AssessmentDetail.objects.all()
            for ass in assessment:
                subject_faculty = Faculty.objects.filter(subjects=ass.subject)
                if len(subject_faculty) == 0:
                    messages.error(request, f'No Faculty Found for {ass.subject}')
                    break

                # Distrubiting
                each = int(ass.total_answer_sheets / len(subject_faculty))
                total = ass.total_answer_sheets
                for faculty in subject_faculty:
                    left = total - each if total - each > 0 else 0
                    first_ans_sheet = int(ass.first_ans_sheet)
                    last_ans_sheet = int(ass.last_ans_sheet)

                    assessment_local = Assessment(subject=ass.subject, total_answer_sheets=left, first_ans_sheet=first_ans_sheet, last_ans_sheet=last_ans_sheet)
                    assessment_local.save()
                    faculty.assessment.add(assessment_local)
                    first_ans_sheet += each
                    last_ans_sheet += each
            messages.success(request, 'Successfully Assigned')
        return render(request=request, template_name='home/home_admin.html')

    return render(request=request, template_name='home/home_faculty.html', context={'faculty': Faculty.objects.get(user=request.user.id)})


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
def examblock_add(request):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    if not isFaculty:
        if request.POST:
            form = ExamAddForm(request.POST)
            pprint(form.is_valid())
            pprint(form.cleaned_data)
            if form.is_valid():
                form.save()
                messages.success(request, f'Exam Successfully Added.')
            else:
                messages.error(request, 'Something Went Wrong')
                pprint(form.errors)

            pass
        return render(request, 'home/edit_exam_block.html',)
    return redirect('home')

@login_required(login_url='/login')
def examblock_edit(request, id):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    exam = ExamBlock.objects.filter(pk=id)
    if len(exam) == 0:
        return redirect('exam_block_add')
    exam = exam[0]
    if not isFaculty:
        if request.POST:
            form = ExamAddForm(request.POST or None, instance=exam)
            if form.is_valid():
                form.save()
                messages.success(request, f'Exam Successfully Saved.')
            else:
                messages.error(request, 'Something Went Wrong')
                pprint(form.errors)

            pass
        return render(request, 'home/edit_exam_block.html', context={"exam": exam})
    return redirect('home')


@login_required(login_url='/login')
def assessment_add(request):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    if not isFaculty:
        if request.POST:
            form = AssessmentAddForm(request.POST)
            pprint(form.is_valid())
            pprint(form.cleaned_data)
            if form.is_valid():
                form.save()
                messages.success(request, f'Saved Successfully.')
            else:
                messages.error(request, 'Something Went Wrong')
                pprint(form.errors)

            pass
        return render(request, 'home/edit_assessment_form.html', context={"subjects": Subject.objects.all()})
    return redirect('home')


@login_required(login_url='/login')
def assessment_edit(request, id):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    assessment = AssessmentDetail.objects.filter(pk=id)
    if len(assessment) == 0:
        return redirect('assessment_add')
    assessment = assessment[0]
    if not isFaculty:
        if request.POST:
            form = AssessmentAddForm(request.POST or None, instance=assessment)
            if form.is_valid():
                form.save()
                messages.success(request, f'Successfully Saved.')
            else:
                messages.error(request, 'Something Went Wrong')
                pprint(form.errors)

            pass
        return render(request, 'home/edit_assessment_form.html', context={"assessment": assessment, "subjects": Subject.objects.all()})
    return redirect('home')



@login_required(login_url='/login')
def faculty_assement_edit(request, id):
    isFaculty = True if len(Faculty.objects.filter(user=request.user)) > 0 else False
    ass = Assessment.objects.filter(pk=id)
    if len(ass) == 0:
        return redirect('home')

    ass = ass[0]
    if isFaculty:
        if request.POST:
            form = AddPaper(request.POST)
            pprint(form.is_valid())
            pprint(form.cleaned_data)
            if form.is_valid():
                paper = form.save()
                ass.checked.add(paper)
                messages.success(request, f'Saved Successfully.')
            else:
                messages.error(request, 'Something Went Wrong')
                pprint(form.errors)

            pass
        return render(request, 'home/edit_assessment_faculty_.html', context={"assessment": ass, "range": range(int(ass.first_ans_sheet), int(ass.last_ans_sheet))})
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
