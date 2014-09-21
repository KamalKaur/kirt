from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
import datetime

# Create your models here.

# This error not yet shown
alphabets = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabets are allowed.')

class WorkerDetail(models.Model):
    first_name = models.CharField(max_length=100, validators=[alphabets])
    last_name = models.CharField(max_length=100, validators=[alphabets])
    address = models.CharField(max_length=200)
    joining_date = models.DateField(default=datetime.date.today)
    basic_wage = models.IntegerField()
    provident_fund = models.IntegerField()
    def __unicode__(self):
        return self.first_name

class MonthlyAttendance(models.Model):
    worker_id = models.ForeignKey(WorkerDetail)
    attended_days = models.IntegerField() # Value not more than 31?
    overtime_hours = models.IntegerField(max_length=3) 
    for_month = models.DateField(default=datetime.date.today)

class Advance(models.Model):
    worker_id = models.ForeignKey(WorkerDetail)
    advance_amount = models.IntegerField()
    advance_date = models.DateField(default=datetime.date.today)

class PaidSalary(models.Model):
    worker_id = models.ForeignKey(WorkerDetail)
    paid_amount = models.IntegerField()
    payment_date = models.DateField(default=datetime.date.today)

class WageDescription(models.Model): # Is this model needed? 
    worker_id = models.ForeignKey(WorkerDetail)
    daily_wage = models.IntegerField()
    overtime_wage = models.IntegerField()
    monthly_wage = models.IntegerField()
    monthly_payable = models.IntegerField()
    net_payable = models.IntegerField()
    for_month = models.DateField()

class Balance(models.Model): # Why not calculate only when asked?
    worker_id = models.ForeignKey(WorkerDetail)
    balance_amount = models.IntegerField()
    for_month = models.DateField()
