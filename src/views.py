from django.shortcuts import HttpResponse
from django.shortcuts import render
from src.models import *
from src.forms import *
import forms
import datetime


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
    return render(request, 'src/form.html', {'allworkers':allworkers})

def ajaxrequest(request):
    worker_id = request.GET['worker_id']
    days = request.GET['days']
   # ot = request.GET['ot']
    #date = datetime.date.today
   # obj = MonthlyAttendamce(worker_id = worker_id, ttended_days = days, overtime_hours = ot, for_month = date)
    #obj.save()
    return HttpResponse(worker_id)
