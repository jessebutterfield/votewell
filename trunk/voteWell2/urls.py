from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import logout, login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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
    url(r'^register.html/$', 'votes.views.register'),
    url(r'^register/submit', 'votes.views.submitRegistration'),
    url(r'^logout/$',logout,{'next_page': '/'}),
    url(r'^login/$', login),
    url(r'^search/$','votes.views.search'),
    url(r'^search/(?P<search_type>\w+)','votes.views.searchSubmit'),
    # url(r'^$', 'voteWell2.views.home', name='home'),
    # url(r'^voteWell2/', include('voteWell2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()

