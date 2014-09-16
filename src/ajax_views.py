
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
    if PaidSalary.objects.filter(worker_id_id=worker_id, payment_date__month=today.month).exists():
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
