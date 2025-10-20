from django.shortcuts import render, HttpResponse
from .models import streams

# Create your views here.
def hello(request):
    name = streams.objects.all()
    return render(request, 'base.html', {'name': name})

