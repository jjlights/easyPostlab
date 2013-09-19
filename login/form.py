# Create your views here.
from django import forms

class LoginField(forms.Form):
    username = forms.CharField(label=(u'User Name'),max_length=64,required=True,widget=forms.TextInput(attrs={'class':'profile textfield'}))
    password = forms.CharField(label=(u'Password'),max_length=64,required=True,widget=forms.PasswordInput(render_value=False))

