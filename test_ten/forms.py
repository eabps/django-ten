from django import forms

from . models import Tenant, Patient, ScheduledService


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=43, label='Username')
    first_name = forms.CharField(max_length=32, label='First Name')
    last_name = forms.CharField(max_length=64, label='Last Name')
    email = forms.EmailField(max_length=64, label='E-mail')
    password = forms.CharField(max_length=16, widget=forms.PasswordInput())


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name']


class ScheduledServiceForm(forms.ModelForm):
    class Meta:
        model = ScheduledService
        fields = ['patient', 'date']
    
    def __init__(self, *args, **kwargs):
        super(ScheduledServiceForm, self).__init__(*args, **kwargs)
        from . models import Patient
        self.fields['patient'].queryset = Patient.objects.all()
