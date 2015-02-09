from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

"""
All the URLs that can be possibly called by user are working here. 
"""

urlpatterns = patterns('',
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','src.views.index'),
    url(r'^addworker/','src.views.addworker'),
    url(r'^logout/$','src.views.my_logout'),
    url(r'^src/addadvance/','src.views.addadvance'),
    url(r'^src/promotions/','src.views.promotions'),
    url(r'^ajaxpromotions/','src.views.ajaxpromotions'),
    url(r'^popup_promotions/','src.views.popup_promotions'),
    url(r'^daily_attendance/','src.views.daily_attendance'),
    url(r'^ajax_daily_attendance/','src.views.ajax_daily_attendance'),
    url(r'^ajaxdetails/','src.views.ajaxdetails'),
    url(r'^ajaxrequest/','src.views.ajaxrequest'),
    url(r'^ajaxrequestpaid/','src.views.ajaxrequestpaid'),
    url(r'^popupadvance/','src.views.popupadvance'),
    url(r'^ajaxpopupadvance/','src.views.ajaxpopupadvance'),
    url(r'^particulars/','src.views.particulars'),
    url(r'^payslip/', 'src.views.payslip'),
    url(r'^return_advance/','src.views.return_advance'),
    url(r'^deleteworker/','src.views.deleteworker'),
    url(r'^jsreverse/', 'src.views.jsreverse'),
    
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Are these things needed after + ?


