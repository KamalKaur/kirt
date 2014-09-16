from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse
from django.shortcuts import render
from src.models import *
from src.forms import *
import forms
import ajax_views
import datetime
from django.db.models import Sum
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

def addadvance(request):
    if request.method == 'POST':
        form = AdvanceForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse("Done! Done!")
    else:
        form = AdvanceForm()
    return render(request,'src/addadvance.html',{'AdvanceForm':form})

def ajaxdetails(request):
    allworkers = WorkerDetail.objects.values('id').all()
    detail_list = []
    for value in allworkers:
        worker_dict = {}
        details = WorkerDetail.objects.values('first_name', 'last_name', 'address').filter(id = value['id'])
        attendance = MonthlyAttendance.objects.values('attended_days').filter(worker_id = value['id']).filter(for_month__month=today.month)
        overtime = MonthlyAttendance.objects.values('overtime_hours').filter(worker_id = value['id']).filter(for_month__month=today.month)
        paid_salary = PaidSalary.objects.values('paid_amount').filter(worker_id = value['id']).filter(payment_date__month=today.month)
        advance = Advance.objects.filter(worker_id = value['id']).filter(advance_date__month=today.month).aggregate(Sum('advance_amount'))
        worker_dict['worker_id'] = value['id']
        for item in details:
            worker_dict['first_name'] = item['first_name']
            worker_dict['last_name'] = item['last_name']
            worker_dict['address'] = item['address']
        for item in attendance:
            worker_dict['attendance'] = item['attended_days']
        for item in overtime:
            worker_dict['overtime '] = item['overtime_hours']
        for item in paid_salary:
            worker_dict['paid_salary'] = item['paid_amount']
        worker_dict['advance_amount'] = advance['advance_amount__sum']
        detail_list.append(worker_dict)

    return render(request, 'src/form.html', {'detail_list':detail_list})

