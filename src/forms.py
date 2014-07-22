from django import forms
from django.forms import ModelForm
from src.models import *

class WorkerDetailForm(ModelForm):
	class Meta:
		model = WorkerDetail
		fields = '__all__'
		
		#joining_date not there
