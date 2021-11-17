from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date

from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey

uType=(("official","Official"),("Voter","Voter"),("Candidate","Candidate"))
aType=(("official","Official"),("Normie","Normie"))
class userDetails(AbstractUser):
    uid=models.AutoField(primary_key=True)
    email=models.EmailField(_("email_address"))
    fName=models.CharField(max_length=30)
    lName=models.CharField(max_length=30)
    contactNumber=models.CharField(max_length=10)
    username=models.CharField(max_length=30)
    DOB=models.DateField()
    documentLocation=models.CharField(max_length=500,null=True,blank=True)
    # password=models.TextField()
    Address=models.TextField()
    type=models.CharField(
        max_length = 20,
        choices = uType,
        )
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['Fname','Lname','contactNumber','username','email','DOB',"documentLocation"]
    EMAIL_FIELD='email'

class candidates(models.Model):
    cid=models.AutoField(primary_key=True)
    uid=models.ForeignKey(userDetails,on_delete=models.CASCADE)
    party=models.CharField(primary_key=True)

class Accounts(models.Model):
    aid=models.AutoField(primary_key=True)
    accountType=models.CharField(
        max_length = 20,
        choices = aType,
        )
    accountString=models.CharField(max_length=250)
    accountPrivate=models.TextField()
    accountPublic=models.TextField()
    assigned_to = models.ForeignKey(userDetails,to_field="uid",null=True,blank=True)

class location(models.Model):
    lid=models.AutoField(primary_key=True)
    context=models.CharField(max_length=20)
    locationName=models.CharField(max_length=500)
    locationVoteCount=models.BigIntegerField()

class election(models.Model):
    eid=models.AutoField(primary_key=True)
    electionType=models.CharField(max_length=250)
    allowedContext=models.CharField(max_length=250)
    voteCount=models.BigIntegerField()
    sDate=models.DateTimeField()
    fDate=models.DateTimeField()
    inCharge=models.ForeignKey(userDetails,null=True,blank=True,to_field="uid")

class candidateHistory(models.Model):
    hid=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(candidates,on_delete=models.CASCADE,to_field="cid")
    election=models.ForeignKey(election,on_delete=models.CASCADE,to_field="eid")
    voteCount=models.BigIntegerField()

class userVerification(models.Model):
    vid=models.AutoField(primary_key=True)
    uid=models.models.ForeignKey(candidates,on_delete=models.CASCADE,to_field="cid")
    documentType=models.CharField(max_length=50)
    documentName=models.CharField(max_length=50)
    Status=models.BooleanField()

class Vote(models.Model):
    uid=models.ForeignKey(userDetails,on_delete=models.CASCADE,to_field="uid")
    eid=models.ForeignKey(election,on_delete=models.CASCADE,to_field="eid")

    
