from django import forms
from holiday.models import Leave, Resions
from django.core import validators
from django.shortcuts import redirect

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        exclude = ['manager','employee', 'status']

        widgets={
            'title': forms.TextInput(attrs={'placeholder': 'enter your subject', "class":'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'description..........', "class": 'form-control'}),
            'starting_date': forms.DateInput(attrs={'type': 'date', "class": 'form-control'}),
            'ending_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'half_day': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        ending_date = self.cleaned_data['ending_date']
        half_day = self.cleaned_data['half_day'].strip(" ").lower()
        print('half', half_day,ending_date)
        if ending_date:
            print('in side of end date')
        else:
            print('out sido of end')
        if half_day=="first_half" or half_day=="second_half":
            if ending_date:
                raise validators.ValidationError("You can select only either an end date or days ")
        else:
            if half_day == "select" and ending_date==None:
                raise validators.ValidationError("Please Select Any One Ending Date or Half Day")
        return self.cleaned_data

# class ApprovedForm(forms.ModelForm):
#     class Meta:
#         model = Leave
#         fields = ('status',)
#
#         widgets = {
#             'status': forms.Select(attrs={'class': 'form-control'}),
#         }

    # def clean(self):
    #     status = self.cleaned_data['status'].strip(" ").lower()
    #     if status == 'resion':
    #         print('status', status)
    #         # return redi
    #     return self.cleaned_data

class ResionForm(forms.ModelForm):
    class Meta:
        model = Resions
        fields = "__all__"
        exclude = ['employee', 'leave']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'enter your subject', "class": 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'description..........', "class": 'form-control'}),
        }



