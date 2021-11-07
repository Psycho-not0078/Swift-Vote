from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"home.html")

def login(request):
    return render(request,"Log In.html")

def error(request):
    return render(request,"errorpage.html")

def register(request):
    return render(request,"Sign Up.html")

def candidateDB(request):
    return render(request,"candidate_db.html")

def ecDB(request):
    return render(request,"ec_db.html")

def electionSetting(request):
    return render(request,"ElectionSetting.html")

def myAccount(request):
    return render(request,"MyAccount.html")

def updateProfile(request):
    return render(request,"UpdateProfile.html")

def voterDB(request):
    return render(request,"voter_db.html")