from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from src.models import *
from src.forms import *
import forms

# Create your views here.

def index(request):
	return render_to_response('src/index.html')

def addworker(request):
	form = WorkerDetailForm()
	return render_to_response('src/addworker.html', {'WorkerDetailForm': form})
