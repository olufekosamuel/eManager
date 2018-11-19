from django.shortcuts import render, redirect
from .forms import addUserForm, addExpenseForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import expense
import re, json
import requests


# home index page. login required here
@login_required
def index(request):
	expenses = expense.objects.filter(user=request.user)
	return render(request, 'index.html', {'expenses':expenses})


#fucntion to register new users
def signup(request):
	if(request.method == "POST"):
		form = addUserForm(request.POST)
		if form.is_valid():
			
			user = form.save(commit=False)
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
		
			user.password = make_password(password)
			user.save()
			messages.success(request, 'Congratulations! you successfully registered, you may login to start using Expense manager.' )
			return redirect('login')
		else:
			form = addUserForm()
	else:
		form = addUserForm()
	return render(request, 'registration/signup.html', {'form': form})

#function to user logout
def log_out(request):
	logout(request)
	messages.success(request, 'Thank you for using Expense manager today.' )
	return redirect('login')

#function to add user's expenses, login is also required here
@login_required
def add_expense(request):
	form = addExpenseForm
	if(request.method == "POST"):
		reason = request.POST['reason']
		date = request.POST['date']
		value = request.POST['value']
		value = re.sub('[^0-9]','', value)
		poundsvalue = currency_converter(value)

		if poundsvalue is None:
			messages.error(request, 'An error occured while trying to submit expenses, please try again.')
			return redirect('emanager:add_expense')
		vat = float(poundsvalue) * 0.2
		expenseobj = expense.objects.create(user=request.user,value=value,reason=reason,vat=vat,date=date)
		expenseobj.save()
		messages.success(request, 'Expense saved successfully with Expense manager' )
		return redirect('emanager:index')
	else:
		form = addExpenseForm
	return render(request, 'addexpense.html', {'form':form})


#Fuction to handle realtime currency rate
def currency_converter(amount): 
	url = 'https://free.currencyconverterapi.com/api/v6/convert?q=EUR_GBP&compact=ultra'
	#try and ctach to handle errors
	try:
		r = requests.get(url)
	except requests.exceptions.RequestException as e:  # This is the correct syntax
		return None
	rate = r.json()
	rate = rate['EUR_GBP']

	conversion = float(rate) * float(amount)
	return amount
