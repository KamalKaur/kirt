from __future__ import division
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from src.models import *
from src.forms import *
#import forms
import datetime
from django.db.models import Sum
from calendar import monthrange
from django.core.urlresolvers import reverse
from src.config import _MAN_HOURS_A_DAY
from src.config import _OVERTIME_WAGE_FACTOR
from src.config import _COMPANY_NAME
from src.config import _COMPANY_ADDRESS_PART_1
from src.config import _COMPANY_ADDRESS_PART_2
#for payslip
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO



# These two variables are used >7 times in this file, so are declared 
# here only and refers to the current month and year.
this_month = datetime.date.today().month
this_year = datetime.date.today().year

@login_required
def index(request):
    """
    This view is meant to redirect the user to first add a worker, 
    before going anywhere when using Kirt for the first time. Else it 
    redirects to the salarysheet.
    """
    if not WorkerDetail.objects.all() or not WorkerDetail.objects.filter(status=1):
        return HttpResponseRedirect(reverse("src.views.addworker"))
    else:
        return render(request,'src/index.html',{})

@login_required
def my_logout(request):
    """
    The logout function imports logout from the views of django.auth,
    redirects to the index view and then the login page is renderd
    again.
    """
    from django.contrib.auth.views import logout
    logout(request)
    return HttpResponseRedirect(reverse("src.views.index"))

def jsreverse(request):
    """
    This function reverse looks up the urls for the AJAX Requests and
    enalbles he developer to use dynamic URLs in JavaScript.
    """
    string_to_reverse = request.GET['string'];
    return HttpResponse(reverse(string_to_reverse))

@login_required
def addworker(request):
    """
    If a new worker is to be added, this view is parsed and a form is 
    generated to add description about a new worker. On submitting the 
    the same form, from same page, the model WorkerDetails gets updates
    with respective records and starts appearing in salarysheet.
    """
    if request.method == 'POST':
        form = WorkerDetailForm(request.POST)
        if form.is_valid():
            #try:
            workerdetail = form.save()
            request.session['success'] = 'success'
            wd = WorkerDetail.objects.get(id = workerdetail.id)
            monthlyattendance = MonthlyAttendance(worker_id = wd,\
            attended_days = 0, overtime_hours = 0,\
            for_month = workerdetail.joining_date)
            monthlyattendance.save()
            paidsalary = PaidSalary(worker_id = wd, paid_amount = None,\
            payment_date = workerdetail.joining_date)
            paidsalary.save()
            first_basic_wage = Promotions(worker_id = wd, promoted_wage =\
            workerdetail.basic_wage, on_date = workerdetail.joining_date)
            first_basic_wage.save()
            return HttpResponseRedirect(reverse("src.views.index"))
        else:
            message = "Please correct the errors below"
            form = WorkerDetailForm(request.POST)
            return render(request,'src/addworker.html',{'WorkerDetailForm':form,
            'message':message })
			
            # except:
              #  message = "Sorry, there were invalid values in the form! "
               # url = reverse("src.views.addworker")
                #return render(request, 'src/error.html', {'message':message,\
                 #   'url':url})
    else:
        form = WorkerDetailForm()
    return render(request,'src/addworker.html',{'WorkerDetailForm':form})

@login_required
def daily_attendance(request):
    """
    This view displays the list of the employees who are currently working
    to add their attendance for today or for the date which it has not yet 
    been added.
    """
    detail_list = []
    allworkers = WorkerDetail.objects.values('id').filter(status = 1)

    for worker in allworkers:
        if  DailyAttendance.objects.filter(worker_id = worker['id']).\
        filter(for_day = datetime.date.today()).exists():
            pass
        else:
            worker_object = WorkerDetail.objects.get(pk=worker['id'])
            new_object = DailyAttendance(worker_id = worker_object,\
            overtime = 0, attendance = 0, for_day = datetime.date.today())
            new_object.save()
            pass

        if MonthlyAttendance.objects.filter(worker_id = worker['id']).\
        filter(for_month__month = this_month).filter(for_month__year
        = this_year).exists():
            pass
        else:
            worker_object = WorkerDetail.objects.get(pk=worker['id'])
            new_object = MonthlyAttendance(worker_id = worker_object,\
            attended_days = 0, overtime_hours = 0, for_month = datetime.date.today())
            new_object.save()
        pass
    """
    for value in allworkers:
        worker_dict = {}

        details = WorkerDetail.objects.values('first_name', 'last_name',
        'address').filter(status = 1).filter(id = value['id'])

        daily_attendance = DailyAttendance.objects.values('attendance').\
        filter(worker_id = value['id']).filter(for_day = datetime.\
        date.today()).filter(worker_id__status = 1)

        daily_overtime = DailyAttendance.objects.values('overtime').\
        filter(worker_id = value['id']).filter(for_day = datetime.\
        date.today()).filter(worker_id__status = 1)

        worker_dict['worker_id'] = value['id']

        for item in details:
            worker_dict['first_name'] = item['first_name']
            worker_dict['last_name'] = item['last_name']
            worker_dict['address'] = item['address']
        for item in daily_attendance:
            worker_dict['daily_attendance'] = item['attendance']
        for item in daily_overtime:
            worker_dict['daily_overtime'] = item['overtime']
        detail_list.append(worker_dict)
    """

    workerDetail_attendance = DailyAttendance.objects.filter(for_day = datetime.\
    date.today()).order_by('worker_id_id').select_related('worker_id').\
    filter(worker_id__status = 1).all()

    date = datetime.date.today()
        
    return render(request,'src/daily_attendance.html',{'workerDetail_attendance':\
        workerDetail_attendance, 'date': date})

@login_required
def ajax_daily_attendance(request):
    """
    This view checks the incoming request and saves overtime or 
    attendance accordingly
    """
    worker_id = request.GET['worker_id']
    try:
        overtime = request.GET['overtime']
        overtime = float(overtime)
        if overtime >= 0 and overtime <= 11:
            edit_daily_overtime = DailyAttendance.objects.get(worker_id_id=worker_id,\
            for_day = datetime.date.today())
            # When overtime is updated in daily attendance, also remove 
            # the previously added value from monthlyattendance even before 
            # updating in daily attendance table.
            value_to_be_subtracted_from_monthlyattendance = edit_daily_overtime.overtime
            edit_obj = MonthlyAttendance.objects.get(worker_id_id=worker_id,\
            for_month__month=this_month, for_month__year=this_year)
            edit_obj.overtime_hours = edit_obj.overtime_hours - value_to_be_subtracted_from_monthlyattendance
            edit_obj.save()
            #return HttpResponse(value_to_be_subtracted_from_monthlyattendance)
            # After subtracting the previously saved value from monthly 
            # attendance, now override it.
            edit_daily_overtime.overtime = overtime
            edit_daily_overtime.save()
    
            edit_monthly_overtime = MonthlyAttendance.objects.get(worker_id_id=worker_id,\
            for_month__month=this_month, for_month__year=this_year)
            edit_monthly_overtime.overtime_hours = edit_monthly_overtime.\
            overtime_hours+overtime 
            edit_monthly_overtime.save()
        return HttpResponse(overtime)

    except:
        attendance = request.GET['attendance']
        attendance = float(attendance)
        edit_daily_attendance = DailyAttendance.objects.get(worker_id_id=worker_id,\
        for_day = datetime.date.today())
        edit_daily_attendance.attendance = attendance
        edit_daily_attendance.save()

        edit_monthly_attendance = MonthlyAttendance.objects.get(worker_id_id=worker_id,\
        for_month__month=this_month, for_month__year=this_year)
        edit_monthly_attendance.attended_days =  edit_monthly_attendance.\
        attended_days+attendance 
        edit_monthly_attendance.save()
        return HttpResponse(edit_monthly_attendance.attended_days)
        

""" Yet not required :P AS the conditions in above two views are changed :)

    if DailyAttendance.objects.filter(worker_id=worker_id,\
        for_day = datetime.date.today()).exists():
        editable_obj = DailyAttendance.objects.get(worker_id_id=worker_id,\
        for_day = datetime.date.today())
        try:
            overtime = request.GET['overtime']
            editable_obj.overtime = overtime
            editable_obj.save()
            #editable_obj.for_day = datetime.date.today()
            editable_hours = MonthlyAttendance.objects.get(worker_id_id=worker_id,\
                for_month__month=this_month, for_month__year=this_year)
            editable_hours.overtime_hours = overtime
            editable_hours.save() # Update in MonthlyAttendance to be displayed in salarysheet.
            return HttpResponse(overtime)
        except:
            attendance = request.GET['attendance']
            attendance = float(attendance)
            #return HttpResponse(attendance)
            editable_obj.attendance = attendance
            editable_obj.save()
            new_attendance = MonthlyAttendance.objects.get(worker_id_id=worker_id,\
                for_month__month=this_month, for_month__year=this_year)
            new_attendance.attended_days = new_attendance.attended_days + attendance/8
            new_attendance.save()
            #editable_obj.for_day = datetime.date.today()
            return HttpResponse(attendance)


    else:
        worker = WorkerDetail.objects.get(pk=worker_id)
        try:
            attendance = request.GET['attendance']
            attendance = float(attendance)
            new_obj = DailyAttendance(worker_id = worker, attendance
            = attendance, overtime = 0, for_day = datetime.date.today()) # that day
            new_obj.save()
            new_attendance = MonthlyAttendance(worker_id = worker, attended_days 
            = attendance, overtime_hours = 0, for_month = datetime.date.today())
            new_attendance.save()	
            return HttpResponse("Days saved. Refresh the page!")
        except:
            overtime = request.GET['overtime'] 
            new_obj = DailyAttendance(worker_id = worker, attendance 
            = 0, overtime = overtime, for_day = datetime.date.today())
            new_hours = MonthlyAttendance(worker_id = worker, attended_days 
            = 0, overtime_hours = overtime, for_month = datetime.date.today())
            new_obj.save()
            new_hours.save() # Update in MonthlyAttendance to be displayed in salarysheet.
            return HttpResponse("Overtime saved. Refresh the page!")
    #return HttpResponse(worker_id)
"""
@login_required 
def addadvance(request):
    if request.method == 'POST':
        form = AdvanceForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            message = "Please correct the errors below"
            form = AdvanceForm(request.POST)
            return render(request,'src/addadvance.html',{'AdvanceForm':form,
            'message':message })
        return HttpResponseRedirect(reverse("src.views.index"))
    else:
        form = AdvanceForm()
        return render(request,'src/addadvance.html',{'AdvanceForm':form})

@login_required
def promotions(request):
    """
    This view is called to add and update te promotions in worker
    salaries.
    """
    date = datetime.date.today()
    worker_details = WorkerDetail.objects.filter(status=1)
    return render(request,'src/promotions.html',{'worker_details': \
    worker_details, 'date':date})

@login_required
def ajaxpromotions(request):
    """
    Handles the ajax request from Promotions page
    """
    worker_id = request.GET['worker_id']
    promotion = request.GET['promotion']
    worker = WorkerDetail.objects.get(pk=worker_id)
    if Promotions.objects.filter(worker_id_id=worker_id,\
        on_date__month=this_month, on_date__year=this_year).exists():
        editable_obj = Promotions.objects.get(worker_id_id=worker_id,\
        on_date__month=this_month, on_date__year=this_year)
        editable_obj.promoted_wage = promotion
        editable_obj.save()
        edit_in_workerdetails = WorkerDetail.objects.get(id = worker_id)
        edit_in_workerdetails.basic_wage = promotion
        edit_in_workerdetails.save()
        return HttpResponse("Updated")
    else:
        new_promotion_object = Promotions(worker_id = worker, promoted_wage \
        = promotion, on_date = datetime.date.today())
        new_promotion_object.save()
        edit_in_workerdetails = WorkerDetail.objects.get(id = worker_id)
        edit_in_workerdetails.basic_wage = promotion
        edit_in_workerdetails.save()
        return HttpResponse("New object added")

@login_required
def previous_promotions(request):
    worker_id = request.GET['worker_id']
    worker_name = WorkerDetail.objects.values('first_name', 'middle_name',\
    'last_name').get(id= worker_id)
    full_name = worker_name['first_name'] + " " + worker_name['middle_name'] \
    + " " + worker_name['last_name']
    date = WorkerDetail.objects.values('joining_date').get(id= worker_id)
    joining_date = date['joining_date']
    previous_promotions = Promotions.objects.filter(worker_id = worker_id)
    return render(request,'src/previous_promotions.html',{'full_name':\
        full_name, 'previous_promotions':previous_promotions, 'joining_date':joining_date})


@login_required
def ajaxdetails(request):
    """
    No, the name is not illogical!
    I've used AJAX the first time here, so is the name behind this view.
    In actual this is the main view in app, which gives details of workers 
    particualarly about a combination of a month and year after filtering.
    It Displays the salarysheet for any month even for history, the same
    view is called and displays the required data.
    
    There are lot more things happening here, look for other comments given
    inside the view as well.
    """
    # When worker is added, get session variable and get ready to display message "Success!"
    success = request.session.get('success')
    message = 'Success!'
    request.session['success'] = ''
    # First, fetch only the ids of all workers.
    allworkers = WorkerDetail.objects.values('id').filter(status = 1)
    # This list will contain a lot of values...
    detail_list = []
    editable = ""
    # Initially, the idea of implementation started from search and the first
    # thing, here, is search, only then control proceeds forward.

    # A minimal function to get the last day of month using the date.
    def last_day_of_month(any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)


    if request.method == 'POST':
         search_form = SearchSelect(request.POST)
         if search_form.is_valid():
            # If the search form posts some data, then get the year and
            # month from posted data
            year = search_form.cleaned_data['year']
            # return HttpResponse(year)
            month = search_form.cleaned_data['month']
            # return HttpResponse(month)
            # The year is converted to string to match the format, 
            # in case you were wondering.
            if (str(year) > str(this_year)): 
                message = "Hey! There are no future values yet!"
                url = "src.views.ajaxdetails"
                return render(request, 'src/error.html', {'message':message,\
                    'url':url})
            elif (str(year) <= str(this_year)):
                if (str(month) > str(this_month) and str(year) == str(this_year)):
                    message = "Hey! There are no future values yet!"
                    url = "src.views.ajaxdetails" 
                    return render(request, 'src/error.html', {'message':message,\
                        'url':url})
                elif (str(month) == str(this_month) and str(year) == str(this_year)):
                    editable = 1

                else:
                    start_date = datetime.date(int(year),int(month),1)
                    end_date = last_day_of_month(start_date)
                    date_filter = Q(resigning_date__range = [str(start_date),str(end_date)])
                    date_filter |= Q(resigning_date__isnull = True)
                    allworkers = WorkerDetail.objects.values('id').filter(date_filter)\
                    .filter(joining_date__lte = str(end_date))
#                   temp_month = int(month) + 1;
#                   temp_year = int(year)
#                    
#                   if temp_month > 12:
#                       temp_month = temp_month - 12
#                       temp_year = temp_year + 1
#                   temp_date = datetime.date(temp_year, temp_month, 1)
#                   allworkers = WorkerDetail.objects.values('id').\
#                   filter(joining_date__lt=temp_date,resigning_date__gte=temp_date)
                editable = 0
    # Else take values for today's year and month and pass the values of
    # month and year to the for loop for feeding that list ;)
            
    else:
        year = this_year
        month = this_month
        search_form = SearchSelect(initial={'year': this_year, 'month':this_month})
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
    edited, uses Try except. I was so happy to make this simple logic! :D
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
    column and you know what happens to it? It first checks if such a
    calue exists or not. If a value exists, the same is updated,
    else, a new row is inserted into the table Paid amount.
    """
    worker_id = request.GET['worker_id']
    paid = float(request.GET['paid'])
    month = int(request.GET['month'])
    year = int(request.GET['year'])

    # To get the instance but not the id
    worker = WorkerDetail.objects.get(pk=worker_id) 
    if PaidSalary.objects.filter(worker_id_id=worker_id,\
        payment_date__month=month, payment_date__year=year).exists():
        # If the edited object's worker id and this month's and year's value exists
        editable = PaidSalary.objects.get(worker_id_id=worker_id,\
        payment_date__month=month, payment_date__year=year) 
        # for field in editable instance
        editable.paid_amount = paid
        editable.payment_date = datetime.date(year,month,28)
        editable.save()
    else:
        obj = PaidSalary(worker_id = worker, paid_amount = paid,\
        payment_date = datetime.date(year,month,28)) 
        obj.save()

    further_advance = request.session['amount_to_be_paid'] - paid
    worker = WorkerDetail.objects.get(pk=worker_id)

    if Balance.objects.filter(worker_id=worker_id, for_month__month
        =month, for_month__year=year).exists():
        editable = Balance.objects.get(worker_id=worker_id,\
        for_month__month=month, for_month__year=year)
        editable.balance_amount = further_advance
        editable.for_month = datetime.date(year,month,28)
        editable.save()
    else:
        obj = Balance(worker_id=worker, balance_amount = further_advance)
        obj.save()

    if WageDescription.objects.filter(worker_id_id=worker_id).\
        filter(for_month__month = month).exists():
        wage_obj = WageDescription.objects.get(worker_id_id=worker_id,\
        for_month__month = month)
        wage_obj.monthly_basic_wage = request.session['monthly_basic_wage']
        wage_obj.overtime_wage = request.session['overtime_wage']
        wage_obj.monthly_wage = request.session['monthly_wage']
        wage_obj.amount_to_be_paid = request.session['amount_to_be_paid']
        wage_obj.paid_amount = paid
        wage_obj.for_month = datetime.date(year,month,28)
        wage_obj.save()
    else:
        wage_obj = WageDescription(worker_id_id=worker_id, \
        monthly_basic_wage = request.session['monthly_basic_wage'], \
        overtime_wage = request.session['overtime_wage'], \
        monthly_wage = request.session['monthly_wage'],\
        amount_to_be_paid = request.session['amount_to_be_paid'],\
        paid_amount = paid,
        for_month = datetime.date(year,month,28))
        wage_obj.save()

    return HttpResponse(further_advance) 

@login_required
def popupadvance(request):
    """
    This view takes all the values of advances to the popup!
    A button for every worker is displayed on the salarysheet and this 
    view is accessed when that button is clicked. 
    """
    worker_id = request.GET["worker_id"]
    year = request.GET['year']
    month = request.GET['month']
    worker_name = WorkerDetail.objects.values('first_name','last_name').get(id= worker_id)
    full_name = worker_name['first_name'] + " " +  worker_name['last_name']
    old_advances = Advance.objects.filter(worker_id = worker_id).\
    filter(advance_date__month=this_month).filter(advance_date__year=this_year)
    return render(request,'src/popup_addadvance.html', {'worker_id':\
    worker_id, 'old_advances':old_advances, 'full_name': full_name,\
    'year': year, 'month': month})
	
@login_required 
def ajaxpopupadvance(request):
    """
    This view is saving the new values for advances in the popup that
    was opened after clicking the button to add advance. 
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
    This function is called when a user clicks the worker name.
    All the values after fetching from database, are calculated
    and displayed on the next page. Also the balance amount, if already exists,
    is updated. Else its added in a new row in Balance table.

    Ah! These comments are very useful which were left there only, while
    testing. All the very very important calculations are handled here. 
    THe developer can uncomment any return response to break the processing and
    see what value is there :)
    """
    # "worker_id =" or "worker-id_id"?
    worker_id = request.GET['worker_id']
    month = int(request.GET['month'])
    year = int(request.GET['year'])
    #further_advance = 0.0
    
        
    first_name = WorkerDetail.objects.values('first_name').\
    filter(id=worker_id)[0]['first_name']
    last_name = WorkerDetail.objects.values('last_name').\
    filter(id=worker_id)[0]['last_name']
    address = WorkerDetail.objects.values('address').\
    filter(id=worker_id)[0]['address']

    try:
        found = 0
        temp_month = month
        temp_year = year
        while found == 0:
            if Promotions.objects.filter(worker_id=\
                worker_id).filter(on_date__month = temp_month).\
                filter(on_date__year = temp_year).exists() == True:

                basic_wage = Promotions.objects.values('promoted_wage').\
                filter(worker_id=worker_id).filter(on_date__month = \
                temp_month).filter(on_date__year = temp_year)[0]['promoted_wage']
                found = 1;
            else:
                if temp_month==1: 
                    temp_month = 12
                    temp_year = temp_year-1
                else:
                    temp_month = temp_month-1

        attended_days = MonthlyAttendance.objects.values('attended_days').\
        filter(worker_id=worker_id).filter(for_month__month=month).\
        filter(for_month__year=year)[0]['attended_days']
        #return HttpResponse(basic_wage)_OVERTIME_WAGE_FACTOR

        days_in_month = monthrange(year, month)[1]		

        overtime_hours = MonthlyAttendance.objects.values('overtime_hours').\
        filter(worker_id=worker_id).filter(for_month__month=month).\
        filter(for_month__year=year)[0]['overtime_hours']
            #return HttpResponse(overtime_hours)

        if month == 1:
            try:
                last_month_advance = Balance.objects.values('balance_amount').\
                filter(worker_id = worker_id).filter(for_month__month=12).\
                filter(for_month__year=year-1)[0]['balance_amount']
                # return HttpResponse(last_month_advance)
            except:
                last_month_advance = 0
                # return HttpResponse(last_month_advance)
        else:
            try:
                last_month_advance = Balance.objects.values('balance_amount').\
                filter(worker_id = worker_id).filter(for_month__month=month-1).\
                filter(for_month__year=year)[0]['balance_amount']
            except:
                last_month_advance = 0
                # return HttpResponse(last_month_advance)
        if last_month_advance == None:
            last_month_advance = 0
        try:
            month_advance = Advance.objects.filter(worker_id = worker_id ).\
            filter(advance_date__year=year).filter(advance_date__month=\
            month).aggregate(Sum('advance_amount'))['advance_amount__sum']
            # return HttpResponse(month_advance)
        except:
            month_advance = 0
        if month_advance == None:
            month_advance = 0
        provident_fund = WorkerDetail.objects.values('provident_fund').\
            filter(id=worker_id)[0]['provident_fund']

#        paid_amount = PaidSalary.objects.values('paid_amount'). \
#            filter(worker_id=worker_id)[0]['paid_amount']
            # return HttpResponse(paid_amount)

#        if paid_amount == None:
#            paid_amount = 0

        if PaidSalary.objects.values('paid_amount').\
            filter(worker_id=worker_id).filter(payment_date__month = month).\
            filter(payment_date__year = year)[0]['paid_amount'] == None:
            
            monthly_basic_wage = round(((basic_wage / days_in_month) * attended_days),2)	
            # return HttpResponse(monthly_basic_wage)

            overtime_wage = round((basic_wage / days_in_month) / (_MAN_HOURS_A_DAY/_OVERTIME_WAGE_FACTOR ) * overtime_hours, 2) # 6 = (9/1.5)

            total = monthly_basic_wage + overtime_wage
            # return HttpResponse(total)

            monthly_wage = total - month_advance 
            # return HttpResponse(monthly_wage)
            
            grand_total = monthly_wage - last_month_advance

            amount_to_be_paid = grand_total - provident_fund
            #return HttpResponse(amount_to_be_paid)

            paid_amount = 0
        else:
            wage_obj = WageDescription.objects.get(worker_id_id=worker_id, \
            for_month__month = month, for_month__year = year)

            monthly_basic_wage = wage_obj.monthly_basic_wage
            overtime_wage = wage_obj.overtime_wage
            monthly_wage = wage_obj.monthly_wage
            amount_to_be_paid = wage_obj.amount_to_be_paid
            paid_amount = wage_obj.paid_amount
            grand_total = monthly_wage - last_month_advance
            # return HttpResponse(grand_total)

        further_advance = amount_to_be_paid - paid_amount

        request.session['name'] = first_name + ' ' + last_name
        request.session['address'] = address
        request.session['attended_days'] = attended_days
        request.session['overtime_hours'] = overtime_hours
        request.session['monthly_basic_wage'] = monthly_basic_wage
        request.session['monthly_wage'] = monthly_wage
        request.session['overtime_wage'] = overtime_wage
        request.session['provident_fund'] = provident_fund
        request.session['last_month_advance'] = last_month_advance
        request.session['month_advance'] = month_advance
        request.session['amount_to_be_paid'] = amount_to_be_paid

        if PaidSalary.objects.values('paid_amount').filter(worker_id=worker_id).\
            filter(payment_date__month = month).\
            filter(payment_date__year = year)[0]['paid_amount'] == None:
            salary_paid = False
            temp_month = month
            temp_year = year
            if temp_month == 1:
                temp_month = 12
                temp_year = temp_year - 1
            else:
                temp_month = temp_month - 1
            if PaidSalary.objects.values('paid_amount').filter(worker_id=worker_id).\
                filter(payment_date__month = temp_month).\
                filter(payment_date__year = temp_year)[0]['paid_amount'] == None:
                previous_salary_paid = False
        else:
            salary_paid = True

        return render(request, 'src/particulars.html', {'first_name': first_name,\
        'last_name': last_name,'basic_wage': basic_wage, 'salary_paid':salary_paid,\
        'attended_days': attended_days, 'days_in_month': days_in_month,  'previous_salary_paid': previous_salary_paid,\
        'monthly_basic_wage':  monthly_basic_wage, 'overtime_hours': overtime_hours, \
        'overtime_wage': overtime_wage, 'last_month_advance': last_month_advance, \
        'month_advance': month_advance, 'monthly_wage': monthly_wage, \
        'provident_fund': provident_fund, 'amount_to_be_paid':amount_to_be_paid , \
        'paid_amount': paid_amount, 'grand_total': grand_total, 'worker_id':worker_id,\
        'further_advance':further_advance, 'this_month':this_month,'worker_id':worker_id, 'month': month, 'year': year})

    except:
         # Is there is some prolem in the above, data insufficient, don't throw an error.
         # Instead, show what is already there.
         basic_wage = WorkerDetail.objects.values('basic_wage').\
         filter(id=worker_id)[0]['basic_wage']
         try:
             attended_days = MonthlyAttendance.objects.values('attended_days').\
             filter(worker_id=worker_id).filter(for_month__month=month).\
             filter(for_month__year=year)[0]['attended_days']
         except:
             attended_days = 0
         #return HttpResponse(basic_wage)
         days_in_month = monthrange(year, month)[1]		
         monthly_basic_wage = round(((basic_wage / days_in_month) * attended_days),2)
         #return HttpResponse(monthly_basic_wage)
         try: 
             overtime_hours = MonthlyAttendance.objects.values('overtime_hours').\
             filter(worker_id=worker_id).filter(for_month__month=month).\
             filter(for_month__year=year)[0]['overtime_hours']
         except:
             overtime_hours = 0
         provident_fund = WorkerDetail.objects.values('provident_fund').\
         filter(id=worker_id)[0]['provident_fund']
         return render(request, 'src/particulars1.html', {'first_name': first_name,\
        'last_name': last_name, 'basic_wage': basic_wage, \
         'attended_days': attended_days, 'days_in_month': days_in_month, \
         'monthly_basic_wage':  monthly_basic_wage, 'overtime_hours': overtime_hours,\
         'worker_id':worker_id})

def return_advance(request):
    """
    Here comes another interesting thing which enhances the user 
    experience to a greater extent. When the popup is closed, the
    control comes here and takes the new value to form field, which is 
    called refreshing through AJAX ;) 
    """
    worker_id = request.GET['worker_id']
    month = request.GET['month']
    year = request.GET['year']
    updated_advance = Advance.objects.filter(worker_id = worker_id ).\
    filter(advance_date__year=year).filter(advance_date__month=\
    month).aggregate(Sum('advance_amount'))['advance_amount__sum']
    return HttpResponse(updated_advance)

def deleteworker(request):
    """
    When the user clicks on Delete button, this function is called to
    change that worker's status to inactive and set the resigning date.
    Which isthen reflected in the spreadsheet after a success message.
    """
    worker_id = request.GET['worker_id']
    try:
        obj = WorkerDetail.objects.get(id = worker_id)
        obj.status = 0
        obj.resigning_date = datetime.date.today()
        obj.save()
    except:
        message = "Not deleted"

    return HttpResponse(worker_id)

def payslip(request):
    """
    When the user clicks on Payslip button, this function is called to
    provide options to save or view the Pay slip as PDF using a python 
    library: ReportLab
    """
    worker_id = request.GET['worker_id']
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Payslip-'+request.session['name']+'.pdf'

        buff = BytesIO()
        doc = SimpleDocTemplate(buff)
        # container for the 'Flowable' objects
        elements = []
        month = datetime.date.today().strftime("%B")
        year = str(this_year)
 
        data= [['PAYSLIP (' + month + ', ' + year + ')'],
               [_COMPANY_NAME],
               [_COMPANY_ADDRESS_PART_1],
               [_COMPANY_ADDRESS_PART_2],
               ['Employee Details'],
               ['Name', request.session['name']],
               ['Address', request.session['address']],
               ['Salary Details'],
               ['Description','Days/Hours','Amount'],
               ['Earnings'],
               ['Basic wage', str(request.session['attended_days']) +' days',request.session['monthly_basic_wage']],
               ['Overtime wage', str(request.session['overtime_hours']) +' hours',request.session['overtime_wage']],
               ['Deductions'],
               ['Provident Fund', request.session['provident_fund']],
               ['Other'],
               ['Last Month Advance', request.session['last_month_advance']],
               ['Current Month Advance', request.session['month_advance']],
               ['TOTAL',request.session['amount_to_be_paid']]]

        t=Table(data, colWidths=2.40*inch,  rowHeights=0.35*inch)
        t.setStyle(TableStyle([('ALIGN',(-2,-13),(-1,-1),'RIGHT'),
                               ('ALIGN',(-3,-11),(-1,-11),'CENTER'),
                               ('TEXTCOLOR',(0,0),(0,-1),colors.black),
                               ('FONT',(-3,-18),(-1,-1),'Helvetica',12),
                               ('FONT',(-3,-4),(-1,-4),'Helvetica-Bold',10),
                               ('FONT',(-3,-6),(-1,-6),'Helvetica-Bold',10),
                               ('FONT',(-3,-9),(-1,-9),'Helvetica-Bold',10),
                               ('FONT',(-3,-11),(-1,-10),'Helvetica-Bold',10),
                               ('FONT',(-3,-14),(-1,-14),'Helvetica-Bold',10),
                               ('FONT',(-3,-1),(-1,-1),'Helvetica-Bold',13),
                               ('LINEBELOW',(-3,-18),(-1,-18),1,colors.black),
                               ('LINEBELOW',(-3,-1),(-1,-1),1,colors.black),
                               ('LINEABOVE',(-3,-1),(-1,-1),1,colors.black),
                               ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                               ('TEXTCOLOR',(0,-1),(-1,-1),colors.black),
                               ('BACKGROUND', (-3,-14), (-1,-14), colors.gray),
                               ('BACKGROUND', (-3,-11), (-1,-11), colors.gray),
                               ('BACKGROUND', (-3,-9), (-1,-9), colors.gray),
                               ('BACKGROUND', (-3,-6), (-1,-6), colors.gray),
                               ('BACKGROUND', (-3,-4), (-1,-4), colors.gray),
                               ('SPAN',(-2,-13),(-1,-13)),
                               ('SPAN',(-2,-12),(-1,-12)),
                               ('SPAN',(-2,-5),(-1,-5)),
                               ('SPAN',(-2,-4),(-1,-4)),
                               ('SPAN',(-2,-3),(-1,-3)),
                               ('SPAN',(-2,-2),(-1,-2)),
                               ('SPAN',(-2,-1),(-1,-1)),
                               ('SPAN',(-3,-11),(-1,-11)),
                               ('SPAN',(-3,-18),(-1,-18)),
                               ('SPAN',(-3,-17),(-1,-17)),
                               ('SPAN',(-3,-16),(-1,-16)),
                               ('SPAN',(-3,-15),(-1,-15)),
                               ('ALIGN',(-3,-17),(-1,-15),'RIGHT'),
                               ('ALIGN',(-2,-10),(-2,-7),'RIGHT'),
                               ('ALIGN',(-3,-18),(-1,-18),'CENTER'),
                               ('INNERGRID', (-3,-13), (-1,-12), 0.25, colors.black),
                               ('INNERGRID', (-3,-10), (-1,-10), 0.25, colors.black),
                               ('INNERGRID', (-3,-8), (-1,-7), 0.25, colors.black),
                               ('INNERGRID', (-3,-5), (-1,-5), 0.25, colors.black),
                               ('INNERGRID', (-3,-3), (-1,-2), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ]))

        elements.append(t)
        # write the document to disk
        doc.build(elements)
        response.write(buff.getvalue())
        buff.close()
        return response
    except:
        return render(request,'src/index.html',{})
