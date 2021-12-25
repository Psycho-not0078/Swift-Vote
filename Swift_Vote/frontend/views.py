from django.db.models import deletion
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import auth
from .forms import UserForm
import web3
from .solWarper import *
from datetime import datetime

# from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.core.mail import send_mail


w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
handle = deploy_contract()
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        obj = userDetails.objects.get(email=request.user.get_username())
    else:
        obj = ""
    return render(request, "home.html", {"obj": obj})


def login(request):
    if request.method == "POST":
        email = str(request.POST["email"]).lower()
        password = request.POST["password"]
        try:
            user = userDetails.objects.get(email=email)
            print(user.password)
            if check_password(password, user.password):
                print(12345)
                user = auth.authenticate(request, email=email, password=password)
                auth.login(request, user)
                return redirect("/")
            else:
                return render(request, "Log In.html", {"msg": "Invalid Credentials dcfvghbj"})
        except Exception as e:
            return render(
                request, "Log In.html", {"msg": "Invalid Credentials" +"  "+ str(e)}
            )  #  
    else:
        return render(request, "Log In.html")


def register(request):
    if request.method == "POST":

        acc = Accounts()
        acc.accountType = request.POST["utype"]
        acc.accountAddress = addUser(handle, request.POST["address"])
        acc.usable = False  # make the value 1 when ec starts
        acc.save()

        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = str(request.POST["email"]).lower()
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        password = request.POST["password"]
        username = request.POST["username"]
        address = request.POST["address"]
        utype = request.POST["utype"]

        
        user = userDetails.objects.create_user(
            username=username,
            email=email,
            dob=dob,
            address=address,
            fName=fname,
            lName=lname,
            contactNumber=contact,
            password=password,
            accountId = acc,
            type=utype,
        )
        user.save()
        return redirect("/login")
    else:
        return render(request, "Sign Up.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


def error(request):
    return render(request, "errorpage.html")


def candidateDB(request):
    return render(request, "candidate_db.html")


def candidateApplication(request):
    if request.user.is_authenticated:
        obj = userDetails.objects.get(email=request.user.get_username())
    if request.method == "POST":
        cd = candidates()
        obj = userDetails.objects.get(email=request.user.get_username())
        print(obj.uid)
        cd.candidateName = request.POST.get("cName")
        cd.cDob = request.POST.get("doB")
        cd.cState = request.POST.get("state")
        print(cd.cState)
        cd.cCity = request.POST.get("city")
        cd.electionType = request.POST.get("ecType")
        cd.party = request.POST.get("party")
        cd.uid = obj.uid
        cd.save()
        # BC
        addCandidate(handle, request.POST.get("cName"), request.POST.get("state"))

        return redirect("/")
    else:
        if request.user.is_authenticated:
            dob = str(obj.dob)
            print(dob)
            return render(request, "candidateApplication.html", {"obj": obj, "dob1":dob})
        else:
            return render(request, "candidateApplication.html")


def ecDB(request):
    return render(request, "ec_db.html")


def electionSetting(request):
    return render(request, "ElectionSetting.html")


def myAccount(request):
    return render(request, "MyAccount.html")


def updateProfile(request):
    if request.user.is_authenticated:
        obj = userDetails.objects.get(email=request.user.get_username())
    if request.method == "POST":
        obj.fName = request.POST["fname"]
        obj.lName = request.POST["lname"]
        obj.email = str(request.POST["email"]).lower()
        obj.contactNumber = request.POST["contact"]
        obj.dob = request.POST["dob"]
        obj.username = request.POST["username"]
        obj.address = request.POST["address"]
        obj.save()
        return redirect("/")
    else:
        if request.user.is_authenticated:
            return render(request, "UpdateProfile.html", {"obj": obj})
        else:
            return render(request, "UpdateProfile.html")


def voterDB(request):
    # datetime object containing current date and time
    now = datetime.now().date()
    # dd/mm/YY I:M:
    print(now)
    get_ec = (
        election.objects.filter(sDate=now).filter(status="enable").values("location")
    )
    loc_list = list(get_ec)

    for i in loc_list:
        if request.user.is_authenticated:
            obj = userDetails.objects.get(email=request.user.get_username())
            if obj.voted != True:
                changeAblity(handle,obj.accountId.accountAddress,1,1)
                if obj.address == i["location"]:
                    start = True
                    return render(request, "voter_db.html", {"st": start})
                    # for all the locations - General Elections
                if i["location"] == "all":
                    start = True
                    return render(request, "voter_db.html", {"st": start})
            else:
                start = False
                return render(request, "voter_db.html", {"st": start})
    return render(request, "voter_db.html")


def createElection(request):
    if request.method == "POST":
        ec = election()
        ec.ec_name = request.POST.get("ecName")
        # Converting data to datetime format
        ec.sDate = request.POST.get("startDate")
        ec.fDate = request.POST.get("endDate")
        # sdt = str(sd) + ' ' + str(st)
        # edt = str(ed) + ' ' +str(et)
        # datetime_object1 = datetime.strptime( sdt, '%Y-%m-%d %H:%M')
        # datetime_object2 = datetime.strptime(edt, '%Y-%m-%d %H:%M')
        # ec.sDate = datetime_object1
        x = request.POST.get("ecType")

        if x == "General Elections":
            ec.electionType = x
            ec.location = "all"
        else:
            ec.electionType = x
            ec.location = request.POST.get("state")

        ec.save()

        return redirect("/electionSetting")
    else:
        return render(request, "create_election.html")


def disableElection(request):
    context = {}
    context['toDis'] = election.objects.all()

    if request.method == "POST":
        disable = request.POST.get('toBeDis')
        print(disable)
        state = request.POST.get('state')
        print(state)
        if state == '1' and disable != 'None':
            record = election.objects.get(ec_name = disable)
            record.status = "enable"
            record.save(update_fields=['status'])
            return redirect('electionHistory')
        elif state == '0' and disable != 'None':
            election.objects.filter(ec_name=disable).update(status="disable")
            return redirect('electionHistory')
        else:
            pass
        sTerm = request.POST.get('ecSearch')
        try:
            context['term'] = election.objects.filter(ec_name=sTerm)
            dell = request.POST.get('toBeDel')
            delete = request.POST.get('delete')
            if delete == "delete":
                election.objects.filter(ec_name=dell).delete()
                return redirect('electionHistory')
            return render(request,"disable_election.html", context)

        except election.DoesNotExist:
            return redirect('disableElection')

    else:
        return render(request,"disable_election.html",context)


def electionHistory(request):
    history = election.objects.all()
    print(history)
    return render(request, "election_history.html", {"hist": history})


def cResults(request):
    return render(request, "results.html")


def vResults(request):
    arguments = {}
    arguments['key'] = []
    arguments['value'] = []
    if request.user.is_authenticated:
        obj = userDetails.objects.get(email=request.user.get_username())
        q_location = obj.address
        clist = listCandidates(handle,q_location)
        print(clist)
        for i in clist:
            if i != "":
                arguments['key'].append(i)
                arguments['value'].append(countVote(handle,i))

    return render(request, "voterResults.html", {'res':arguments})


def ack(request):
    return render(request, "ack.html")

def voting(request):
    now = datetime.now().date()
    get_ec = (
        election.objects.filter(sDate=now).filter(status="enable").values("location")
    )
    loc_list = list(get_ec)
    b = []
    for i in loc_list:
        a = i["location"]
        # BC
        c = listCandidates(handle, a)  # candidatename & id
        #print(a)
        print(c)
        b = list(election.objects.filter(location=a).values("ec_name", "electionType"))
        # acc = list(Accounts.objects.values('accountAddress'))
        # accAddress = acc[0]["accountAddress"]
        obj = userDetails.objects.get(email=request.user.get_username())
        # acc = Accounts.objects.get(pk=obj.accountId)
        accAddress = obj.accountId.accountAddress
        
    cand = candidates.objects.all()

    if request.method == "POST":
        cid = request.POST.get("vote")
        #print(request.POST.get("vote"), request.POST["vote"])
        cobj = candidates.objects.get(cid=cid)
        cname = cobj.candidateName
        print(cname)
        if request.user.is_authenticated:
                #vote
                date1 = str(now)
                vote(handle,accAddress,cname,a,date1)
                print(" Vote Count for", cname ,countVote(handle,cname))
                userDetails.objects.filter(email=request.user.get_username()).update(voted=True)


                #ack
                obj = userDetails.objects.get(email=request.user.get_username())
                receiver = obj.email
                fname = obj.fName
                lname = obj.lName
                receiver_name = fname + ' ' + lname
                subject = "Swift Vote Voting Acknowledgement"
                message = f"Greetings {receiver_name}!\nYour Vote has been recorded successfully. \nThank You, \nTeam Swift Vote."
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [
                    receiver,
                ]
                send_mail(subject, message, email_from, recipient_list)
                return redirect("ack")

    return render(request, "voting.html", {"ec": b[0], "cand":cand})
