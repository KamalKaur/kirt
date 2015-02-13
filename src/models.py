from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator   
from django.db import models
import datetime

# This error not yet shown
alphabets = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabets and spaces are allowed.')

class WorkerDetail(models.Model):
    """
    This model keeps all the details of workers at one place. And is 
    updated with a new record after the user submits "Add worker" form.
    All the fields are mendatory. The joining_date is kept default for 
    the ease of user. WHen a new worker is added, the status is by default
    added as true which signifies that the worker is currently working in 
    the organisation. When a worker gets deleted, it changes to false
    and the queries are used this way to show only the workers who are
    currently working. 
    """
    first_name = models.CharField(max_length=100, validators=[alphabets])
    middle_name = models.CharField(max_length=100, validators=[alphabets], null=True, blank=True)
    last_name = models.CharField(max_length=100, validators=[alphabets])
    address = models.CharField(max_length=200)
    joining_date = models.DateField(default=datetime.date.today)
    basic_wage = models.FloatField(validators = [MinValueValidator(0)])
    provident_fund = models.FloatField(validators = [MinValueValidator(0)], null=True, blank=True, default=0)
    status = models.BooleanField(default=True)
    resigning_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.first_name

class Promotions(models.Model):
    """
    Here, we store the promotions of worker salaries which are done from 
    time to time. The date field helps to keep the track of date, time
    and year of the same action.
    """
    worker_id = models.ForeignKey(WorkerDetail)
    promoted_wage = models.FloatField(validators = [MinValueValidator(0)])
    on_date = models.DateField(default=datetime.date.today)

class MonthlyAttendance(models.Model):
    """
    This model keeps the attendance of all the workers and is accessed 
    anytime the salarysheet is accessed or searched backward. 
    """
    worker_id = models.ForeignKey(WorkerDetail)
    attended_days = models.FloatField(null=True, blank=True, validators = [MinValueValidator(0)]) # Value not more than 31?
    overtime_hours = models.FloatField(null=True, blank=True)
    for_month = models.DateField(default=datetime.date.today)

class DailyAttendance(models.Model):
    """
    This tabel is used to store worker attendance on daily basis
    """
    worker_id = models.ForeignKey(WorkerDetail)
    attendance = models.FloatField(null=True, blank=True)
    overtime = models.FloatField(null=True, blank=True)
    for_day = models.DateField(default=datetime.date.today)
    
class Advance(models.Model):
    """
    The advance values, which are to be entered for any worker or for any month
    are stored here. It is updated when a new advance value is added
    and is accessed when the salarysheet is dislayed.
    """
    worker_id = models.ForeignKey(WorkerDetail)
    advance_amount = models.FloatField()
    advance_date = models.DateField(default=datetime.date.today)

class PaidSalary(models.Model):
    """
    This model stores the paid salaries for all workers along with
    date which tells about the paid salary for a particular month
    for a particular worker. 
    """   
    worker_id = models.ForeignKey(WorkerDetail)
    paid_amount = models.FloatField(null=True, blank=True)
    payment_date = models.DateField(default=datetime.date.today)

class WageDescription(models.Model): 
    """
    This model was added initially to store the wage description
    for workers for particular months. But its not in use as 
    the purpose is served by run time calculations and else every entry
    will also be updated here and it will increase the response time
    which is not required.
    """
#   worker_id = models.ForeignKey(WorkerDetail)
#   daily_wage = models.FloatField()
#   monthly_wage = models.FloatField()
#   monthly_payable = models.FloatField()
#   net_payable = models.FloatField()

    worker_id = models.ForeignKey(WorkerDetail)
    monthly_basic_wage = models.FloatField()
    overtime_wage = models.FloatField()
    monthly_wage = models.FloatField()
    amount_to_be_paid = models.FloatField()
    paid_amount = models.FloatField()
    for_month = models.DateField()

class Balance(models.Model):
    """
    This model is used to store balance amount left for any worker
    after a salary is paid. This is updated whenever a Pay Slip page 
    is accessed and the values for previous balance are taken into 
    account in next month automatically.
    """
    worker_id = models.ForeignKey(WorkerDetail)
    balance_amount = models.FloatField()
    for_month = models.DateField(default=datetime.date.today)
