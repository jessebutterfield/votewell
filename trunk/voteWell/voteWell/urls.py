from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^states/(?P<state_abbr>\w+)', 'votes.views.state'),
    url(r'^legislator/(?P<leg_id>\d+)', 'votes.views.legislatorDetail'),
    #url(r'^static/', include(stat))
    # url(r'^$', 'voteWell.views.home', name='home'),
    # url(r'^voteWell/', include('voteWell.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
