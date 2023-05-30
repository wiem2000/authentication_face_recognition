from django.forms import ModelForm
from django import forms

from useradmin_app.models import User

class user_form(ModelForm):
    mdp2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label="Confirmer le mot de passe")

    class Meta :
        model=User
        fields=['last_name','first_name','email','photo','password']
        labels={'last_name':'Nom','first_name':'Prenom','email':'E-mail personnel','password':'Mot de passe','photo':'Photo'}
        widgets={
            'last_name' : forms.TextInput(attrs={'class':'form-control '}) ,
            'first_name' : forms.TextInput(attrs={'class':'form-control '}) ,
            'email': forms.EmailInput(attrs={'class':'form-control'}), 
            'password': forms.PasswordInput(attrs={'class':'form-control '}),}
        
class user_form_without_mdp(ModelForm):
    class Meta :
        model=User
        fields=['last_name','first_name','email','photo']
        labels={'last_name':'Nom','first_name':'Prenom','email':'E-mail personnel','photo':'Photo'}
        widgets={
            'last_name' : forms.TextInput(attrs={'class':'form-control '}) ,
            'first_name' : forms.TextInput(attrs={'class':'form-control '}) ,
            'email': forms.EmailInput(attrs={'class':'form-control'}), 
           }