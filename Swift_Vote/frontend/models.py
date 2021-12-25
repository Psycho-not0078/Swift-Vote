# from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date

from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey

uType=(("official","Official"),("Voter","Voter"),("Candidate","Candidate"))
aType=(("official","Official"),("normie","Normie"))

class Accounts(models.Model):
    accountType=models.CharField(
        max_length = 20,
        choices = aType,
        )
    accountAddress=models.CharField(max_length=250)
    usable = models.BooleanField()
    # assigned_to = models.ForeignKey(userDetails,to_field="uid",null=True,blank=True,on_delete=models.CASCADE)

class userDetails(AbstractUser):
    uid=models.AutoField(primary_key=True)
    voted=models.BooleanField(default=False)
    email=models.EmailField("email address", unique=True)
    fName=models.CharField(max_length=30)
    lName=models.CharField(max_length=30)
    contactNumber=models.CharField(max_length=10)
    username=models.CharField(max_length=30)
    dob=models.DateField()
    # password = models.CharField(max_length=500,null=True)
    documentLocation=models.CharField(max_length=500,null=True,blank=True)
    # password=models.TextField()
    # Address=models.TextField()
    address = models.CharField(max_length=250)
    type=models.CharField(
        max_length = 20,
        choices = uType,
        )
    accountId = models.ForeignKey(Accounts,on_delete=models.CASCADE, null=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['fname','lname','contactNumber','username','dob',"documentLocation"]
    # EMAIL_FIELD='email'
    # def __str__(self):
    #     return "{}".format(self.email)

class candidates(models.Model):
    cid=models.AutoField(primary_key=True)
    candidateName=models.CharField(max_length=120)
    cDob=models.DateField()
    cState=models.CharField(max_length=240)
    cCity=models.CharField(max_length=240)
    electionType=models.CharField(max_length=120)
    uid=models.IntegerField()
    # uid=models.ForeignKey(userDetails,on_delete=models.CASCADE, default=1)
    party=models.CharField(max_length=60)


class location(models.Model):
    lid=models.AutoField(primary_key=True)
    context=models.CharField(max_length=20)
    locationName=models.CharField(max_length=500)
    locationVoteCount=models.BigIntegerField(default=0)

class election(models.Model):
    eid=models.AutoField(primary_key=True)
    ec_name=models.CharField(max_length=200)
    electionType=models.CharField(max_length=250)
    allowedContext=models.CharField(max_length=250)
    voteCount=models.BigIntegerField(default=0)
    sDate=models.DateField()
    fDate=models.DateField()
    location=models.CharField(max_length=250)
    inCharge=models.ForeignKey(userDetails,null=True,blank=True,to_field="uid",on_delete=models.CASCADE)
    status=models.CharField(max_length=7, default='enable')

class candidateHistory(models.Model):
    hid=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(candidates,on_delete=models.CASCADE,to_field="cid")
    
    election=models.ForeignKey(election,on_delete=models.CASCADE,to_field="eid")
    voteCount=models.BigIntegerField()

class userVerification(models.Model):
    vid=models.AutoField(primary_key=True)
    uid=models.ForeignKey(candidates,on_delete=models.CASCADE,to_field="cid")
    documentType=models.CharField(max_length=50)
    documentName=models.CharField(max_length=50)
    Status=models.BooleanField()

class Vote(models.Model):
    uid=models.ForeignKey(userDetails,on_delete=models.CASCADE,to_field="uid")
    eid=models.ForeignKey(election,on_delete=models.CASCADE,to_field="eid")
