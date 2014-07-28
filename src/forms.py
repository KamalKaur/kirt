from django import forms
from django.forms import ModelForm
from src.models import *

class WorkerDetailForm(ModelForm):
	class Meta:
		model = WorkerDetail
		fields = '__all__'

class AdvanceForm(ModelForm):
	class Meta:
		model = Advance
		fields = '__all__'

class MonthlyAttendanceForm(ModelForm):
	class Meta:
		model = MonthlyAttendance
		fields = '__all__'

class PaidSalaryForm(ModelForm):
	class Meta:
		model = PaidSalary
		fields = '__all__'
