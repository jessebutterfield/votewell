from django.conf.urls import patterns, include, url
from django.views.generic import  ListView, DetailView
from votes.models import Subject

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','votes.views.home'),
    url(r'^states/(?P<state_abbr>\w+)', 'votes.views.state'),
    url(r'^legislators/(?P<leg_id>\d+)', 'votes.views.legislatorDetail'),
    url(r'^bills/(?P<bill_id>\d+)/$', 'votes.views.billDetail'),
    url(r'^bills/(?P<bill_id>\d+)/comment', 'votes.views.billComment'),
    url(r'^subjects/$', ListView.as_view(
            queryset=Subject.objects.all().order_by('name'),
            template_name='votes/subjectList.html')),
    url(r'^subjects/(?P<pk>\d+)/$', DetailView.as_view(
            model=Subject,
            template_name='votes/subject.html')),           
    #url(r'^static/', include(stat))
    # url(r'^$', 'voteWell.views.home', name='home'),
    # url(r'^voteWell/', include('voteWell.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
