from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"home.html")

def login(request):
    return render(request,"Log In.html")

def error(request):
    return render(request,"errorpage.html")

