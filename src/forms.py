from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from src.models import *
import datetime

class WorkerDetailForm(ModelForm):
     # first_name = forms.CharField(label='')
     # last_name = forms.CharField(label='')
     # address = forms.CharField(label='') 
     # joining_date = forms.DateField(label='') 
     # basic_wage = forms.IntegerField(label='') 
     # provident_fund = forms.IntegerField(label='') 
	 # Labels names are needed here, so fields are not defined separately.
    
     class Meta:
        model = WorkerDetail
        fields = '__all__'
        error_messages = {'first_name': {'max_length': ("Give proper length"),},}

class AdvanceForm(ModelForm):
    worker_id = forms.ModelChoiceField(WorkerDetail.objects.all(),label ='')
    advance_amount = forms.IntegerField(label='', widget=forms.TextInput(attrs={'onchange':'save_advance();'}))
    # advance_date = forms.DateField(label='',initial=datetime.date.today)
    # Date field with default date in form can be added like this ^
    
    class Meta:
        model = Advance
        # exclude = ('advance_date',) 
		# Excluding the date field but it automatically saves today's date :)
        # fields = ('worker_id', 'advance_amount')
		# The above line takes the field behaviour directly from models but how to ignore labels?
        labels = {'advance_date': (''),}

class MonthlyAttendanceForm(ModelForm):
    attended_days = forms.IntegerField(label='')
    overtime_hours = forms.IntegerField(label='')

    class Meta:
        model = MonthlyAttendance
        exclude = ('worker_id','for_month')

class PaidSalaryForm(ModelForm):
    # paid_amount = forms.IntegerField(label='')
    class Meta:
        model = PaidSalary
        labels = {'paid_amount': (''),}
        exclude = ('worker_id','payment_date',)
