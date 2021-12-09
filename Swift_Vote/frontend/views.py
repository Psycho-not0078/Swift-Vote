from django.shortcuts import render,redirect
from .models import candidateHistory, userDetails, election, location
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import auth
from .forms import UserForm
# Create your views here.
def index(request):
    return render(request,"home.html")

def login(request):
    if request.method == 'POST':
        email = str(request.POST['email']).lower()
        password = request.POST['password']
        try:
            user = userDetails.objects.get(email=email)
            if check_password(password, user.password):
                user = auth.authenticate(request, email=email, password=password)
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'Log In.html', {'msg': 'Invalid Credentials'})
        except Exception as e:
            return render(request, 'Log In.html', {'msg': 'Invalid Credentials' +"  "+ str(e)})
    else:
        return render(request,"Log In.html")

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = str(request.POST['email']).lower()
        contact = request.POST['contact']
        dob = request.POST['dob']
        password = request.POST['password']
        username = request.POST['username']
        address = request.POST['address']
        user = userDetails.objects.create_user(
            username=username,email=email,dob=dob,Address=address ,fName=fname,lName=lname, contactNumber=contact,password = password)
        user.save()
        return redirect('/login')
    else:
        return render(request, 'Sign Up.html')
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
    if request.method == "POST":
        ec = election()
        ec.ec_name = request.POST.get('ecName')
        ec.sDate = request.POST.get('startDate')
        ec.electionType  = request.POST.get('ecType')
        ec.fDate = request.POST.get('endDate')
        ec.save()

        locate = location()
        locate.locationName = request.POST.get('state')
        locate.save()

        return redirect('/electionSetting')
    else:
        return render(request, "create_election.html")

def disableElection(request):
    if request.method == "POST":
        try:
            sTerm = request.POST.get('ecSearch')
            term = election.objects.get(ec_name=sTerm)
            print(term)
            return render(request,"disable_election.html", {'st':term})
        except election.DoesNotExist:
            return redirect("disableElection")

    else:
        return render(request, "disable_election.html")

def electionHistory(request):
    history = election.objects.all()
    print(history)
    return render(request,"election_history.html", {'hist': history})