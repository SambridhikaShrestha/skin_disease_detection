from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("<h1> hello Sam</h1>")

def root(request):
    return render(request, template_name="home.html")
    #return HttpResponse("This is root page")