from django.db import models

# Create your models here.

class WorkerDetail(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	joining_date = models.DateField(auto_now_add=True)
	basic_wage = models.IntegerField()

class MonthlyAttendance(models.Model):
	worker_id = models.ForeignKey(WorkerDetail)
	attended_days = models.IntegerField()
	overtime_hours = models.IntegerField()
	for_month = models.DateField() # need only month here

class Advance(models.Model):
	worker_id = models.ForeignKey(WorkerDetail)
	amount = models.IntegerField()
	advance_date = models.IntegerField()

class ProvidentFund(models.Model):
	worker_id = models.ForeignKey(WorkerDetail)
	pf = models.IntegerField()

class PaidSalary(models.Model):
	worker_id = models.ForeignKey(WorkerDetail)
	amount = models.IntegerField()
	payment_date = models.DateField()

class WageDescription(models.Model):
	worker_id = models.ForeignKey(WorkerDetail)
	daily_wage = models.IntegerField()
	overtime_wage = models.IntegerField()
	monthly_wage = models.IntegerField()
	monthly_payable = models.IntegerField()
	net_payable = models.IntegerField()
	for_month = models.DateField()

class Balance(models.Model):
	worker_id = models.ForeignKey(WorkerDetail)
	balance_amount = models.IntegerField()
	for_month = models.DateField()
