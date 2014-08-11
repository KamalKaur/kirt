from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kirt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('registration.urls')),
    url(r'^$','src.views.index'),
    url(r'^addworker/','src.views.addworker'),
    # url(r'^addadvance/','src.views.addadvance'),
    # url(r'^monthlyattendance/','src.views.monthlyattendance'),
    # url(r'^paidamount/','src.views.paidamount'),
)
