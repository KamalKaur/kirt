from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render
from src.models import *
from src.forms import *
import forms


# Create your views here.

def index(request):
	if not WorkerDetail.objects.all():
		if request.method == "POST":
			form = WorkerDetailForm(request.POST)
			if form.is_valid:
				form.save()
				return HttpResponse("Done! Done!")
		else:
			form = WorkerDetailForm()
			return render(request,'src/addworker.html',{'WorkerDetailForm':form})
	else:
		if request.method == "POST":
			form = AdvanceForm(request.POST)
			if form.is_valid:
				form.save()
		else:
			form = AdvanceForm()
			return render(request,'src/form.html',{'AdvanceForm':form})	


	

def addworker(request):
	if request.method == "POST":
		form = WorkerDetailForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse("Submitted oye :D ")
	else:
		form = WorkerDetailForm()
		return render(request,'src/form.html', {'WorkerDetailForm':form})
			
def addadvance(request):
	if request.method == "POST":
		form = AdvanceForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse("Done!")
	else:
		return render(request,'src/form.html',{'form':AdvanceForm()})

def monthlyattendance(request):
	if request.method == "POST":
		form = MonthlyAttendanceForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse("Yay!")
	else:
		return render(request,'src/form.html',{'form':MonthlyAttendanceForm()})

def paidamount(request):
	if request.method == "POST":
		form = PaidSalaryForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse(":-o")
	else:
		return render(request,'src/form.html',{'form':PaidSalaryForm()})
