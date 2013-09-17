from django.conf.urls import patterns, include, url

urlpatterns = patterns('vehicles.views',
    url(r'vehicleSearch/$', 'vehicle_search', name='vehicle_search'),
)
