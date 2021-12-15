from django import forms
from .models import userDetails
class UserForm(forms.ModelForm):
    pass
    # class Meta:  
    #     model = userDetails
    #     fields = ['fName','lName','username','email','contactNumber','dob','Address']