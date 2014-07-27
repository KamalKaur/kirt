from django import forms
from django.forms import ModelForm
from src.models import *

class WorkerDetailForm(ModelForm):
	class Meta:
		model = WorkerDetail

class AdvanceForm(ModelForm):
	class Meta:
		model = Advance

class MonthlyAttendanceForm(ModelForm):
	class Meta:
		model = MonthlyAttendance
