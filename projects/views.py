from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

import math, random
# from django_otp.oath import hotp

from .models import Department, Participant, Department, Exam, Question
from .forms import DepartmentForm, ParticipantForm, QuestionForm, ExamForm, CustomUserForm

from django.views.decorators.cache import cache_control

# department list
def home(request):
    departmentList = Department.objects.all()
    return render(request, 'home.html', {'departments': departmentList})

# department page
def department(request, dept_id):
    departmentObj = Department.objects.get(id = dept_id)
    examObj = Exam.objects.filter(name = departmentObj.id)
    return render(request, 'department.html', {'department': departmentObj, 'exams': examObj})

# exam page
def exam(request, exam_id, dept_id):
    examObj = Exam.objects.get(id = exam_id)
    return render(request, 'exam.html', {'exam': examObj, 'departmentID': dept_id})

# create new exam
@login_required(login_url="loginUser")
def createExam(request, dept_id):
    form = ExamForm()
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Exam Created.")
            return redirect('department', dept_id = dept_id )
    context = {'form': form, 'departmentID': dept_id}
    return render(request, 'create-exam.html', context)

# add new question
@login_required(login_url="loginUser")
def createQuestion(request, dept_id):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Question Created.")
            return redirect('department', dept_id)
    context = {'form': form}
    return render(request, 'create-question.html', context)

# update question
@login_required(login_url="loginUser")
def updateQuestion(request, dept_id, exam_id, que_id):
    questionObj = Question.objects.get(id = que_id)
    form = QuestionForm(instance = questionObj)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance = questionObj)
        if form.is_valid():
            form.save()
            messages.info(request, "Question Updated.")
            return redirect('exam', dept_id, exam_id)
    context = {'form': form}
    return render(request, 'create-question.html', context)

# edit exam
@login_required(login_url="loginUser")
def updateExam(request, dept_id, exam_id):
    examObj = Exam.objects.get(id = exam_id)
    form = ExamForm(instance = examObj)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance = examObj)
        if form.is_valid():
            form.save()
            messages.info(request, "Exam Updated.")
            return redirect('department', dept_id = dept_id)
    context = {'form': form}
    return render(request, 'create-exam.html', context)

# delete exam
@login_required(login_url="loginUser")
def deleteExam(request, dept_id, exam_id):
    examObj = Exam.objects.get(id = exam_id)
    if request.method == 'POST':
        examObj.delete()
        messages.warning(request, "Exam Deleted Successfully.")
        return redirect('department', dept_id = dept_id)
    context = {'object': examObj, "dept_id": dept_id}
    return render(request, 'delete-exam.html', context)

# create new department
@login_required(login_url="loginUser")
def createDepartment(request):
    form = DepartmentForm()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Department created successfully.")
            return redirect('home')
    context = {'form': form}
    return render(request, 'create-question.html', context)

# function to generate OTP
def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def emailVerification(request, part_id):
    if request.method == "POST":
        otp = request.POST['num1'] + request.POST['num2'] + request.POST['num3'] + request.POST['num4']
        participantObj = Participant.objects.get(id = part_id)
        examObj = Exam.objects.get(code = "123456")
        if otp == participantObj.code:
            messages.info(request, "Email Verified !!")
            return redirect('quiz', examObj.id, part_id)
        else:
            messages.warning(request, "Enter Correct OTP.")
    return render(request, 'email-verification.html')
  
# add participant
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createParticipant(request):
    form = ParticipantForm()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participantObj = form.save(commit=False)
            otp = generateOTP()
            participantObj.code = otp
            participantObj.save()
            subject = 'Email Verification'
            message = 'OTP: ' + otp
            send_mail(
                subject, 
                message,
                settings.EMAIL_HOST_USER,
                [participantObj.email],
                fail_silently = True
            )
            return redirect('email-verification', participantObj.id)
            # return redirect('quiz', examObj.id, partObj.id)
    context = {'form': form}
    return render(request, 'create-participant.html', context)

# user login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            messages.warning(request, "User does not exist.")
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "User login successfully..")
            return redirect("home")
        else:
            messages.warning(request, "Username or Password are incorrect.")
    context = {"page": page}
    return render(request, 'login_for_recruiter.html', context)

# logout
def logoutUser(request):
    logout(request)
    messages.info(request, "User successfully logout..")
    return redirect('loginUser')

# user register
def registerUser(request):
    page = "register"
    form = CustomUserForm()

    if request.method == "POST":
        form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            messages.success(request, "User login successfully..")
            return redirect("home")
        else:
            messages.warning(request, "An error occurred..")
            return redirect("registerUser")

    context = {"page": page, "form": form}
    return render(request, "login_for_recruiter.html", context)

# home page
def quizapp(request):
    logout(request)
    messages.info(request, "User successfully logout..")
    return render(request, 'quizapp.html')

