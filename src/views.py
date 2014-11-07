from __future__ import division
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from src.models import *
from src.forms import *
#import forms
import datetime
from django.db.models import Sum
from calendar import monthrange

# These two variables are used >7 times in this file, so are declared 
# here only and refers to the current month and year.
this_month = datetime.date.today().month
this_year = datetime.date.today().year

@login_required
def index(request):
    """
    This view is used just for now and is only meant to redirect the
    user to first add a worker, before going anywhere when using Kirt 
    for the first time.
    """
    if not WorkerDetail.objects.all():
        return HttpResponseRedirect('/addworker/')
    else:
        return HttpResponseRedirect('/ajaxdetails/')

@login_required
def addworker(request):
    """
    If a new worker is to be added, this view is parsed and a form is 
    generated to add description about a new worker.
    """
    if request.method == 'POST':
        form = WorkerDetailForm(request.POST)
        if form.is_valid:
            try:
                form.save()
                request.session['success'] = 'success'
                # Return to form page
                return HttpResponseRedirect('/ajaxdetails/')
            except:
                message = "Sorry, there were invalid values in the form! "
                url = "/addworker/"
                return render(request, 'src/error.html', {'message':message,\
                    'url':url})
    else:
        form = WorkerDetailForm()
    return render(request,'src/addworker.html',{'WorkerDetailForm':form})

@login_required
def ajaxdetails(request):
    """
    No, the name is not illogical!
    I've used AJAX the first time here, so is the name behind this view.
    In actual this is the main view in app, which gives details of worker 
    particualarly about a combination of a month and year after filtering.
    There are lot more things happening here, look for other comments also.
    """
    # When worker is added, get session variable and get ready to display message "Success!"
    success = request.session.get('success')
    message = 'Success!'
    request.session['success'] = ''
    # First, fetch only the ids of all workers.
    allworkers = WorkerDetail.objects.values('id').all()
    # This list will contain a lot of values...
    detail_list = []
    # Initially, the idea of implementation started from search and the first
    # thing, here, is search, only then control proceeds forward.

    if request.method == 'POST':
         search_form = SearchSelect(request.POST)
         if search_form.is_valid():
             # If the search form posts some data, then get the year and 
             # month from posted data 
             year = search_form.cleaned_data['year']
             month = search_form.cleaned_data['month']
             # The year is converted to string to match the format, 
             # in case you were wondering.
             if (str(year) > str(this_year)):
                 #if (str(month) > str(this_month)):
                     message = "Hey! There are no future values yet!"
                     url = "/"
                     return render(request, 'src/error.html', {'message':message,\
                        'url':url})
             else:
                 if (str(this_year) == str(year)) and (str(this_month) == str(month)):
                     editable = 1
                 else:
                     editable = 0
    # Else take values for today's year and month and pass the values of
    # month and year to the for loop for feeding that list ;)
           	
    else:
        year = this_year
        month = this_month
        search_form = SearchSelect()
        editable = 1

    for value in allworkers:
        worker_dict = {}
        # Just collect everything needed!

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
    'search':search_form, 'editable':editable, 'year':year, 'month':month,
    'success':success, 'message':message})

# Ajax calls the following views

@login_required
def ajaxrequest(request):
    """
    This name needed to be changed!
    In actual this view is for the working of Days and OT fields, which 
    are updated, if already exist but are added, if doesn't exist for 
    current month and year. Both conditions work if partiular column is
    edited, uses Try except. I was so happy to make this logic! :D
    """
    worker_id = request.GET['worker_id']
    if MonthlyAttendance.objects.filter(worker_id_id=worker_id,\
        for_month__month=this_month, for_month__year=this_year).exists():
        editable_obj = MonthlyAttendance.objects.get(worker_id_id=worker_id,\
        for_month__month=this_month, for_month__year=this_year)
        try:
            days = request.GET['days']
            editable_obj.attended_days = days
            editable_obj.for_month = datetime.date.today()
            editable_obj.save()
            return HttpResponse(days)
        except:
            overtime = request.GET['overtime']
            editable_obj.overtime_hours = overtime
            editable_obj.for_month = datetime.date.today()
            editable_obj.save()
            return HttpResponse(overtime)
    else:
        worker = WorkerDetail.objects.get(pk=worker_id)
        try:
            days = request.GET['days']
            new_obj = MonthlyAttendance(worker_id = worker, attended_days 
            = days, overtime_hours = 0, for_month = datetime.date.today())
            new_obj.save()
            return HttpResponse("Days saved. Refresh the page!")
        except:
            overtime = request.GET['overtime'] 
            new_obj = MonthlyAttendance(worker_id = worker, attended_days 
            = 0, overtime_hours = overtime, for_month = datetime.date.today())
            new_obj.save()
            return HttpResponse("Overtime saved. Refresh the page!")

@login_required
def ajaxrequestpaid(request):
    """
    As the name says... here comes the AJAX request for editing Paid
    column and you know what happens to it... If exists, value is updated,
    else, a new row is inserted.
    """
    worker_id = request.GET['worker_id']
    paid = request.GET['paid']
    # To get the instance but not the id
    worker = WorkerDetail.objects.get(pk=worker_id) 
    if PaidSalary.objects.filter(worker_id_id=worker_id,\
        payment_date__month=this_month, payment_date__year=this_year).exists():
        # If the edited object's worker id and this month's and year's value exists
        editable = PaidSalary.objects.get(worker_id_id=worker_id,\
        payment_date__month=this_month, payment_date__year=this_year) 
        # for field in editable instance
        editable.paid_amount = paid
        editable.payment_date = datetime.date.today()
        editable.save()
        return HttpResponse("What you edited, is saved :)") 
    else:
        obj = PaidSalary(worker_id = worker, paid_amount = paid,\
        payment_date = datetime.date.today()) 
        obj.save()
        return HttpResponse("New value for paid added!")   

@login_required
def popupadvance(request):
    """
    This view takes all the values of advances to the popup!
    """
    worker_id = request.GET["worker_id"]
    worker_name = WorkerDetail.objects.values('first_name','last_name').get(id= worker_id)
    full_name = worker_name['first_name'] + " " +  worker_name['last_name']
    old_advances = Advance.objects.filter(worker_id = worker_id).\
    filter(advance_date__month=this_month).filter(advance_date__year=this_year)
    return render(request,'src/popup_addadvance.html', {'worker_id':\
    worker_id, 'old_advances':old_advances, 'full_name': full_name})
	
@login_required 
def ajaxpopupadvance(request):
    """
    This view is saving the new values for advances in popup, right?
    """
    worker_id = request.GET["worker_id"]
    # Advance.worker_id must be a WorkerDetail instance :P
    worker = WorkerDetail.objects.get(pk=worker_id) 
    popupadvance = request.GET['popupadvance']
    obj = Advance(worker_id=worker, advance_amount=popupadvance,\
    advance_date=datetime.date.today())
    obj.save()
    return HttpResponse("Advance added, Refresh page! :D ")

@login_required
def particulars(request):
    """
    Ah! These comments are very useful which were left there only, while
    testing. All the very very important calculations are handled here. 
    You can uncomment any return response to break the processing and
    see what value is there :)
    """
    # "worker_id =" or "worker-id_id"?
    worker_id = request.GET['worker_id']
    month = int(request.GET['month'])
    year = int(request.GET['year'])
    #further_advance = 0.0
        
    try:    
        basic_wage = WorkerDetail.objects.values('basic_wage').\
        filter(id=worker_id)[0]['basic_wage']
        attended_days = MonthlyAttendance.objects.values('attended_days').\
        filter(worker_id=worker_id).filter(for_month__month=month).\
        filter(for_month__year=year)[0]['attended_days']
        #return HttpResponse(basic_wage)
        days_in_month = monthrange(year, month)[1]		
        monthly_basic_wage = ((basic_wage / days_in_month) * attended_days)	
            # return HttpResponse(monthly_basic_wage)
        overtime_hours = MonthlyAttendance.objects.values('overtime_hours').\
        filter(worker_id=worker_id).filter(for_month__month=month).\
        filter(for_month__year=year)[0]['overtime_hours']
            #return HttpResponse(overtime_hours)
        overtime_wage = round((basic_wage / days_in_month) / 6 * overtime_hours)
        total = monthly_basic_wage + overtime_wage
            # return HttpResponse(total)
        last_month_advance = Balance.objects.values('balance_amount').\
        filter(worker_id = worker_id).filter(for_month__month=month-1).\
        filter(for_month__year=year)[0]['balance_amount']
            # return HttpResponse(last_month_advance)
        month_advance = Advance.objects.filter(worker_id = worker_id ).\
        filter(advance_date__year=year).filter(advance_date__month=\
        month).aggregate(Sum('advance_amount'))['advance_amount__sum']
            # return HttpResponse(month_advance)
        monthly_wage = total - month_advance 
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
        if Balance.objects.filter(worker_id=worker_id, for_month__month
            =month, for_month__year=year).exists():
            editable = Balance.objects.get(worker_id=worker_id,\
            for_month__month=month, for_month__year=year)
            editable.balance_amount = further_advance
            editable.for_month = datetime.date.today()
            editable.save()
        else:
            obj = Balance(worker_id=worker, balance_amount = further_advance)
            obj.save()
        return render(request, 'src/particulars.html', {'basic_wage': basic_wage, \
        'attended_days': attended_days, 'days_in_month': days_in_month, \
        'monthly_basic_wage':  monthly_basic_wage, 'overtime_hours': overtime_hours, \
        'overtime_wage': overtime_wage, 'last_month_advance': last_month_advance, \
        'month_advance': month_advance, 'monthly_wage': monthly_wage, \
        'provident_fund': provident_fund, 'amount_to_be_paid':amount_to_be_paid , \
        'paid_amount': paid_amount, 'grand_total': grand_total, 'worker_id':worker_id,\
        'further_advance':further_advance})
    except:
        # Is there is some prolem in the above, data insufficient, don't throw an error.
        # Instead, show what is already there.
        basic_wage = WorkerDetail.objects.values('basic_wage').\
        filter(id=worker_id)[0]['basic_wage']
        attended_days = MonthlyAttendance.objects.values('attended_days').\
        filter(worker_id=worker_id).filter(for_month__month=month).\
        filter(for_month__year=year)[0]['attended_days']
        #return HttpResponse(basic_wage)
        days_in_month = monthrange(year, month)[1]		
        monthly_basic_wage = ((basic_wage / days_in_month) * attended_days)	
        #return HttpResponse(monthly_basic_wage)
        overtime_hours = MonthlyAttendance.objects.values('overtime_hours').\
        filter(worker_id=worker_id).filter(for_month__month=month).\
        filter(for_month__year=year)[0]['overtime_hours']
        return render(request, 'src/particulars1.html', {'basic_wage': basic_wage, \
        'attended_days': attended_days, 'days_in_month': days_in_month, \
        'monthly_basic_wage':  monthly_basic_wage, 'overtime_hours': overtime_hours})

def return_advance(request):
    """
    Here comes another interesting thing :D When the popup is closed, the
    control comes here and takes the new value to form field, which is 
    caled refreshing through AJAX ;)
    """
    worker_id = request.GET['worker_id']
    month = request.GET['month']
    year = request.GET['year']
    updated_advance = Advance.objects.filter(worker_id = worker_id ).\
    filter(advance_date__year=year).filter(advance_date__month=\
    month).aggregate(Sum('advance_amount'))['advance_amount__sum']
    return HttpResponse(updated_advance)
