from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name

"""
I wasn't sure if the relationship between Manufacturer and VehicleModel
should be many to many or if we should just have the name/manufacturer combo
be unique. It is possible that two separate companies name their vehicle with
the same name but it is also possible to have a car switch branding based on
market or other "business" factors. Perhaps this issue would be resolved with
an umbrella company that would indicate via relationships if it were the latter.
"""
class VehicleModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = ('name', 'manufacturer')

    def __unicode__(self):
        return '%s %s' % (self.manufacturer, self.name)

"""
Made vendor trim id a char field so that we can support trim ids that include
alphanumeric characters. May want to include manufacturer if trims across
manufacturers have the same values but currently assuming that trim ids are
unique.
"""
class TrimStyle(models.Model):
    vendor_trim_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s %s' % (self.vendor_trim_id, self.name)

"""
We could've added manufacturer/model information here for quicker searches but
at the cost of storage. Also I am not sure what makes an Automobile instance
unique. More clarification could make this better.
"""
class Automobile(models.Model):
    serial_number = models.CharField(max_length=12)
    vehicle_model = models.ForeignKey(VehicleModel)
    trim_style = models.ForeignKey(TrimStyle)
    year = models.DateField()

    def is_valid_vsn(self, vsn):
        return len(vsn) == 12

    def __unicode__(self):
        return '%s %s %s %s' % (self.serial_number, self.vehicle_model, self.trim_style, self.year)
