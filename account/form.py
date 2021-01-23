from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    # username = forms.CharField(validators=[validator.username],widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password', 'class' : 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Enter confirm password', 'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter you first name', 'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter you last name', 'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name']

        # widgets={
        #     'name': forms.TextInput(attrs={'placeholder':'Enter name',"class":'form-control'}),
        #
        # }

#     def clean(self):
#         password = self.cleaned_data.get('password')
#         confirm_password = self.cleaned_data.get('confirm_password')
#         print('rakesh',password,confirm_password)
#         if password==confirm_password:
#             if not len(password)>=6:
#                 raise validators.ValidationError('Password length is less then 6')
#             return self.cleaned_data
#         else:
#             raise validators.ValidationError('Password and confirm_password does not match')
#
class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password', 'class':'form-control'}))
#
# class customerForm(forms.ModelForm):
#     class Meta:
#         model = MyProfile
#         fields = "__all__"
#         exclude = ['user']