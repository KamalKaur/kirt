from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse
from django.shortcuts import render
from src.models import *
from src.forms import *
import forms
import datetime

today = datetime.date.today()
# Create your views here.

def index(request):
    return render(request, 'src/index.html', {})

def adddetails(request):
    allworkers = WorkerDetail.objects.all()
    if request.method == "POST":
        aform = AdvanceForm(request.POST, prefix ='one')
        mform = MonthlyAttendanceForm(request.POST, prefix ='two')
        pform = PaidSalaryForm(request.POST, prefix ='three')
        a_valid = aform.is_valid()
        m_valid = mform.is_valid()
        p_valid = pform.is_valid()
        if a_valid and m_valid and p_valid:
            object_one = aform.save()
            object_two = mform.save(commit=False)
            object_two.worker_id = object_one.worker_id
            object_two.save()
            object_three = pform.save(commit=False) # What if already saved?
            object_three.worker_id = object_one.worker_id
            object_three.save()
            return HttpResponse("Done! Done!")
    else:
        aform = AdvanceForm(prefix='one')
        mform = MonthlyAttendanceForm(prefix='two')
        pform = PaidSalaryForm(prefix='three')
        return render(request,'src/details.html', {'AdvanceForm':aform, 'MonthlyAttendanceForm':mform, \
                'PaidSalaryForm':pform, 'allworkers':allworkers})

def addworker(request):
    if request.method == 'POST':
        form = WorkerDetailForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse("Done! Done!")
    else:
        form = WorkerDetailForm()
    return render(request,'src/addworker.html',{'WorkerDetailForm':form})

def ajaxdetails(request):
    allworkers = WorkerDetail.objects.all()
    paid_salaries = PaidSalary.objects.all().values('worker_id','worker_id_id__first_name', 'worker_id_id__address','worker_id_id__id')
    return render(request, 'src/form.html', {'allworkers':allworkers, 'paid_salaries':paid_salaries})

# Ajax calls the following views

def ajaxrequest(request):
    try:
       worker_id = request.GET['worker_id']
       days = request.GET['days']
       goo = 123
    except:
       goo = 345
    # overtime = request.GET['overtime']
    # date = datetime.date.today
    #  obj = MonthlyAttendamce(worker_id = worker_id, ttended_days = days, overtime_hours = ot, for_month = date)
    # obj.save()
    return HttpResponse(goo)

def ajaxrequestpaid(request):
    worker_id = request.GET['worker_id']
    paid = request.GET['paid']
    worker = WorkerDetail.objects.get(pk=worker_id) # Fetches the instance of this id from WorkerDetail
    if PaidSalary.objects.filter(worker_id_id=worker_id).exists():
        editable = PaidSalary.objects.get(worker_id_id=worker_id, payment_date__month=today.month) # If the edited object's worker id and this month's value exists
      #  date_filter = PaidSalary.objects.filter(date_year='', date-month='')
      #  for field in editable instance
        editable.paid_amount = paid
        editable.date = today
        editable.save()
        return HttpResponse('')
    else:
        obj = PaidSalary(worker_id = worker, paid_amount = paid, payment_date = today) # date is defined there in the beginning of this file
        obj.save()
    #allw = PaidSalary.objects.all()
        return HttpResponse(worker_id)   

def ajaxrequestadvance(request):
    worker_id = request.GET["worker_id"]
#   advance = request.GET["advance"]
#    worker = WorkerDetail.objects.get(pk=worker_id) # It can be used throughout the file
    return HttpResponse(worker_id)
