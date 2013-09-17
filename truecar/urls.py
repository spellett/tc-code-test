from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'truecar.views.index', name='index'),
    url(r'upload/$', 'truecar.views.upload_to_database', name='upload'),
    # Examples:
    # url(r'^$', 'truecar.views.home', name='home'),
    # url(r'^truecar/', include('truecar.foo.urls')),

    url(r'^vehicles/', include('vehicles.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
