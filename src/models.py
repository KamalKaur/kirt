from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
import datetime

# This error not yet shown
alphabets = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabets and spaces are allowed.')

class WorkerDetail(models.Model):
    first_name = models.CharField(max_length=100, validators=[alphabets])
    last_name = models.CharField(max_length=100, validators=[alphabets])
    address = models.CharField(max_length=200)
    joining_date = models.DateField(default=datetime.date.today)
    basic_wage = models.FloatField()
    provident_fund = models.FloatField()
    status = models.BooleanField(default=True)
    resigning_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.first_name

class MonthlyAttendance(models.Model):
    worker_id = models.ForeignKey(WorkerDetail)
    attended_days = models.FloatField(null=True, blank=True) # Value not more than 31?
    overtime_hours = models.FloatField(null=True, blank=True)
    for_month = models.DateField(default=datetime.date.today)

class Advance(models.Model):
    worker_id = models.ForeignKey(WorkerDetail)
    advance_amount = models.FloatField()
    advance_date = models.DateField(default=datetime.date.today)

class PaidSalary(models.Model):
    worker_id = models.ForeignKey(WorkerDetail)
    paid_amount = models.FloatField(null=True, blank=True)
    payment_date = models.DateField(default=datetime.date.today)

class WageDescription(models.Model): # Is this model needed? 
    worker_id = models.ForeignKey(WorkerDetail)
    daily_wage = models.FloatField()
    overtime_wage = models.FloatField()
    monthly_wage = models.FloatField()
    monthly_payable = models.FloatField()
    net_payable = models.FloatField()
    for_month = models.DateField()

class Balance(models.Model): # Why not calculate only when asked?
    worker_id = models.ForeignKey(WorkerDetail)
    balance_amount = models.FloatField()
    for_month = models.DateField(default=datetime.date.today)
