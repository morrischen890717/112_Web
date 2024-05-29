from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'base.html')

def eventPage(request):
    return render(request, 'eventPage.html')
