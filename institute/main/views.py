from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Student, Course, Contact
from django.contrib import messages

def home(request):
    from .models import Course
    courses = Course.objects.all()[:3]  # show only top 3
    return render(request, 'home.html', {'course_list': courses})


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name, email=email, phone=phone, message=message
        )
        messages.success(request, "Thank you! Your message has been sent successfully.")
        return redirect('contact')

    return render(request, "contact.html")

def courses(request):
    data = Course.objects.all()
    return render(request, 'courses.html', {'course_list': data})



def signup(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        pwd = request.POST['password']
        user = User.objects.create_user(username=uname, email=email, password=pwd)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'msg': 'Invalid Credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


from django.contrib.auth.decorators import login_required
from .models import Student, Course

@login_required
def dashboard(request):
    students = Student.objects.count()
    courses = Course.objects.count()
    inquiries = Contact.objects.count()   # NEW

    return render(request, 'dashboard.html', {
        'students': students,
        'courses': courses,
        'inquiries': inquiries,   # NEW
    })

from django.shortcuts import get_object_or_404

@login_required
def add_student(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            contact=request.POST['contact'],
            course_id=request.POST['course']
        )
        return redirect('view_students')
    return render(request, 'add_student.html', {'courses': courses})


@login_required
def view_students(request):
    data = Student.objects.all()
    return render(request, 'view_students.html', {'students': data})


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    courses = Course.objects.all()
    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.contact = request.POST['contact']
        student.course_id = request.POST['course']
        student.save()
        return redirect('view_students')
    return render(request, 'edit_student.html', {'student': student, 'courses': courses})


@login_required
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('view_students')


@login_required
def add_course(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        fees = request.POST['fees']
        Course.objects.create(title=title, description=description, fees=fees)
        return redirect('dashboard')
    return render(request, 'add_course.html')


@login_required
def inquiries(request):
    msgs = Contact.objects.all().order_by('-id')
    return render(request, 'inquiries.html', {'messages': msgs})


from django.contrib import messages

def book_demo(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course = request.POST.get("course")

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            interested_course=course,
            message="Home page demo request"
        )
        messages.success(request, "🎉 Your demo class request has been submitted successfully!")
        return redirect('home')

    return redirect('home')
