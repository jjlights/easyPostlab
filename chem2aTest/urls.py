from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chem2aTest.views.home', name='home'),
    # url(r'^chem2aTest/', include('chem2aTest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login/$','login.views.userLogin'),
    url(r'^main/$','login.views.main'),
    url(r'^prelab_quiz/$', 'prelabq.views.prelablst'),
    url(r'^prelab_quiz/(?P<quiz_id>\d+)/$', 'prelabq.views.prelabqz'),
    url(r'^postlab_quiz/$', 'postlabq.views.postlablst'),
    url(r'^postlab_quiz/(?P<quiz_id>\d+)/$', 'postlabq.views.postlabqz'),
    url(r'^edit/$', 'editq.views.editlst'),
    url(r'^edit/(?P<quiz_id>\d+)/$', 'editq.views.editqzlst'),
    url(r'^reports/$', 'reports.views.reportlst'),
    url(r'^reports/(?P<sec_id>\d+)/(?P<quiz_id>\d+)/$', 'postlabq.views.secqzReport'),
    url(r'^reports/(?P<stu_id>\d+)/(?P<quiz_id>\d+)/$', 'postlabq.views.stuqzReport'),
    url(r'^reports/(?P<stu_id>\d+)/$', 'postlabq.views.studentReport'),
    url(r'^admin/', include(admin.site.urls)),
)
