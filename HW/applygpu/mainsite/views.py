from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import News
from django.core.mail import send_mail

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

def simple_mail(repuest):
    send_mail(subject='Your Subject', 
              message='Your Message body', 
              from_email='test@lab402',
              recipient_list=['testing@gmail.com'])
    return HttpResponse('Message Send')