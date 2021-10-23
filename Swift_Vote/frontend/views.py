from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,"Log In.html")

def error(request):
    return render(request,"errorpage.html")