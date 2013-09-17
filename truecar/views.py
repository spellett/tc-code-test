from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

import datetime
import re

from truecar.forms import UploadFileForm
from vehicles.models import Automobile, Manufacturer, TrimStyle, VehicleModel

def index(request):
    return redirect('vehicle_search')

def upload_to_database(request):
    template_vars = {}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            f = request.FILES['file']

            data_regex = r'(?P<vsn>[^,]+),(?P<tid>[^,]+),(?P<year>[^,]+),(?P<make>[^,]+),(?P<model>[^,]+),(?P<trim_name>.+)'

            for line in f:
                # parse the data out of each line
                parsed_data = re.match(data_regex, line)

                # if manufacturer doesn't exist, add it to the database
                manufacturer_name =  parsed_data.group('make')

                manufacturer, manufacturer_created = Manufacturer.objects.get_or_create(name=manufacturer_name)

                # if model doesn't exist, add it to the database
                model_name = parsed_data.group('model')

                vehicle_model, vehicle_model_created = VehicleModel.objects.get_or_create(name=model_name, manufacturer=manufacturer)

                # if trim doesn't exist, add it to the database
                tid = parsed_data.group('tid')
                trim_name = parsed_data.group('trim_name').strip('"')
                
                trim, trim_created = TrimStyle.objects.get_or_create(vendor_trim_id=tid, name=trim_name)

                # if automobile doesn't exist, add it to the database
                vsn = parsed_data.group('vsn').upper()
                year = int(parsed_data.group('year'))
                date = datetime.date(year, 1, 1)

                automobile = Automobile(serial_number=vsn, vehicle_model=vehicle_model, trim_style=trim, year=date)
                automobile.save()

        f.close()
    else:
        form = UploadFileForm()
        print 'test not post'

    template_vars['form'] = form

    return render_to_response('test.html', template_vars, context_instance=RequestContext(request))
