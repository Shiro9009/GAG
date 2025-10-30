from django.shortcuts import render, HttpResponse
from .models import Streams

# Create your views here.
def page1(request):
    name = Streams.objects.all()
    return render(request, 'base.html', {'name': name})

def page2(request):

    return render(request, 'page-2.html')

def page3(request):

    return render(request, 'page-3.html')
    
def page4(request):

    return render(request, 'page-4.html')

def page5(request):

    return render(request, 'page-5.html')
