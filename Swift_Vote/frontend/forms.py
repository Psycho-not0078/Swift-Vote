from django import forms
from .models import userDetails
class UserForm(forms.ModelForm):
    class Meta:  
        model = userDetails
        fields = "__all__"  
        exclude = ['uid','type','documentLocation']