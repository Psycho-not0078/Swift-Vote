from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date

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
    documentLocation=models.CharField(max_length=500)
    # password=models.TextField()
    Address=models.TextField()
    type=models.CharField(
        max_length = 20,
        choices = uType,
        )
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['Fname','Lname','contactNumber','username','email','DOB',"documentLocation"]
    EMAIL_FIELD='email'


class Accounts(models.Model):
    aid=models.IntegerField(primary_key=True)
    accountType=models.CharField(
        max_length = 20,
        choices = aType,
        )
    accountString=models.CharField(max_length=250)
    accountPrivate=models.TextField()
    accountPublic=models.TextField()
    assigned_to = models.ForeignKey(userDetails,to_field="uid",null=True,blank=True)

    
