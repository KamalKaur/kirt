from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render
from src.models import *
from src.forms import *
import forms


# Create your views here.

def index(request):
	return render(request,'src/index.html',{})

def addworker(request):
	if request.method == "POST":
		form = WorkerDetailForm(request.POST)
		if form.is_valid:
			form.save()
			return HttpResponse("Submitted oye :D ")
	else:
		form = WorkerDetailForm()
		return render(request,'src/addworker.html', {'WorkerDetailForm': form})
			
	
