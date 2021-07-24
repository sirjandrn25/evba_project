from django.contrib import admin
from tracker.models import *

# Register your models here.

admin.site.register(Service)
admin.site.register(Mechanic)
admin.site.register(MechanicProfile)
admin.site.register(Driver)
admin.site.register(DriverProfile)
admin.site.register(Help)
admin.site.register(Feedback)