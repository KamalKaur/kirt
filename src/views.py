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

		if request.method == "POST":
			form2 = MonthlyAttendanceForm(request.POST)
			if form2.is_valid:
				form2.save()
		else:
			form2 = MonthlyAttendanceForm()
			

		if request.method == "POST":
			form3 = PaidSalaryForm(request.POST)
			if form3.is_valid:
				form3.save()
		else:
			form3 = PaidSalaryForm()
		return render(request,'src/form.html',{'AdvanceForm':form, 'MonthlyAttendanceForm': form2, 'PaidSalaryForm':form3})
	

"""def addworker(request):
	if request.method == "POST":
		form = WorkerDetailForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse("Submitted oye :D ")
	else:
		form = WorkerDetailForm()
		return render(request,'src/form.html', {'WorkerDetailForm':form})"""
			
"""def addadvance(request):
	if request.method == "POST":
		form = AdvanceForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse("Done!")
	else:
		return render(request,'src/form.html',{'form':AdvanceForm()})"""

"""def monthlyattendance(request):
	if request.method == "POST":
		form = MonthlyAttendanceForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse("Yay!")
	else:
		return render(request,'src/form.html',{'form':MonthlyAttendanceForm()})"""

def paidamount(request):
	if request.method == "POST":
		form = PaidSalaryForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse(":-o")
	else:
		return render(request,'src/form.html',{'form':PaidSalaryForm()})
