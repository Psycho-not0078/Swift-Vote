from django.shortcuts import render,redirect
# from .models import userDetails
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import auth
# Create your views here.
def index(request):
    return render(request,"home.html")

def login(request):
    # if request.method == 'POST':
    #     email = str(request.POST['email']).lower()
    #     password = request.POST['password']
    #     try:
    #         user = userDetails.objects.get(email=email)
    #         if check_password(password, user.password):
    #             user = auth.authenticate(request, email=email, password=password)
    #             auth.login(request, user)
    #             return redirect('/')
    #         else:
    #             return render(request, 'Log In.html', {'msg': 'Invalid Credentials'})
    #     except Exception as e:
    #         return render(request, 'Log In.html', {'msg': 'Invalid Credentials' + str(e)})
    # else:
        return render(request,"Log In.html")

def register(request):
    # if request.method == 'POST':
    #     email = request.POST['Email']
    #     pwd = request.POST['Password']
    #     userType = request.POST['flexRadioDefault']
    #     user = userDetails.objects.create_user(
    #         email=email, password=pwd, type=userType)
    #     user.save()
    #     return redirect('/login')
    # else:
        return render(request,"Sign Up.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def error(request):
    return render(request,"errorpage.html")

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

def createElection(request):
    return render(request,"create_election.html")

def disableElection(request):
    return render(request,"disable_election.html")

def electionHistory(request):
    return render(request,"election_history.html")