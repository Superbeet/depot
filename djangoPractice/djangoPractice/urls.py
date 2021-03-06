# from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from depotapp.views import hello

urlpatterns = patterns('',
    url(r'^hello/$', hello),
)

urlpatterns += patterns ('',
 (r'^depotapp/', include('depotapp.urls')),
)

urlpatterns += staticfiles_urlpatterns()