from django.contrib import admin

from vehicles.models import *

admin.site.register(Manufacturer)
admin.site.register(VehicleModel)
admin.site.register(TrimStyle)
admin.site.register(Automobile)
