from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms import ModelForm


#Sign up form
class addUserForm(ModelForm):
	username = forms.CharField(label=False, widget = forms.TextInput(attrs = {'placeholder': 'Username', 'class': 'fadeIn first'}) )
	email = forms.CharField(label=False, widget = forms.TextInput(attrs = {'placeholder': 'Email', 'class': 'fadeIn second'}) )
	password = forms.CharField(label=False, widget = forms.PasswordInput(attrs = {'placeholder': 'Password', 'class': 'fadeIn third'}) )
	confirm_password= forms.CharField(label=False, widget=forms.PasswordInput(attrs = {'placeholder': 'Confirm Password','class': 'fadeIn fourth'}))
	class Meta:
		model = User
		fields = ['username','email', 'password',]

	def clean(self):
		cleaned_data = super(addUserForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")

		if password != confirm_password:
			raise forms.ValidationError(
				"password and confirm_password does not match"
			)

#add expenses form
class addExpenseForm(ModelForm):
	value = forms.IntegerField(label=True, widget = forms.TextInput(attrs={'placeholder': 'Enter amount of expense'}))
	#vat = forms.IntegerField(label=False, widget = forms.NumberInput(attrs = {'placeholder': 'VAT', 'class': 'fadeIn vat second', 'readonly':'readonly'}) )
	reason = forms.CharField(label=False, widget = forms.TextInput(attrs = {'placeholder': 'Enter reason of expense', 'class': 'fadeIn third'}) )
	date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder':'Enter date of expense'}))
	class Meta:
		model = expense
		widgets = {
            'date': forms.DateInput(attrs={'class':'datepicker'}),
        }
		fields = ['value','vat','reason','date']
