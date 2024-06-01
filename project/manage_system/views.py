from django.shortcuts import render
from .models import Event

# Create your views here.
def homepage(request):
    return render(request, 'base.html')

def eventPage(request):
    events = Event.objects.all()
    return render(request, 'eventPage.html', locals())
