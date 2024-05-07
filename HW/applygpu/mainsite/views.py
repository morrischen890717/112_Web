from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import News

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