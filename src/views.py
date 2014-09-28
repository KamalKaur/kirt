from __future__ import division
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.shortcuts import render
from src.models import *
from src.forms import *
import forms
import datetime
from django.db.models import Sum
from calendar import monthrange



this_month = datetime.date.today().month
this_year = datetime.date.today().year
# Create your views here.

@login_required
def index(request):
    return render(request, 'src/index.html', {})

@login_required
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

@login_required
def addworker(request):
    if request.method == 'POST':
        form = WorkerDetailForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse("Done! Done!")
    else:
        form = WorkerDetailForm()
    return render(request,'src/addworker.html',{'WorkerDetailForm':form})

@login_required
def addadvance(request):
    if request.method == 'POST':
        form = AdvanceForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse("Done! Done!")
    else:
        form = AdvanceForm()
    return render(request,'src/addadvance.html',{'AdvanceForm':form})

@login_required
def ajaxdetails(request):
    allworkers = WorkerDetail.objects.values('id').all()
    detail_list = []
    editable = 0
    # If the search form posts some data, then get the year and month from 
    # posted data, else take values for today's year and month and pass in for
    # loop.
    if request.method == 'POST':
       search_form = SearchSelect(request.POST)
       if search_form.is_valid():
           year = search_form.cleaned_data['year']
           month = search_form.cleaned_data['month']
    else:
        year = this_year
        month = this_month
        search_form = SearchSelect()
     
    #
    if year == this_year:
        editable = 1
    
    for value in allworkers:
        worker_dict = {}

        details = WorkerDetail.objects.values('first_name', 'last_name',
        'address').filter(id = value['id'])
	
        attendance = MonthlyAttendance.objects.values('attended_days').\
        filter(worker_id = value['id']).filter(for_month__year=
        year).filter(for_month__month=month)

        overtime = MonthlyAttendance.objects.values('overtime_hours').\
        filter(worker_id = value['id']).filter(for_month__year=
        year).filter(for_month__month=month)

        paid_salary = PaidSalary.objects.values('paid_amount').\
        filter(worker_id = value['id']).filter(payment_date__year=
        year).filter(payment_date__month=month)
        
        advance = Advance.objects.filter(worker_id = value['id']).\
        filter(advance_date__year=year).filter(advance_date__month= 
        month).aggregate(Sum('advance_amount'))

        worker_dict['worker_id'] = value['id']
        for item in details:
            worker_dict['first_name'] = item['first_name']
            worker_dict['last_name'] = item['last_name']
            worker_dict['address'] = item['address']
        for item in attendance:
            worker_dict['attendance'] = item['attended_days']
        for item in overtime:
            worker_dict['overtime'] = item['overtime_hours']

        for item in paid_salary:
            worker_dict['paid_salary'] = item['paid_amount']
        worker_dict['advance_amount'] = advance['advance_amount__sum']
        detail_list.append(worker_dict)

    return render(request, 'src/form.html', {'detail_list':detail_list,\
    'search':search_form, 'editable':editable})

# Ajax calls the following views

@login_required
def ajaxrequest(request):
    try:
       worker_id = request.GET['worker_id']
       days = request.GET['days']
       goo = 123
    except:
       goo = 345
    # overtime = request.GET['overtime']
    # date = datetime.date.today
    #  obj = MonthlyAttendamce(worker_id = worker_id, attended_days = days, overtime_hours = ot, for_month = date)
    # obj.save()
    return HttpResponse(goo)

@login_required
def ajaxrequestpaid(request):
    worker_id = request.GET['worker_id']
    paid = request.GET['paid']
    worker = WorkerDetail.objects.get(pk=worker_id) # To get the instance but not the id
    if PaidSalary.objects.filter(worker_id_id=worker_id, payment_date__month=this_month).exists():
        editable = PaidSalary.objects.get(worker_id_id=worker_id,\
        payment_date__month=this_month) # If the edited object's worker id and this month's value exists
        # date_filter = PaidSalary.objects.filter(date_year='', date-month='')
        # for field in editable instance
        editable.paid_amount = paid
        editable.payment_date = datetime.date.today()
        editable.save()
        return HttpResponse('') # Field is not refreshed
    else:
        obj = PaidSalary(worker_id = worker, paid_amount = paid,\
        payment_date = datetime.date.today()) 
        obj.save()
        #allw = PaidSalary.obj1ects.all()
        return HttpResponse(worker_id)   

@login_required
def popupadvance(request):
    worker_id = request.GET["worker_id"]
    old_advances = Advance.objects.filter(worker_id = worker_id).\
    filter(advance_date__month=this_month).filter(advance_date__year=this_year)
    # advance = request.GET["advance"]
    # worker = WorkerDetail.objects.get(pk=worker_id) # It can be used throughout the file
    return render(request,'src/popup_addadvance.html',\
    {'worker_id':worker_id, 'old_advances':old_advances})

@login_required
def ajaxpopupadvance(request):
    worker_id = request.GET["worker_id"]
    # Advance.worker_id must be a WorkerDetail instance :P
    worker = WorkerDetail.objects.get(pk=worker_id) 
    popupadvance = request.GET['popupadvance']
    obj = Advance(worker_id=worker, advance_amount=popupadvance,\
    advance_date=datetime.date.today())
    obj.save()
    return HttpResponse("yo! :D ")

@login_required
def particulars(request):
    
    # Yet only for this month
    # "worker_id =" or "worker-id_id"?
    worker_id = request.GET['worker_id']
    
    basic_wage = WorkerDetail.objects.values('basic_wage').\
    filter(id=worker_id)[0]['basic_wage']
    attended_days = MonthlyAttendance.objects.values('attended_days').\
    filter(worker_id=worker_id).filter(for_month__month=this_month).\
    filter(for_month__year=this_year)[0]['attended_days']
    #return HttpResponse(basic_wage)
    days_in_month = monthrange(this_year, this_month)[1]		
    monthly_basic_wage = ((basic_wage / days_in_month) * attended_days)	
    # return HttpResponse(monthly_basic_wage)
    overtime_hours = MonthlyAttendance.objects.values('overtime_hours').\
    filter(worker_id=worker_id).filter(for_month__month=this_month).\
    filter(for_month__year=this_year)[0]['overtime_hours']
    #return HttpResponse(overtime_hours)
    overtime_wage = (basic_wage / days_in_month) / 6 * overtime_hours
    total = monthly_basic_wage + overtime_wage
    # return HttpResponse(total)
    last_month_advance = Balance.objects.values('balance_amount').\
    filter(worker_id = worker_id).filter(for_month__month=this_month-1).\
    filter(for_month__year=this_year)[0]['balance_amount']
    # return HttpResponse(last_month_advance)
    this_month_advance = Advance.objects.filter(worker_id = worker_id ).\
    filter(advance_date__year=this_year).filter(advance_date__month=\
    this_month).aggregate(Sum('advance_amount'))['advance_amount__sum']
    # return HttpResponse(this_month_advance)
    monthly_wage = total - this_month_advance 
    # return HttpResponse(monthly_wage)
    grand_total = monthly_wage - last_month_advance
    # return HttpResponse(grand_total)
    provident_fund = WorkerDetail.objects.values('provident_fund').\
    filter(id=worker_id)[0]['provident_fund']
    amount_to_be_paid = grand_total - provident_fund
    # return HttpResponse(amount_to_be_paid)
    paid_amount = PaidSalary.objects.values('paid_amount'). \
    filter(worker_id=worker_id)[0]['paid_amount']
    # return HttpResponse(paid_amount)
    further_advance = amount_to_be_paid - paid_amount
    worker = WorkerDetail.objects.get(pk=worker_id)
    if Balance.objects.filter(worker_id=worker_id, for_month__month=this_month, for_month__year=this_year).exists():
        editable = Balance.objects.get(worker_id=worker_id, for_month__month=this_month, for_month__year=this_year)
        editable.balance_amount = further_advance
        editable.for_month = datetime.date.today()
    else:
        obj = Balance(worker_id=worker, balance_amount = further_advance)
        obj.save()
    return render(request, 'src/particulars.html', {'basic_wage': basic_wage, \
    'attended_days': attended_days, 'days_in_month': days_in_month, \
    'monthly_basic_wage':  monthly_basic_wage, 'overtime_hours': overtime_hours, \
    'overtime_wage': overtime_wage, 'last_month_advance': last_month_advance, \
    'this_month_advance': this_month_advance, 'monthly_wage': monthly_wage, \
    'provident_fund': provident_fund, 'amount_to_be_paid':amount_to_be_paid , \
    'paid_amount': paid_amount, 'grand_total': grand_total, 'worker_id':worker_id,\
    'further_advance':further_advance})
