from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class AddEventForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['category'].empty_label = 'The category is not chosen'
        self.fields['location'].empty_label = 'The location is not chosen'
    
     
    class Meta:
        model = Event
        fields = ['name','poster','category','program','location','date','time','is_published']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-input'}),
            'program': forms.Textarea(attrs={'cols':80,'rows':15}),
            'date': forms.NumberInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            
        }

class AddCategoryForm(forms.ModelForm):
      
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-input'}),
            
        }

        
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-input'}))
        