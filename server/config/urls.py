from django.conf.urls import patterns, include, url
import os.path
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'browser.views.home', name='home'),
    # url(r'^browser/', include('browser.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^gateway/', 'config.amfgateway.my_gateway'),
	url(r'^crossdomain.xml$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.dirname(__file__)), 'path': 'crossdomain.xml'}),
	url(r'^client/?$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.dirname(__file__)), 'path': os.path.join('..', 'WebOmicsViewer.html')}),
	url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)
