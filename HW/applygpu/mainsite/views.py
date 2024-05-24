from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import News, User

# Create your views here.
def homepage(request):
    newss = News.objects.all()
    return render(request, 'index.html', locals())

def showNews(request, slug):
    try:
        news = News.objects.get(slug=slug)
        return render(request, 'news.html', locals())
    except:
        return redirect('/')

def applyRule(request):
    return render(request, 'applyRule.html')

def applyStatus(request):
    return render(request, 'applyStatus.html')

def registerPage(request):
    return render(request, 'register.html')

def register(request):
    try:
        studentId = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
    except:
        studentId = email = password = None
    if User.objects.filter(studentId=studentId).exist():
        print(f'studentId {studentId} is already exist.')
    if User.objects.filter(email=email).exist():
        print(f'email {email} is already exist.')
    newUser = User(studentId=studentId, email=email, password=password)
    newUser.save()
    return redirect('/')

        

#def login(request):