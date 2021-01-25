from django import forms
from holiday.models import Leave
from  django.core import validators

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        exclude = ['manager', 'employee', 'status', 'starting_date']

        widgets={
            'title': forms.TextInput(attrs={'placeholder':'enter your subject', "class":'form-control'}),
            'description': forms.Textarea(attrs={'placeholder':'description..........', "class": 'form-control'}),
            'starting_date': forms.DateInput(attrs={'type':'date', "class": 'form-control'}),
            'ending_date': forms.DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'half_day': forms.Select(attrs={'class':'form-control'}),
        }

    def clean(self):
        ending_date = self.cleaned_data['ending_date']
        half_day = self.cleaned_data['half_day'].strip(" ").lower()
        if ending_date:
            pass
        else:
            if half_day == "select":
                raise validators.ValidationError("Please Select Any One Ending Date or Half Day")
        return self.cleaned_data





